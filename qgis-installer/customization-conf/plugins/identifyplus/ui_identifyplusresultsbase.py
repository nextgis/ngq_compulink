# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/identifyplusresultsbase.ui'
#
# Created: Fri Mar 13 13:49:59 2015
#      by: PyQt4 UI code generator 4.10.2
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

class Ui_IdentifyPlusResults(object):
    def setupUi(self, IdentifyPlusResults):
        IdentifyPlusResults.setObjectName(_fromUtf8("IdentifyPlusResults"))
        IdentifyPlusResults.resize(303, 507)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(IdentifyPlusResults.sizePolicy().hasHeightForWidth())
        IdentifyPlusResults.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(IdentifyPlusResults)
        self.verticalLayout.setContentsMargins(0, 0, 0, 10)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(10, 5, 10, 0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.lblFeatures = QtGui.QLabel(IdentifyPlusResults)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblFeatures.sizePolicy().hasHeightForWidth())
        self.lblFeatures.setSizePolicy(sizePolicy)
        self.lblFeatures.setWordWrap(True)
        self.lblFeatures.setObjectName(_fromUtf8("lblFeatures"))
        self.verticalLayout_4.addWidget(self.lblFeatures)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnFirstRecord = QtGui.QToolButton(IdentifyPlusResults)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/first.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnFirstRecord.setIcon(icon)
        self.btnFirstRecord.setObjectName(_fromUtf8("btnFirstRecord"))
        self.horizontalLayout.addWidget(self.btnFirstRecord)
        self.btnPrevRecord = QtGui.QToolButton(IdentifyPlusResults)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/previous.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnPrevRecord.setIcon(icon1)
        self.btnPrevRecord.setObjectName(_fromUtf8("btnPrevRecord"))
        self.horizontalLayout.addWidget(self.btnPrevRecord)
        self.btnNextRecord = QtGui.QToolButton(IdentifyPlusResults)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/next.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnNextRecord.setIcon(icon2)
        self.btnNextRecord.setObjectName(_fromUtf8("btnNextRecord"))
        self.horizontalLayout.addWidget(self.btnNextRecord)
        self.btnLastRecord = QtGui.QToolButton(IdentifyPlusResults)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/last.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnLastRecord.setIcon(icon3)
        self.btnLastRecord.setObjectName(_fromUtf8("btnLastRecord"))
        self.horizontalLayout.addWidget(self.btnLastRecord)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.verticalLayout_4)
        self.widget = QtGui.QWidget(IdentifyPlusResults)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.loObjectContainer = QtGui.QVBoxLayout(self.widget)
        self.loObjectContainer.setSpacing(0)
        self.loObjectContainer.setMargin(0)
        self.loObjectContainer.setObjectName(_fromUtf8("loObjectContainer"))
        self.verticalLayout.addWidget(self.widget)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.progressBar = QtGui.QProgressBar(IdentifyPlusResults)
        self.progressBar.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setBaseSize(QtCore.QSize(0, 0))
        self.progressBar.setStyleSheet(_fromUtf8("height:10"))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.horizontalLayout_2.addWidget(self.progressBar)
        self.pushButton = QtGui.QPushButton(IdentifyPlusResults)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setStyleSheet(_fromUtf8("height:10;width:10"))
        self.pushButton.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/close.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon4)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.lblIdentifyStatus = QtGui.QLabel(IdentifyPlusResults)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblIdentifyStatus.sizePolicy().hasHeightForWidth())
        self.lblIdentifyStatus.setSizePolicy(sizePolicy)
        self.lblIdentifyStatus.setTextFormat(QtCore.Qt.AutoText)
        self.lblIdentifyStatus.setScaledContents(False)
        self.lblIdentifyStatus.setWordWrap(True)
        self.lblIdentifyStatus.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.lblIdentifyStatus.setObjectName(_fromUtf8("lblIdentifyStatus"))
        self.verticalLayout.addWidget(self.lblIdentifyStatus)

        self.retranslateUi(IdentifyPlusResults)
        QtCore.QMetaObject.connectSlotsByName(IdentifyPlusResults)

    def retranslateUi(self, IdentifyPlusResults):
        IdentifyPlusResults.setWindowTitle(_translate("IdentifyPlusResults", "Form", None))
        self.lblFeatures.setText(_translate("IdentifyPlusResults", "TextLabel", None))
        self.btnFirstRecord.setToolTip(_translate("IdentifyPlusResults", "First feature", None))
        self.btnFirstRecord.setText(_translate("IdentifyPlusResults", "...", None))
        self.btnPrevRecord.setToolTip(_translate("IdentifyPlusResults", "Previous feature", None))
        self.btnPrevRecord.setText(_translate("IdentifyPlusResults", "...", None))
        self.btnNextRecord.setToolTip(_translate("IdentifyPlusResults", "Next feature", None))
        self.btnNextRecord.setText(_translate("IdentifyPlusResults", "...", None))
        self.btnLastRecord.setToolTip(_translate("IdentifyPlusResults", "Last feature", None))
        self.btnLastRecord.setText(_translate("IdentifyPlusResults", "...", None))
        self.lblIdentifyStatus.setText(_translate("IdentifyPlusResults", "Identification status", None))

import resources_rc
