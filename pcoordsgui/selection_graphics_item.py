from PyQt4 import QtCore, QtGui

import defaults


class SelectionItem(QtGui.QGraphicsItem):

    def __init__(self, image, scene, lines, x, y):
        QtGui.QGraphicsItem.__init__(self)
        self.color = QtGui.QColor(QtCore.qrand() % 256, QtCore.qrand() % 256,
                QtCore.qrand() % 256)
        self.setToolTip("Drag this item over the axis to remove lines")
        self.setCursor(QtCore.Qt.OpenHandCursor)
        # Internal variable to get the global selection position on the axis
        self.axisPosY = y
        self.axisPosX = x
        self.setPos(x, y)
        self.scene = scene
        self.lines = lines
        self.axislimits = {}
        self.axisid = self.axisGetfromX(self.axisPosX)
        self.image = image

    def boundingRect(self):
            return QtCore.QRectF(-20, 2, 20, -2)

    def paint(self, painter, option, widget):
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1))
        painter.setBrush(QtGui.QBrush(self.color))
        painter.drawLine(-20, 0, 20, 0)

    def mouseMoveEvent(self, event):
        self.axisPosY = self.axisPosY + event.pos().y()
        self.moveBy(0, event.pos().y())

    def mouseReleaseEvent(self, event):
        limits = {}

        limits['min'] = 0
        limits['max'] = self.axisPosY
        self.axislimits[self.axisid] = limits

        self.hideAxisItems(self.axisid, limits)
        #self.lines.addLines(self.lines.maxLinesGet(), self.axislimits)

    def mousePressEvent(self, event):
            if event.button() != QtCore.Qt.LeftButton:
                    event.ignore()
                    return

    def axisGetfromX(self, x):
        return int(x / defaults.axiswidth)

    def hideAxisItems(self, axisid, limits):
        itemnb = 0
        for item in self.scene.items():
            if itemnb == 0:
            itemnb = itemnb + 1
            if itemnb == self.image['axes_number']:
                itemnb = 0
