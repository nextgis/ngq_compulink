# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\attributestable.ui'
#
# Created: Tue Dec 23 14:05:42 2014
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AttributesTable(object):
    def setupUi(self, AttributesTable):
        AttributesTable.setObjectName(_fromUtf8("AttributesTable"))
        AttributesTable.resize(552, 434)
        self.verticalLayout = QtGui.QVBoxLayout(AttributesTable)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tblAttributes = QtGui.QTableWidget(AttributesTable)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblAttributes.sizePolicy().hasHeightForWidth())
        self.tblAttributes.setSizePolicy(sizePolicy)
        self.tblAttributes.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tblAttributes.setAutoScroll(True)
        self.tblAttributes.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tblAttributes.setAlternatingRowColors(True)
        self.tblAttributes.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tblAttributes.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblAttributes.setTextElideMode(QtCore.Qt.ElideNone)
        self.tblAttributes.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerItem)
        self.tblAttributes.setShowGrid(True)
        self.tblAttributes.setObjectName(_fromUtf8("tblAttributes"))
        self.tblAttributes.setColumnCount(2)
        self.tblAttributes.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tblAttributes.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tblAttributes.setHorizontalHeaderItem(1, item)
        self.tblAttributes.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tblAttributes)

        self.retranslateUi(AttributesTable)
        QtCore.QMetaObject.connectSlotsByName(AttributesTable)

    def retranslateUi(self, AttributesTable):
        AttributesTable.setWindowTitle(QtGui.QApplication.translate("AttributesTable", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.tblAttributes.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("AttributesTable", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.tblAttributes.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("AttributesTable", "Value", None, QtGui.QApplication.UnicodeUTF8))

