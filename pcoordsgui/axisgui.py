from PyQt4 import QtCore, QtGui

import defaults


#class AxisName(QtGui.QWidget):
class AxisName(QtGui.QComboBox):

    def __init__(self, ui, parent=None):
        QtGui.QWidget.__init__(self, parent)

    def setItemName(self, label, id):
        """Set the item name in Combo Box"""
        itemlabel = ""
        if label:
            itemlabel = label
        else:
            itemlabel = "axis%d" % id
        self.addItem(itemlabel)
        return itemlabel

    def getCurrentIndex(self):
        return self.currentIndex()


def addAxes(image, scene, lines, axes_number, ui):
    pen = QtGui.QPen()
    pen.setColor(QtCore.Qt.black)

    i = 0
    while i < axes_number:
        # Draw axes lines
        scene.addLine(i * defaults.axiswidth, 0,
                      i * defaults.axiswidth, image['height'],
                      pen)

        i = i + 1
