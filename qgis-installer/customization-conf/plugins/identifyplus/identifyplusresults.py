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
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *

from ui_attributestable import Ui_AttributesTable
from ui_attributestablewithimages import Ui_AttributesTableWithImages
from ui_identifyplusresultsbase import Ui_IdentifyPlusResults

from representations import RepresentationContainer

class IdentifyPlusResults(QWidget, Ui_IdentifyPlusResults):
    def __init__(self, qgsMapCanvas, parent):
        QWidget.__init__(self, parent)
        
        if not isinstance(qgsMapCanvas, QgsMapCanvas):
            raise TypeError("IdentifyPlusModel expected a qgis._gui.QgsMapCanvas, got a {} instead".format(type(qgsMapCanvas)))
        
        self.setupUi(self)
        
        self._qgsMapCanvas = qgsMapCanvas
        
        self._objects = list()
        self.currentObjectIndex = -1
        
        self.btnFirstRecord.clicked.connect(self.firstRecord)
        self.btnLastRecord.clicked.connect(self.lastRecord)
        self.btnNextRecord.clicked.connect(self.nextRecord)
        self.btnPrevRecord.clicked.connect(self.prevRecord)
        
        self.lblFeatures.setText(self.tr("No features"))
        
        self.btnFirstRecord.setEnabled(False)
        self.btnLastRecord.setEnabled(False)
        self.btnNextRecord.setEnabled(False)
        self.btnPrevRecord.setEnabled(False)

        self.representations = RepresentationContainer(self)
        self.loObjectContainer.addWidget(self.representations)
        
        self.progressBar.setVisible(False)
        self.pushButton.setVisible(False)
        self.lblIdentifyStatus.setVisible(False)
        
        self.thread = None;
        self.worker = None;
    
    def setModel(self, model):
        self.__model = model
        self.__model.identificationProgress.connect(self.identifyProgressHandel)
        self.__model.identificationLayer.connect(self.identifyMessageHandel)
        self.__model.finished.connect(self.identifyFinishedHandel)
        self.__model.reseted.connect(self.modelResetHandel)
        self.__model.objectsAppended.connect(self.modelAppendObjectsHandel)
    
    def identifyMessageHandel(self, layerName):
         self.lblIdentifyStatus.setText( self.tr("Process layer: %s")%layerName )
    
    def identifyProgressHandel(self, i1, i2):
        if i1 == 0:
            self.progressBar.setVisible(True)
            self.lblIdentifyStatus.setVisible(True)
            self.progressBar.setRange(i1, i2)
        else:
            self.progressBar.setValue(i1)
    
    def identifyFinishedHandel(self):
        self.progressBar.setVisible(False)
        self.lblIdentifyStatus.setVisible(False)
        self.progressBar.setValue(0)
    
    def modelChangeProcess(self):
        if len(self._model.objects) == 0:
            self.resetModelProcess()
        else:
            self.changeModelProcess()
            
        if  self._model.state == self._model.IdentificationIsDone:
            self.finishedModelProcess()
    
    def modelResetHandel(self):
        self.currentObjectIndex = -1
        
        self.lblFeatures.setText(self.tr("Objects not found"))
        
        self.btnFirstRecord.setEnabled(False)
        self.btnLastRecord.setEnabled(False)
        self.btnNextRecord.setEnabled(False)
        self.btnPrevRecord.setEnabled(False)
            
        self.representations.clear()
        self.parent().show()
    
    def modelAppendObjectsHandel(self):
        if self.__model.objectsCount() > 0:
            self.btnFirstRecord.setEnabled(True)
            self.btnLastRecord.setEnabled(True)
            self.btnNextRecord.setEnabled(True)
            self.btnPrevRecord.setEnabled(True)
            
            self.updateInterface()
            if self.currentObjectIndex == -1:
                self.firstRecord()
        else:
            self.lblFeatures.setText(self.tr("Objects not found"))
            self.btnFirstRecord.setEnabled(False)
            self.btnLastRecord.setEnabled(False)
            self.btnNextRecord.setEnabled(False)
            self.btnPrevRecord.setEnabled(False)
            QgsMessageLog.logMessage(self.tr("Objects not found"), u'IdentifyPlus', QgsMessageLog.WARNING)
            
    def firstRecord(self):
        self.currentObjectIndex = 0
        self._loadFeatureAttributes()
        
    def lastRecord(self):
        self.currentObjectIndex = self.__model.objectsCount() - 1
        self._loadFeatureAttributes()

    def nextRecord(self):
        self.currentObjectIndex += 1
        if self.currentObjectIndex >= self.__model.objectsCount():
          self.currentObjectIndex = 0
        
        self._loadFeatureAttributes()

    def prevRecord(self):
        self.currentObjectIndex = self.currentObjectIndex - 1
        if self.currentObjectIndex < 0:
            self.currentObjectIndex = self.__model.objectsCount() - 1
    
        self._loadFeatureAttributes()
    
    def _loadFeatureAttributes(self):
        self.updateInterface()
        obj = self.__model.data(self.currentObjectIndex)
        self.representations.takeControl(obj)
    
    def updateInterface(self):
        self.lblFeatures.setText(
            self.tr("Feature %s from %s (%s)") % (
                self.currentObjectIndex + 1, 
                self.__model.objectsCount(),
                self.__model.data(self.currentObjectIndex).qgsMapLayer.name() ))
        
class IdentifyPlusResultsDock(QDockWidget):
    def __init__(self, model):
        QDockWidget.__init__(self, None)
        self.setWindowTitle(self.tr("IdentifyPlus"))