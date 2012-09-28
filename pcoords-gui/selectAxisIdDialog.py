
from PyQt4 import QtCore, QtGui
from selectAxisIdDialogUi import Ui_axisSpinBox


class buildSelectIdPanel (QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_axisSpinBox()
        self.ui.setupUi(self)
        self.parent = parent
        self.ui.axisIdSpinBox.setMinimum(1)
        self.ui.axisIdSpinBox.setMaximum(self.parent.axes_number)
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL('accepted()'), self.accept)

    def accept(self):
        self.parent.scene.AxisIncrease(self.ui.axisIdSpinBox.value())
        self.close()
