# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setWidthDialog.ui'
#
# Created: Wed Sep  9 10:44:38 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_setWidth(object):
    def setupUi(self, setWidth):
        setWidth.setObjectName("setWidth")
        setWidth.setWindowModality(QtCore.Qt.WindowModal)
        setWidth.resize(246, 107)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(setWidth.sizePolicy().hasHeightForWidth())
        setWidth.setSizePolicy(sizePolicy)
        setWidth.setMinimumSize(QtCore.QSize(246, 107))
        setWidth.setMaximumSize(QtCore.QSize(246, 107))
        self.buttonBox = QtGui.QDialogButtonBox(setWidth)
        self.buttonBox.setGeometry(QtCore.QRect(150, 20, 81, 241))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widthSpinBox = QtGui.QDoubleSpinBox(setWidth)
        self.widthSpinBox.setGeometry(QtCore.QRect(10, 40, 131, 27))
        self.widthSpinBox.setObjectName("widthSpinBox")

        self.retranslateUi(setWidth)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), setWidth.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), setWidth.reject)
        QtCore.QMetaObject.connectSlotsByName(setWidth)

    def retranslateUi(self, setWidth):
        setWidth.setWindowTitle(QtGui.QApplication.translate("setWidth", "Set Width", None, QtGui.QApplication.UnicodeUTF8))

