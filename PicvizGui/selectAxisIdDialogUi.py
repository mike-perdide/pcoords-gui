# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'selectAxisIdDialog.ui'
#
# Created: Wed Sep  9 10:44:38 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_axisSpinBox(object):
    def setupUi(self, axisSpinBox):
        axisSpinBox.setObjectName("axisSpinBox")
        axisSpinBox.setWindowModality(QtCore.Qt.WindowModal)
        axisSpinBox.resize(246, 107)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(axisSpinBox.sizePolicy().hasHeightForWidth())
        axisSpinBox.setSizePolicy(sizePolicy)
        axisSpinBox.setMinimumSize(QtCore.QSize(246, 107))
        axisSpinBox.setMaximumSize(QtCore.QSize(246, 107))
        self.buttonBox = QtGui.QDialogButtonBox(axisSpinBox)
        self.buttonBox.setGeometry(QtCore.QRect(150, 20, 81, 241))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.axisIdSpinBox = QtGui.QSpinBox(axisSpinBox)
        self.axisIdSpinBox.setGeometry(QtCore.QRect(10, 40, 121, 27))
        self.axisIdSpinBox.setObjectName("axisIdSpinBox")

        self.retranslateUi(axisSpinBox)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), axisSpinBox.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), axisSpinBox.reject)
        QtCore.QMetaObject.connectSlotsByName(axisSpinBox)

    def retranslateUi(self, axisSpinBox):
        axisSpinBox.setWindowTitle(QtGui.QApplication.translate("axisSpinBox", "Select Axis ID", None, QtGui.QApplication.UnicodeUTF8))

