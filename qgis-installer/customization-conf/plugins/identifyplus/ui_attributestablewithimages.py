# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\attributestablewithimages.ui'
#
# Created: Wed Dec 03 16:56:33 2014
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AttributesTableWithImages(object):
    def setupUi(self, AttributesTableWithImages):
        AttributesTableWithImages.setObjectName(_fromUtf8("AttributesTableWithImages"))
        AttributesTableWithImages.resize(516, 299)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AttributesTableWithImages.sizePolicy().hasHeightForWidth())
        AttributesTableWithImages.setSizePolicy(sizePolicy)
        AttributesTableWithImages.setStyleSheet(_fromUtf8(""))
        self.verticalLayout_3 = QtGui.QVBoxLayout(AttributesTableWithImages)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.tabWidget = QtGui.QTabWidget(AttributesTableWithImages)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.vlAtributesViewContainer = QtGui.QVBoxLayout(self.tab)
        self.vlAtributesViewContainer.setSpacing(2)
        self.vlAtributesViewContainer.setMargin(0)
        self.vlAtributesViewContainer.setObjectName(_fromUtf8("vlAtributesViewContainer"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(3, 3, 3, 0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.galleryWidget = QtGui.QWidget(self.tab_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.galleryWidget.sizePolicy().hasHeightForWidth())
        self.galleryWidget.setSizePolicy(sizePolicy)
        self.galleryWidget.setObjectName(_fromUtf8("galleryWidget"))
        self.vlImageGaleryContainer = QtGui.QVBoxLayout(self.galleryWidget)
        self.vlImageGaleryContainer.setMargin(0)
        self.vlImageGaleryContainer.setObjectName(_fromUtf8("vlImageGaleryContainer"))
        self.verticalLayout_2.addWidget(self.galleryWidget)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setContentsMargins(-1, 5, 20, 10)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.btnLoadPhoto = QtGui.QToolButton(self.tab_2)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnLoadPhoto.setIcon(icon)
        self.btnLoadPhoto.setIconSize(QtCore.QSize(24, 24))
        self.btnLoadPhoto.setObjectName(_fromUtf8("btnLoadPhoto"))
        self.horizontalLayout_4.addWidget(self.btnLoadPhoto)
        self.btnSaveAllPhotos = QtGui.QToolButton(self.tab_2)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/download.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSaveAllPhotos.setIcon(icon1)
        self.btnSaveAllPhotos.setIconSize(QtCore.QSize(24, 24))
        self.btnSaveAllPhotos.setObjectName(_fromUtf8("btnSaveAllPhotos"))
        self.horizontalLayout_4.addWidget(self.btnSaveAllPhotos)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout_3.addWidget(self.tabWidget)

        self.retranslateUi(AttributesTableWithImages)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(AttributesTableWithImages)

    def retranslateUi(self, AttributesTableWithImages):
        AttributesTableWithImages.setWindowTitle(QtGui.QApplication.translate("AttributesTableWithImages", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("AttributesTableWithImages", "Attributes", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLoadPhoto.setToolTip(QtGui.QApplication.translate("AttributesTableWithImages", "Load photo to database", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLoadPhoto.setText(QtGui.QApplication.translate("AttributesTableWithImages", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSaveAllPhotos.setToolTip(QtGui.QApplication.translate("AttributesTableWithImages", "Save all photos to disk", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSaveAllPhotos.setText(QtGui.QApplication.translate("AttributesTableWithImages", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("AttributesTableWithImages", "Image", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
