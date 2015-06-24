# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './quick_geocoding_toolbox.ui'
#
# Created: Mon May 12 00:12:51 2014
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_QuickGeocodingToolbox(object):
    def setupUi(self, QuickGeocodingToolbox):
        QuickGeocodingToolbox.setObjectName(_fromUtf8("QuickGeocodingToolbox"))
        QuickGeocodingToolbox.resize(255, 379)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.cmbGeocoder = QtGui.QComboBox(self.dockWidgetContents)
        self.cmbGeocoder.setObjectName(_fromUtf8("cmbGeocoder"))
        self.verticalLayout.addWidget(self.cmbGeocoder)
        self.txtSearch = QgsFilterLineEdit(self.dockWidgetContents)
        self.txtSearch.setObjectName(_fromUtf8("txtSearch"))
        self.verticalLayout.addWidget(self.txtSearch)
        self.lstSearchResult = QtGui.QListWidget(self.dockWidgetContents)
        self.lstSearchResult.setObjectName(_fromUtf8("lstSearchResult"))
        self.verticalLayout.addWidget(self.lstSearchResult)
        QuickGeocodingToolbox.setWidget(self.dockWidgetContents)

        self.retranslateUi(QuickGeocodingToolbox)
        QtCore.QMetaObject.connectSlotsByName(QuickGeocodingToolbox)

    def retranslateUi(self, QuickGeocodingToolbox):
        QuickGeocodingToolbox.setWindowTitle(_translate("QuickGeocodingToolbox", "Quick geocoding", None))
        self.txtSearch.setToolTip(_translate("QuickGeocodingToolbox", "Enter address for geocoding", None))

from qgis.gui import QgsFilterLineEdit
