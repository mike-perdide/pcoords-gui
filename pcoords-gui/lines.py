from PyQt4 import QtCore, QtGui

import defaults


class Line:
    def __init__(self, scene, image, axes_number, ui, comboList):
        self.scene = scene
        self.image = image
        self.axes_number = axes_number
        self.ui = ui
        self.comboList = comboList

    def hex2dec(self, s):
        '''This function converts an hex string to an integer value)'''
        return int(s, 16)

    def QTColorGet(self, color):

        r = self.hex2dec(color[1:3])
        g = self.hex2dec(color[3:5])
        b = self.hex2dec(color[5:7])
        return QtGui.QColor(r, g, b)

    def addLines(self, show_max, axislimits=None):
        pen = QtGui.QPen()
        self.backupRows = []
        self.backupRows.append([])
        #print str(axislimits)
        parentcontainer = []
        linecounter = self.axes_number - 1
        plotnb = -1
        parentDict = {}
        row = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(row)
        hidden = []
        for line in self.image['lines']:
            plotnb = plotnb + 1
            linecounter = linecounter + 1
            qtcolor = self.QTColorGet(line['color'])
            pen.setColor(qtcolor)
            pen.setWidthF(line['penwidth'])
            currentLine = lineItem(plotnb * defaults.axiswidth, self.image['height'] - line['y1'], (plotnb + 1) *
                         defaults.axiswidth, self.image['height'] - line['y2'])
            currentLine.setToolTip("%s -> %s" % (line['x1_strval'], line['x2_strval']))
            currentLine.setPen(pen)
            currentLine.setCursor(QtCore.Qt.OpenHandCursor)
            currentLine.setLayer(line['layer'])
            self.scene.createLayer(line['layer'], linecounter, currentLine)
            self.scene.addItem(currentLine)
            self.ui.tableWidget.setItem(row, plotnb, QtGui.QTableWidgetItem(line['x1_strval']))
            self.backupRows[row].append(line['x1_strval'])
            currentLine.setOneRow(self.ui.tableWidget.item(row, plotnb))
            parentcontainer.append(linecounter)
            if line['hidden']:
                hidden.append(currentLine)
            if plotnb == self.axes_number - 2:
                self.ui.tableWidget.setItem(row, plotnb + 1, QtGui.QTableWidgetItem(line['x2_strval']))
                currentLine.setTwoRow(self.ui.tableWidget.item(row, plotnb), self.ui.tableWidget.item(row, plotnb + 1))
                self.backupRows[row].append(line['x2_strval'])
                row = self.ui.tableWidget.rowCount()
                self.backupRows.append([])
                self.ui.tableWidget.insertRow(row)
                for each in parentcontainer:
                    parentDict[each] = parentcontainer
                del parentcontainer
                parentcontainer = []
                plotnb = -1

        count = 0 #Set the headers of tableWidget
        for each in self.comboList:
            self.ui.tableWidget.horizontalHeaderItem(count).setText(each.currentText().__str__())
            count = count + 1
        #remove a unused row
        self.ui.tableWidget.removeRow(row)
        #Sets a backup control value, to slider hide/show correctly and efficient
        self.hideValue = linecounter - (self.axes_number - 1) / (self.axes_number - 1)
        #Gets items of scene only 1 time
        self.graph_item = self.scene.items()
        self.scene.getItems(self.graph_item, self.axes_number)
        self.graph_size = len(self.graph_item)

        for each in parentDict:
            count = 0
            parentList = []
            for i in parentDict[each]:
                variant = QtCore.QVariant(i)
                self.graph_item[each].setData(count, variant)
                parentList.append(self.graph_item[i])
                count = count + 1
            self.graph_item[each].setParents(parentList, self.graph_item, each)
            del parentList
        self.doSelectable()
        self.scene.hideList(hidden)

    def doSelectable(self):
        count = 0
        for each in self.graph_item:
            if (count > self.axes_number - 1):
                each.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
            count = count + 1

    def removeLines(self):
        itemnb = 0
        for each in self.graph_item:
            if itemnb >= self.axes_number:
                self.scene.removeItem(each)
            itemnb = itemnb + 1

    def showLines(self, show_max):
        itemnb = 0
        counter = self.hideValue * (self.axes_number - 1)
        while(counter <= show_max * (self.axes_number - 1) + (self.axes_number - 1)):
            if (counter < self.graph_size):
                self.graph_item[counter].show()
            counter = counter + 1

        if(show_max >= self.hideValue):
            for i in range(self.hideValue, show_max):
                self.ui.tableWidget.showRow(i)
                #plotnb = -1
                #for each in self.backupRows[i]:
                #    plotnb = plotnb + 1
                #    self.ui.tableWidget.setItem(i, plotnb, QtGui.QTableWidgetItem(each))
        self.hideValue = show_max

    def update_lines_view(self, value):
        count_item = 0
        for item in self.graph_item:
            if (count_item >= self.axes_number and (count_item > value * (self.axes_number - 1) + self.axes_number - 1)):
                item.hide()
            count_item = count_item + 1
        reversed_range = range(value, self.hideValue)
        reversed_range.reverse()
        for i in reversed_range:
            self.ui.tableWidget.hideRow(i)
        self.showLines(value)
        #self.AxisIncrease(2)

    def clean(self):
        del self.backupRows
        self.removeLines()
        del self.graph_item
        del self.graph_size

        reversed_range = range(0, self.ui.tableWidget.rowCount() + 1)
        reversed_range.reverse()
        for i in reversed_range:
            self.ui.tableWidget.removeRow(i)

    def maxLinesGet(self):
        linecounter = 0
        for line in self.image['lines']:
            linecounter = linecounter + 1
        return linecounter

    def decreaseWidth(self):
        count = 0
        for each in self.graph_item:
            if count > self.axes_number - 1:
                each.decreaseWidth()
            count = count + 1

    def increaseWidth(self):
        count = 0
        for each in self.graph_item:
            if count > self.axes_number - 1:
                each.increaseWidth()
            count = count + 1


class lineItem(QtGui.QGraphicsLineItem):

    def setParents(self, parentList, allItems, Id):
        # = parentList
        self.parentList = [item for item in parentList if not item in [self]]

        self.selec = False
        self.allItems = allItems
        self.ctrlPressed = False
        self.backupPen = self.pen()
        self.selectWidth = 2.5
        self.id = Id
        self.select_pen = QtGui.QPen(QtCore.Qt.gray)
        self.select_pen.setStyle(QtCore.Qt.DotLine)
        self.select_pen.setWidthF(self.selectWidth)
        self.parentSelected = False

    def getLayer(self):
        return self.layer

    def setLayer(self, name):
        self.layer = name

    def setOneRow(self, row1):
        self.tableItem1 = row1
        self.haveTwoItems = False

    def setTwoRow(self, row1, row2):
        self.tableItem1 = row1
        self.tableItem2 = row2
        self.haveTwoItems = True

    def testprint(self):
        print "I'm printable!"

    def dragEnterEvent(self, event):
        print event

    def setPressed(self, key):
        #print "Yes"
        if(key == QtCore.Qt.Key_Control):
            self.ctrlPressed = True

    def setUnPressed(self, key):
        #print "No"
        if(key == QtCore.Qt.Key_Control):
            self.ctrlPressed = False

    def myIsSelected(self):
        return self.selec

    def isPressed(self):
        return self.ctrlPressed

    def setBackupPen(self, pen):
        self.backupPen = pen

    def getBackupPen(self):
        return self.backupPen

    def decreaseWidth(self):
        pen = self.pen()
        if(self.myIsSelected()):
            pen.setWidthF(pen.widthF() * 1 / 1.05)
            self.selectWidth = pen.widthF()
            self.backupPen.setWidthF(self.backupPen.widthF() * 1 / 1.05)
        else:
            pen.setWidthF(pen.widthF() * 1 / 1.05)
            self.selectWidth = self.selectWidth * 1 / 1.05
            self.backupPen = pen
        self.setPen(pen)

    def increaseWidth(self):
        pen = self.pen()
        if(self.myIsSelected()):
            pen.setWidthF(pen.widthF() * 1.05)
            self.selectWidth = pen.widthF()
            self.backupPen.setWidthF(self.backupPen.widthF() * 1.05)
        else:
            pen.setWidthF(pen.widthF() * 1.05)
            self.selectWidth = self.selectWidth * 1.05
            self.backupPen = pen
        self.setPen(pen)

    def setWidth(self, width):
        self.backupPen.setWidthF(width)
        self.setPen(self.backupPen)

    def selectParents(self, selection):
        for each in self.parentList:
            #each.setParentSelected(selection)
            each.setSelected(selection)

    def setParentSelected(self, value):
        self.parentSelected = value

    def mySetSelected(self, selection, first):
        if (selection):
            print "Aplicou"
            self.setPen(self.pen)
            self.setSelected(selection)
            if (first):
                self.selectParents(True)
        else:
            self.setPen(self.backupPen)
            self.setSelected(selection)
            #self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
            if (first):
                self.selectParents(False)
        self.selec = selection

    def deselectRow(self):
        if(self.haveTwoItems):
            self.tableItem2.setSelected(False)
        self.tableItem1.setSelected(False)

    def selectRow(self):
        if(self.haveTwoItems):
            self.tableItem2.setSelected(self.selec)
        self.tableItem1.setSelected(self.selec)

    def getId(self):
        return self.id

    def hoverEnterEvent(self, event):
        print event

    def itemChange(self, event, value):
        if event == QtGui.QGraphicsItem.ItemSelectedHasChanged:
            if self.isSelected():
                self.setPen(self.select_pen)
                self.selec = True
            else:
                self.setPen(self.backupPen)
                self.selec = False
        return value
