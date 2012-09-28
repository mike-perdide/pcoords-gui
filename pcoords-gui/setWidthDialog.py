
from PyQt4 import QtCore, QtGui
from setWidthDialogUi import Ui_setWidth


class buildWidthPanel (QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_setWidth()
        self.ui.setupUi(self)
        self.parent = parent
        self.ui.widthSpinBox.setMaximum(10)
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL('accepted()'), self.accept)

    def accept(self):
        self.parent.scene.changeWidth(self.ui.widthSpinBox.value())
        self.close()
