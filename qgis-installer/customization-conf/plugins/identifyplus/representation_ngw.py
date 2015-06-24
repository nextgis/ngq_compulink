# -*- coding: utf-8 -*-

#******************************************************************************
#
# IdentifyPlus
# ---------------------------------------------------------
# Extended identify tool. Supports displaying and modifying photos
#
# Copyright (C) 2012-2013 NextGIS (info@nextgis.org)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/licenses/>. You can also obtain it by writing
# to the Free Software Foundation, 51 Franklin Street, Suite 500 Boston,
# MA 02110-1335 USA.
#
#******************************************************************************
import base64
import os
import time
from urlparse import urlparse, parse_qs

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtNetwork
from ngw_external_api_python.core.ngw_resource_factory import NGWResourceFactory
from ngw_external_api_python.core.ngw_resource import NGWResource
from ngw_external_api_python.core.ngw_connection import NGWConnection
from ngw_external_api_python.core.ngw_connection_settings import NGWConnectionSettings
from ngw_external_api_python.core.ngw_vector_layer import NGWVectorLayer
from ngw_external_api_python.core.ngw_feature import NGWFeature
from ngw_external_api_python.core.ngw_attachment import NGWAttachment
from PyQt4.Qt import QObject, QFileInfo

from qgis.core import *
from qgis.gui import *

import resources_rc

class NGWImagesModel(QtCore.QAbstractListModel):
    initEnded = QtCore.pyqtSignal()    
    def __init__(self, obj, ngw_resource, parent = None):
        super(NGWImagesModel, self).__init__(parent)
        
        self.__obj = obj
        self.__ngw_resource = ngw_resource
        self.__images = []
        
        self.__thread = QtCore.QThread(self)
        self.moveToThread(self.__thread)
        self.__thread.started.connect(self.initModel)
        self.initEnded.connect(self.__thread.quit)
        self.__thread.start()
    
    def initModel(self):
        fid = self.__obj.fid
        dataProvider = self.__obj.qgsMapLayer.dataProvider()
        if dataProvider.name() == u'WFS':
            if hasattr(dataProvider, 'idFromFid') and callable(getattr(dataProvider, 'idFromFid')):
                fid = dataProvider.idFromFid(fid)
                if type(fid) != 'long':
                    fid = long(fid)
        
        self.__ngw_feature = NGWFeature(fid, self.__ngw_resource)
        self.__images_urls = []
        
        attachments = self.__ngw_feature.get_attachments()
        for attachment in attachments:
            if attachment[u'is_image'] == True:
                self.insertRow(NGWAttachment(attachment[u'id'], self.__ngw_feature))
        
        self.initEnded.emit()
          
    def rowCount(self, parent=QtCore.QModelIndex()):        
        return len( self.__images )
    
    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, row, row + count)
        
        for i in range(0, count):
            #self.__ngw_feature.unlink_attachment( self.__images_urls[row][1] )
            #self.__images_urls.remove(self.__images_urls[row])
            self.__images[row].unlink()
            self.__images.remove(self.__images[row])
            
        self.endRemoveRows()
        return True
    
    def addImage(self, image_filename):
        uploaded_file_info = self.__ngw_feature.ngw_resource._res_factory.connection.upload_file(image_filename)
        id = self.__ngw_feature.link_attachment(uploaded_file_info)
        self.insertRow(NGWAttachment(id, self.__ngw_feature))
    
    def insertRow(self, ngw_attachment):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self.__images.append(ngw_attachment)
        self.endInsertRows()
        
    def data(self, index, role=QtCore.Qt.DisplayRole):        
        if index.isValid() and role == QtCore.Qt.DecorationRole:
            return None
        
        elif index.isValid() and role == QtCore.Qt.DisplayRole:          
            return self.__images[index.row()]
                
        elif index.isValid() and role == (QtCore.Qt.UserRole + 1):
            return self.__images[index.row()]
        
        else:
            return None

class ImageLoader(QtCore.QObject):
    finished = QtCore.pyqtSignal(QtGui.QImage)
    
    def __init__(self, ngw_attachment, parent = None):
        QtCore.QObject.__init__(self, parent)
        self.__ngw_attachment = ngw_attachment
        
    def loadImage(self):
        img = QtGui.QImage()
        img_info = self.__ngw_attachment.get_image()
        res = img.loadFromData(img_info[2])
        self.finished.emit(img)
         
class ImageLabel(QtGui.QLabel):
    imageLoaded = QtCore.pyqtSignal()
    
    def __init__(self, ngw_attachment, parent = None):        
        QtGui.QLabel.__init__(self, parent)
        self.pm = None
        self.setText(self.tr("Loading..."))        
        self.__worker = ImageLoader(ngw_attachment)
        self.__thread = QtCore.QThread(self.__worker)
        self.__worker.moveToThread(self.__thread)
        self.__thread.started.connect(self.__worker.loadImage)
        self.__worker.finished.connect(self.__thread.quit)
        self.__worker.finished.connect(self.load)
        self.__thread.start()

    def load(self, img):
        self.pm = QtGui.QPixmap()
        self.pm.convertFromImage(img)
        self.clear()

        self._k = 1
        self.setScaledContents(True) 
        sp = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sp.setHeightForWidth(True)
        self.setSizePolicy(sp)
        self.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.setMinimumSize(self.pm.width() / 5, self.pm.height() / 5 )
        
        self._k = 1.0 * self.pm.height() / self.pm.width()
        
        self.setPixmap(self.pm)
        
        self.imageLoaded.emit()     
        
    def heightForWidth(self, width):
        if width < self.pm.size().width():
            return width * self._k
        else:
            return self.pm.size().height()

class Image(QtGui.QWidget):
    deleteImage = QtCore.pyqtSignal(QtGui.QWidget)
    downloadImage = QtCore.pyqtSignal(QtGui.QWidget)
    
    def __init__(self, ngw_attachment, parent = None):
        
        QtGui.QWidget.__init__(self, parent)

        self.__vbl_layout = QtGui.QVBoxLayout(self)
        self.__vbl_layout.setAlignment(QtCore.Qt.AlignHCenter)
        self.__vbl_layout.setContentsMargins(5, 5, 5, 5)
        self.__vbl_layout.setSpacing(0)
        
        self.__image_container = ImageLabel(ngw_attachment, self)
        self.__image_container.imageLoaded.connect(self.imageLoadedHandle)
        self.__vbl_layout.addWidget(self.__image_container)
        
        self.__w_buttons_widget = QtGui.QWidget()
        self.__hbl_buttons_layout = QtGui.QHBoxLayout(self.__w_buttons_widget)
        self.__hbl_buttons_layout.setAlignment(QtCore.Qt.AlignRight)
        self.__hbl_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.__hbl_buttons_layout.setSpacing(1)
        self.__vbl_layout.addWidget(self.__w_buttons_widget)
        
        self.__pb_download_image = QtGui.QPushButton()
        self.__pb_download_image.setIcon(QtGui.QIcon(":/icons/downloadImageBtn.png"))
        self.__pb_download_image.setToolTip( self.tr("Download photo") )
        self.__pb_download_image.setStatusTip( self.tr("Download photo") )
        self.__pb_download_image.setVisible(False)

        self.__pb_download_image.clicked.connect(self.emitDownloadImage)
        self.__hbl_buttons_layout.addWidget(self.__pb_download_image)
        
        self.__pb_delete_image = QtGui.QPushButton()
        self.__pb_delete_image.setIcon(QtGui.QIcon(":/icons/deleteImageBtn.png"))
        self.__pb_delete_image.setToolTip( self.tr("Delete photo") )
        self.__pb_delete_image.setStatusTip( self.tr("Delete photo") )
        self.__pb_delete_image.setVisible(False)
        
        self.__pb_delete_image.clicked.connect(self.emitDeleteImage)
        self.__hbl_buttons_layout.addWidget(self.__pb_delete_image)
    
    def imageLoadedHandle(self):
        self.__pb_download_image.setVisible(True)
        self.__pb_delete_image.setVisible(True)
        
    def emitDownloadImage(self):
        self.downloadImage.emit(self)
    
    def emitDeleteImage(self):
        self.deleteImage.emit(self)
        
class NGWImagesView(QtGui.QWidget):
    images_load_finish = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
#         QgsMessageLog.logMessage(
#             "NGWImagesView __init__",
#             u'IdentifyPlus',
#             QgsMessageLog.INFO)
        
        self.__model = None
        self.__images = []
        
        l=QtGui.QVBoxLayout(self)
        l.setContentsMargins(0,0,0,0)
        l.setSpacing(5)
 
        s=QtGui.QScrollArea()
        s.setWidgetResizable(True);
        #s.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sb = s.verticalScrollBar()
        stylesheet = '''
            QScrollBar:vertical {
                  border: 2px solid transparent;
                  background: transparent;
                  width: 8px;
                  margin: 0px 0 0px 0;
              }
              QScrollBar::handle:vertical {
                  background: transparent;
                  border: 2px solid #2AACAC;
                  border-radius: 1px;
                  min-height: 20px;
              }
              
              QScrollBar::add-line:vertical {
                  height: 0px;
              }
            
              QScrollBar::sub-line:vertical {
                  height: 0px;
              }
              
              
              QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                  border: 0px solid grey;
                  width: 0px;
                  height: 0px;
                  background: white;
              }
            
            
              QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                  background: none;
              }
              
            '''
        sb.setStyleSheet(stylesheet)
        
        s.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        l.addWidget(s)
        
        self.__w_buttons_widget = QtGui.QWidget()
        self.__hbl_buttons_layout = QtGui.QHBoxLayout(self.__w_buttons_widget)
        self.__hbl_buttons_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.__hbl_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.__hbl_buttons_layout.setSpacing(1)
        l.addWidget(self.__w_buttons_widget)
        
        self.__pb_download_images = QtGui.QPushButton()
        self.__pb_download_images.setIcon(QtGui.QIcon(":/icons/downloadImageBtn.png"))
        self.__pb_download_images.setToolTip( self.tr("Download photos") )
        self.__pb_download_images.setStatusTip( self.tr("Download photos") )
        self.__pb_download_images.setEnabled(False)
        self.__pb_download_images.clicked.connect(self.downloadImages)
        self.__hbl_buttons_layout.addWidget(self.__pb_download_images)
        
        self.__pb_add_image = QtGui.QPushButton()
        self.__pb_add_image.setIcon(QtGui.QIcon(":/icons/addImageBtn.png"))
        self.__pb_add_image.setToolTip( self.tr("Add photo(s)") )
        self.__pb_add_image.setStatusTip( self.tr("Add photo(s)") )
        self.__pb_add_image.clicked.connect(self.addImage)
        self.__hbl_buttons_layout.addWidget(self.__pb_add_image)
        
        
        self.w=QtGui.QWidget(self)  
        
        self.vbox=QtGui.QVBoxLayout(self.w)
        self.vbox.setSpacing(0)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        
        self.__w_images_container= QtGui.QWidget(self)
        self.__vbl_images_container= QtGui.QVBoxLayout(self.__w_images_container)
        self.__vbl_images_container.setSpacing(5)
        self.__vbl_images_container.setContentsMargins(0, 0, 0, 0)
        
        self.vbox.addWidget(self.__w_images_container)
            
        self.vbox.addSpacerItem(QtGui.QSpacerItem(1,1,QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))
        
        s.setWidget(self.w)
        
        self.__message = QtGui.QLabel(self.tr("Loading..."))
        self.__message.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.__message.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.__vbl_images_container.addWidget(self.__message)
    
    def __updateMessage(self):
#         QgsMessageLog.logMessage(
#             "NGWImagesView __updateMessage",
#             u'IdentifyPlus',
#             QgsMessageLog.INFO)
        
        if self.__model.rowCount() > 0:
            self.__pb_download_images.setEnabled(True)
            self.__message.clear()
        else:
            self.__pb_download_images.setEnabled(False)
            self.__message.setText(self.tr("No photos"))
            
    def setModel(self, model):        
        self.__model = model
        self.__model.initEnded.connect(self.loadModelData)
        self.__model.rowsRemoved.connect(self.rowsRemovedProcess)
        self.__model.rowsInserted.connect(self.rowsInsertedProcess)

    def loadModelData(self):
        self.__updateMessage()
      
    def rowsRemovedProcess(self, parent, start, end):        
        rem_ids = range(start, end)
        rem_ids.reverse()
        for i in rem_ids:
            self.__images[i].hide()
            self.__images[i].close()
            self.__images.remove(self.__images[i])
        
        self.__updateMessage()
    
    def rowsInsertedProcess(self, parent, start, end):

        for i in range(start, end+1):
            index = self.__model.index(i,0)
            data = self.__model.data(index)
            
            img = Image(data, self.w)
            img.deleteImage.connect(self.deleteImage)
            img.downloadImage.connect(self.downloadImage)
            self.__images.append(img)
            self.__vbl_images_container.addWidget(img)
            
        self.__updateMessage()
        
    def deleteImage(self, image):        
        i = self.__images.index(image)
        self.__model.removeRow(i)
        
    def addImage(self):        
        settings = QtCore.QSettings()
        lastLoadPhotoDir = settings.value("identifyplus/lastLoadPhotoDir", "", type=unicode)
        
        file_names = QtGui.QFileDialog.getOpenFileNames(self, self.tr("Choose photo(s)"), lastLoadPhotoDir, self.tr("Image Files (*.png *.jpg *.bmp)"))
        
        for file_name in file_names:
            settings.setValue("identifyplus/lastLoadPhotoDir", QtCore.QFileInfo(file_name).absolutePath())
            self.__model.addImage(file_name)
    
    def downloadImage(self, image):        
        i = self.__images.index(image)
        index = self.__model.index(i,0)
        
        ngw_attachment = self.__model.data(index, QtCore.Qt.UserRole + 1)
        
        settings = QtCore.QSettings()
        lastDir = settings.value( "identifyplus/lastSavePhotoDir", "" )
    
        fName = QtGui.QFileDialog.getSaveFileName(self,
                                            self.tr("Save photo"),
                                            lastDir
                                           )
        if fName == "":
          return
        
        file_info = QtCore.QFileInfo(fName)
        settings.setValue("identifyplus/lastSavePhotoDir", file_info.absolutePath())
        
        ngw_attachments = [ngw_attachment]
        default_names = [file_info.fileName()]
        downloadDialog = ImageDownloadDialog(ngw_attachments, file_info.absolutePath(), default_names)
        downloadDialog.exec_()
        
    def downloadImages(self):        
        settings = QtCore.QSettings()
        lastSavePhotosDir = settings.value("identifyplus/lastSavePhotosDir", "", type=unicode)
        
        dirPath = QtGui.QFileDialog.getExistingDirectory(
                    self, 
                    self.tr("Select directory fo save photos"), 
                    lastSavePhotosDir)
        
        dirPath
        if dirPath == "":
          return
      
        settings.setValue("identifyplus/lastSavePhotoDir", dirPath)
        
        ngw_attachments = []
        for i in range(0, self.__model.rowCount()):
            index = self.__model.index(i,0)
            ngw_attachments.append(self.__model.data(index, QtCore.Qt.UserRole + 1))
        
        downloadDialog = ImageDownloadDialog(ngw_attachments, dirPath)
        downloadDialog.exec_()
            
class ImageDownloadDialog(QtGui.QDialog):
    def __init__(self, ngw_attachments, save_dir, default_names = [],  parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle(self.tr("Download images process"))
        self.setFixedSize(250, 75)
        
        l = QtGui.QVBoxLayout(self)
        self.pb = QtGui.QProgressBar(self)
        self.pb.setRange(0, len(ngw_attachments))
        self.pb.setValue(0)
        l.addWidget(self.pb)
        
        self.__ngw_attachments = ngw_attachments
        self.__default_names = default_names
        
        difference_len = len(self.__ngw_attachments) - len(self.__default_names)
        if difference_len  > 0:
            self.__default_names.extend( [None]*difference_len)
            
        self.__save_dir = save_dir
        self.__current_index = 0
               
        if len(self.__ngw_attachments) > 0 :
            self.downloadNext()
    
    def downloadNext(self):
        self.pb.setValue(self.pb.value() + 1)      
        if self.__current_index == len(self.__ngw_attachments):
            self.hide()
            self.close()
            return
        
        self.worker = ImageDownloader(
            self.__ngw_attachments[self.__current_index], 
            self.__save_dir,
            self.__default_names[self.__current_index])
        
        self.__current_index = self.__current_index + 1
        
        self.thread = QtCore.QThread(self)
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(self.worker.saveImage)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.downloadNext)
        self.thread.start()

class ImageDownloader(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    def __init__(self, ngw_attachment, save_dir, filename = None, parent = None):
        QtCore.QObject.__init__(self, parent)
        self.__ngw_attachment = ngw_attachment
        self.__filename = filename
        self.__save_dir = save_dir
        
        self.__thread = QtCore.QThread(self)
        self.moveToThread(self.__thread)
        self.__thread.started.connect(self.saveImage)
        self.finished.connect(self.__thread.quit)
        self.__thread.start()
        
    def saveImage(self):
        img = QtGui.QImage()
        attachment_info = self.__ngw_attachment.get_image()
        img.loadFromData(attachment_info[2])
        
        if self.__filename is None:
            img.save(
                os.path.join(
                    self.__save_dir, 
                    attachment_info[0] + ".%s"%attachment_info[1]
                ), 
                attachment_info[1])
        else:
            img.save(
                os.path.join(
                    self.__save_dir, 
                    self.__filename + ".%s"%attachment_info[1]
                ), 
                attachment_info[1])
        self.finished.emit()
        
        
