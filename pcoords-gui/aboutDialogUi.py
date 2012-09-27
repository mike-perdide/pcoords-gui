# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aboutDialog.ui'
#
# Created: Wed Sep  9 10:44:38 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(400, 330)
        AboutDialog.setMinimumSize(QtCore.QSize(400, 330))
        AboutDialog.setMaximumSize(QtCore.QSize(400, 330))
        self.buttonBox = QtGui.QDialogButtonBox(AboutDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 280, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.plainTextEdit = QtGui.QPlainTextEdit(AboutDialog)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 10, 351, 261))
        self.plainTextEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.plainTextEdit.setObjectName("plainTextEdit")

        self.retranslateUi(AboutDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), AboutDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), AboutDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QtGui.QApplication.translate("AboutDialog", "About Picviz", None, QtGui.QApplication.UnicodeUTF8))

