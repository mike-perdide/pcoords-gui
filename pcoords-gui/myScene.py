from __future__ import division
from PyQt4 import QtCore, QtGui
import sys


class myScene(QtGui.QGraphicsScene):
    #sys.stdout = open("/var/log/picviz.log","a")
    listUndoStatement = []
    currentIncrease = 0

    # Define the last statement of picviz log file that can be to perform
    countUndo = 0

    layers = {}

    def getItems(self, items, axes):
        self.graph_items = items
        self.size_items = len(items)
        self.axes_number = axes
        self.pressed = False
        self.selected_items = []
        self.semaphore = False
        self.setItemIndexMethod(-1)
        self.groups = []
        self.maximum = []
        for i in range(0, self.axes_number):
            paxis = self.graph_items[i].line()
            self.maximum.append(paxis.y2())

    def getUi(self, ui, dic):
        self.ui = ui
        self.dic = dic

    def getButton(self, button):
        self.axisButton = button

    def mouseReleaseEvent(self, event):
        if not self.semaphore:
            for each in self.selectedItems():
                each.selectParents(True)
        else:
            self.semaphore = False

    def removeDuplicated(self):
        count_removed_lines = 0
        remove = []
        headlist = []
        count = self.axes_number

        while count < len(self.graph_items):
            headlist.append(count)
            count = count + self.axes_number - 1

        progress = QtGui.QProgressDialog("Removing lines..", "Cancel", 0, 100,
                                         self.ui.graphicsView,
                                         QtCore.Qt.WindowFlags())
        progress.show()

        for i in headlist:
            percent = i / len(self.graph_items)
            progress.setValue(percent * 100)
            count = i + self.axes_number - 1
            while count < len(self.graph_items):
                compares_count = 0
                while True:
                    point1 = self.graph_items[i + compares_count].line()
                    point2 = self.graph_items[count + compares_count].line()
                    flag1 = point1.x1() == point2.x1()
                    flag2 = point1.y1() == point2.y1()
                    flag3 = point1.x2() == point2.x2()
                    flag4 = point1.y2() == point2.y2()
                    if (flag1 and flag2 and flag3 and flag4):
                        if (compares_count == self.axes_number - 2):
                            if count not in remove:
                                remove.append(count)
                            count = count + self.axes_number - 1
                            compares_count = 0
                            if count >= len(self.graph_items):
                                break
                        else:
                            compares_count = compares_count + 1
                    else:
                        break
                count = count + self.axes_number - 1
        remove.sort()
        remove.reverse()
        count_showed = count_hidden = 0
        for each in remove:
            remove_items = []
            for i in range(each, each + self.axes_number - 1):
                remove_items.append(i - self.axes_number - 1)
            remove_items.reverse()
            for i in remove_items:
                if (self.dic['lines'][i]['hidden']):
                    count_hidden += 1
                else:
                    count_showed += 1
                del self.dic['lines'][i]
            del remove_items

        progress.setValue(100)
        self.removeAllLayers()
        self.axisButton.updateAfterRemoveDuplicated()
        del progress
        dialog = QtGui.QMessageBox(self.ui.graphicsView)
        dialog.setWindowTitle("Picviz-GUI")
        dialog.setIcon(1)
        dialog.setText("Removed %d normal lines. \nRemoved %d hidden lines." %
                    (count_showed / (self.axes_number - 1),
                     count_hidden / (self.axes_number - 1)))
        dialog.show()

    def dec2hex(self, r, g, b):
        '''return the hexadecimal string representation of rgb color'''
        red = "%X" % r
        if (red == '0'):
            red = "00"
        green = "%X" % g
        if (green == '0'):
            green = "00"
        blue = "%X" % b
        if (blue == '0'):
            blue = "00"
        return "#" + red + green + blue

    def QTColorGet(self, color):
        r = self.hex2dec(color[1:3])
        g = self.hex2dec(color[3:5])
        b = self.hex2dec(color[5:7])
        return QtGui.QColor(r, g, b)

    def hideShowAxes(self):
        for i in range(0, self.axes_number - 1):
            self.graph_items[i].hide()
#            print "HIDE %d" % (i)
        for i in range(0, self.axes_number - 1):
            self.graph_items[i].show()
#            print "SHOW %d" % (i)

    def selChanged(self):
        if (not self.semaphore):
            items = self.selectedItems()
            self.semaphore = True
            items = [item for item in items if not item in self.selected_items]
            if (self.pressed):
                for each in items:
                    each.mySetSelected(True, True)
                self.selected_items = self.selected_items + \
                                      self.selectedItems()
                self.semaphore = False
                del items
            else:
                if (self.selected_items != []):
                    for each in self.selected_items:
                        each.mySetSelected(False, True)
                    del self.selected_items
                    self.selected_items = []
                for i in items:
                    i.mySetSelected(True, True)
                self.selected_items = self.selected_items + \
                                      self.selectedItems()
                self.semaphore = False
                del items

    def cleanScene(self):
        del self.selected_items
        del self.graph_items
        del self.pr
        del self.semaphore
        del self.axes_number
        del self.layers
        self.layers = {}

    def keyPressEvent(self, key):
        pressedKey = key.key()
        count = 0
        if(pressedKey == QtCore.Qt.Key_Control):
            self.pressed = True

    def keyReleaseEvent(self, key):
        pressedKey = key.key()
        if (pressedKey == QtCore.Qt.Key_Control):
            self.pressed = False
            count = 0
            for each in self.graph_items:
                if count > self.axes_number - 1:
                    each.setUnPressed(pressedKey)
                count = count + 1

    def setSemaphore(self, flag):
        self.semaphore = flag

    def brushSelection(self):
        dialog = QtGui.QColorDialog.getColor(QtCore.Qt.white, None)

        if (dialog.isValid()):
            pen = QtGui.QPen(dialog)
            red = pen.color().red()
            green = pen.color().green()
            blue = pen.color().blue()
            color = self.dec2hex(red, green, blue)
            count = 0
            selected = self.selectedItems()
            selected2 = selected
            self.clearSelection()
            statement = "COLOR"
            #self.countUndo = self.countUndo + 1 #(self.axes_number - 1)
            for i in range(len(self.listUndoStatement) - 1,
                           self.countUndo - 1, -1):
                del self.listUndoStatement[i]

            for each in selected:
                pen.setWidthF(each.getBackupPen().widthF())
                each.setBackupPen(pen)
                each.mySetSelected(False, False)
                statement = statement \
                    + " %d " % (each.getId() - self.axes_number,) \
                    + " %s " % (self.dic['lines'][each.getId() - self.axes_number]['color'])

                self.dic['lines'][each.getId() - self.axes_number]['color'] = color
                count = count + 1

            for each in selected2:
                statement = statement \
                    + " %d " % (each.getId() - self.axes_number,) \
                    + " %s " % (self.dic['lines'][each.getId() - self.axes_number]['color'])

            self.listUndoStatement.append(statement)
#            print "COLOR"
#            print self.listUndoStatement
            self.countUndo = len(self.listUndoStatement)

    def brushSelection2(self, paramLine, paramColor, paramSelected):
        colorPen = QtGui.QColor(paramColor)
        pen = QtGui.QPen(colorPen)
        color = paramColor
        count = 0
        selected = self.selectedItems()
        self.clearSelection()
        each = self.graph_items[int(paramLine) + self.axes_number]
        pen.setWidthF(each.getBackupPen().widthF())
        each.setBackupPen(pen)
        each.mySetSelected(False, False)
        self.dic['lines'][int(paramLine)]['color'] = color
        count = count + 1

    def hideSelected(self):
        count = 0
        selected = self.selectedItems()
        #statement = "HIDE"

        for each in selected:
            if (each.getId() % (self.axes_number - 1) == 0):
                self.ui.tableWidget.hideRow(
                    (each.getId() / (self.axes_number - 1)) - 2)

        #    statement = statement + " %d " % (each.getId() - self.axes_number)
            self.dic['lines'][each.getId() - self.axes_number]['hidden'] = 1
        #self.listUndoStatement.append(statement)
        self.groups.append(self.createItemGroup(selected))
        #print "Hided:"
        #print self.listUndoStatement
        #self.countUndo = self.countUndo + 1
        #self.countUndo = len(self.listUndoStatement) #- 1
        self.clearSelection()
        self.groups[len(self.groups) - 1].hide()

    def hideSelected2(self, paramLine):
        count = 0
        each = self.graph_items[int(paramLine) + self.axes_number]
        list = []
        list.append(each)
        self.groups.append(self.createItemGroup(list))

        if (each.getId() % (self.axes_number - 1) == 0):
            self.ui.tableWidget.hideRow(
                (each.getId() / (self.axes_number - 1)) - 2)

        self.dic['lines'][each.getId() - self.axes_number]['hidden'] = 0
        self.clearSelection()
        self.groups[len(self.groups) - 1].hide()

    def hideNotSelected(self):
        count = 0
        list1 = self.selectedItems()
        for i in range(0, self.axes_number):
            # Adding the Axes to not consider them in difference
            list1.append(self.graph_items[i])
        #group = self.selected
        diff = [item for item in self.graph_items if not item in list1]
        self.groups.append(self.createItemGroup(diff))

        for each in diff:
            if (each.getId() % (self.axes_number - 1) == 0):
                self.ui.tableWidget.hideRow(
                    (each.getId() / (self.axes_number - 1)) - 2)
            self.dic['lines'][each.getId() - self.axes_number]['hidden'] = True

        for i in range(0, self.axes_number):
            # Removing the axes from selection to not caught exception in
            # self.changed()
            list1.pop()

        self.clearSelection()
        self.groups[len(self.groups) - 1].hide()

    def changeWidth(self, width):
        count = 0
        statement = "WIDTH"
        #print self.dic['lines']
        selected_items2 = self.selectedItems()
        for i in range(len(self.listUndoStatement) - 1,
                       self.countUndo - 1, -1):
                del self.listUndoStatement[i]

        for each in self.selectedItems():
            statement = statement \
                + " %d %d %d " % (each.getId() - self.axes_number,
                                  self.dic['lines'][each.getId() - self.axes_number]['penwidth'],
                                  len(self.selected_items) - 1)

            self.dic['lines'][each.getId() - self.axes_number]['penwidth'] = width
            each.setWidth(width)
            count = count + 1

        for each in selected_items2:
            statement = statement \
                + " %d %d %d " % (each.getId() - self.axes_number,
                                  self.dic['lines'][each.getId() - self.axes_number]['penwidth'],
                                  len(self.selected_items) - 1)

        #print "Statement width: %s" % (statement)
        if statement != "WIDTH":
            self.listUndoStatement.append(statement)
            #self.countUndo = self.countUndo + 1
            self.countUndo = len(self.listUndoStatement)

        #del self.listUndoStatement[len(self.listUndoStatement) - 1]
        # print "WIDTH"
        # print self.listUndoStatement

        self.clearSelection()

    def changeWidth2(self, paramLine, width):
        count = 0
        each = self.graph_items[int(paramLine) + self.axes_number]
        self.dic['lines'][int(paramLine)]['penwidth'] = int(width)
        each.setWidth(float(width))
        count = count + 1

    def AxisIncrease(self, axis):
        self.countUndo = 1
        self.currentIncrease = axis
        axis = axis - 1
        count = axis + (self.axes_number)
        if (axis == 0):
            diff = 0
            while (count < self.size_items):
                #ajuste o P1-X1Y1 do count
                p1 = self.graph_items[count].line()
                self.graph_items[count].setLine(p1.x1(), p1.y1() * 1.1 - diff,
                                                p1.x2(), p1.y2())
                if (p1.y1() * 1.1 > self.maximum[axis]):
                    self.maximum[axis] = p1.y1() * 1.1
                count = count + self.axes_number - 1

        elif(axis == self.axes_number - 1):
            diff = 0
            while (count < self.size_items):
                #ajuste o P1-X1Y1 do count
                p1 = self.graph_items[count - 1].line()
                self.graph_items[count - 1].setLine(p1.x1(), p1.y1() - diff,
                                                    p1.x2(), p1.y2() * 1.1)
                if (p1.y2() * 1.1 > self.maximum[axis - 1]):
                    self.maximum[axis - 1] = p1.y2() * 1.1
                count = count + self.axes_number - 1
        else:
            diff = 0
            while (count < self.size_items):
                #ajuste o P1-X1Y1 do count
                p1 = self.graph_items[count].line()
                self.graph_items[count].setLine(p1.x1(), p1.y1() * 1.1 - diff,
                                                p1.x2(), p1.y2())
                #ajuste o P2-X2Y2 do count - 1
                p2 = self.graph_items[count - 1].line()
                self.graph_items[count - 1].setLine(p2.x1(), p2.y1(), p2.x2(),
                                                    p2.y2() * 1.1 - diff)
                if (p2.y2() * 1.1 > self.maximum[axis]):
                    self.maximum[axis] = p2.y2() * 1.1
                count = count + self.axes_number - 1

        maximum = self.maximum[0]
        for each in range(1, self.axes_number):
            if (self.maximum[each] > maximum):
                maximum = self.maximum[each]

        for each in range(0, self.axes_number):
            paxis = self.graph_items[each].line()
            self.graph_items[each].setLine(paxis.x1(), paxis.y1(), paxis.x2(),
                                           maximum + 4)

    def hideList(self, hidelist):
        count = 0
        #group = self.selected
        self.groups.append(self.createItemGroup(hidelist))

        for each in hidelist:
            if (each.getId() % (self.axes_number - 1) == 0):
                self.ui.tableWidget.hideRow(
                    (each.getId() / (self.axes_number - 1)) - 2)
                self.dic['lines'][each.getId() - self.axes_number]['hidden'] = True

        self.clearSelection()
        self.groups[len(self.groups) - 1].hide()

    def showAllLines(self):
        count = 0

        for each in self.groups:
            for i in each.childItems():
                #self.countUndo = 1
                each.removeFromGroup(i)
                i.mySetSelected(False, False)
        self.clearSelection()
        for i in range(0, self.ui.tableWidget.rowCount()):
            self.ui.tableWidget.showRow(i)
        #self.countUndo = len(self.listUndoStatement) #- 1

    def showAllLines2(self, paramLine):
        count = 0
        for each in self.groups:
            for i in each.childItems():
                each.removeFromGroup(i)
                i.mySetSelected(False, False)
        self.clearSelection()
        for i in range(0, self.ui.tableWidget.rowCount()):
            self.ui.tableWidget.showRow(i)

    def removeGroup(self):
        count = 0
        for i in self.groups:
            self.destroyItemGroup(i)
            count = count + 1
        #del self.layers
        self.layers = {}
        self.ui.layersTreeWidget.clear()

#### Code for Layers Handle ########
    def doSelectLayer(self):
        self.clearSelection()
        if self.ui.layersTreeWidget.selectedItems() != []:
            treeItem = self.ui.layersTreeWidget.selectedItems()[0]
            selected = treeItem.text(2).__str__()
            if not self.layers[selected]['hidden'] and \
               not self.layers[selected]['blocked']:
                self.semaphore = True
                for each in self.layers[selected]['items']:
                        self.graph_items[each].setSelected(True)
        #pass

    def createLayer(self, name, index, line):
        if name == '':
            line.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
            line.setLayer('default')
            name = 'default'
        if (not self.layers.has_key(name)):
            index_list = [index]

            item = QtGui.QTreeWidgetItem()
            item.setText(2, QtCore.QString(name))
            item.setCheckState(1, QtCore.Qt.Checked)
            item.setCheckState(0, QtCore.Qt.Unchecked)
            #item.setSizeHint (0, QtCore.QSize(5, 5))
            self.ui.layersTreeWidget.insertTopLevelItem(0, item)
            self.ui.layersTreeWidget.header().resizeSection(0, 22)
            self.ui.layersTreeWidget.header().resizeSection(1, 25)
            self.layers[name] = {'items': [index], 'hidden': False,
                                 'blocked': False, 'group': None,
                                 'widget': item}

        else:
            self.layers[name]['items'].append(index)

        statement = "ADDLAYER %s %s %s" % (name, index, line)
        self.listUndoStatement.append(statement)
        #self.countUndo = self.countUndo + 1
        self.countUndo = len(self.listUndoStatement)

    def updateItem(self, name, item):
        item.setFlag(QtGui.QGraphicsItem.ItemIsSelectable,
                     not self.layers[name]['blocked'])
        if self.layers[name]['hidden']:
            item.hide()
        else:
            item.show()

    def selectLayer(self, treeItem, column):
        self.clearSelection()
        treeItem = self.ui.layersTreeWidget.selectedItems()[0]
        selected = treeItem.text(2).__str__()

        if column == 0:
            flag = self.layers[selected]['blocked']
            if (treeItem.checkState(0) == 2 and not flag):
                self.layers[selected]['blocked'] = True
                for each in self.layers[selected]['items']:
                    self.graph_items[each].setFlag(
                        QtGui.QGraphicsItem.ItemIsSelectable, False)

            elif (treeItem.checkState(0) == 0 and flag):
                self.layers[selected]['blocked'] = False
                for each in self.layers[selected]['items']:
                    self.graph_items[each].setFlag(
                        QtGui.QGraphicsItem.ItemIsSelectable, True)

        elif column == 1:
            flag = self.layers[selected]['hidden']
            layer = []
            for each in self.layers[selected]['items']:
                #layer.append(self.graph_items[each])
                self.graph_items[each].hide()
            #self.layers[selected]['group'] = self.createItemGroup(layer)
            if not flag and treeItem.checkState(1) == 0:
                for each in self.layers[selected]['items']:
                    if (each % (self.axes_number - 1) == 0):
                        self.ui.tableWidget.hideRow(
                            (each / (self.axes_number - 1)) - 2)
                    self.dic['lines'][each - (self.axes_number - 1) - 2]['hidden'] = True
                #self.layers[selected]['group'].hide()
                self.layers[selected]['hidden'] = True

            else:
                for i in self.layers[selected]['items']:
                    self.graph_items[i].show()
                for i in self.layers[selected]['items']:
                    if (i - self.axes_number) % self.axes_number == 0:
                        self.ui.tableWidget.showRow(
                            (i / (self.axes_number - 1)) - 2)
                self.layers[selected]['hidden'] = False

    def falseTrue(self, boolean):
        if boolean:
            return 2
        else:
            return 0

    def removeFromLayer(self, line, layer):
        self.layers[layer]['items'].remove(line)
        if self.layers[layer]['items'] == []:
            item = self.layers[layer]['widget']
            self.ui.layersTreeWidget.removeItemWidget(item, 0)
            self.ui.layersTreeWidget.removeItemWidget(item, 1)
            self.ui.layersTreeWidget.removeItemWidget(item, 2)
            del self.layers[layer]

    def addLayer(self):
        ok = False
        selected = self.selectedItems()
        self.clearSelection()

        newLayerName = QtGui.QInputDialog.getText(
            self.ui.layersTreeWidget,
            "Layer Name",
            "Input the new layer name:\n(existant layer to append)",
            QtGui.QLineEdit.Normal,
            "newLayer",
            QtCore.Qt.Widget)

        if newLayerName[1]:
            for each in selected:
                self.removeFromLayer(each.getId(), each.getLayer())
                line = self.dic['lines'][each.getId() - self.axes_number - 1]
                line['layer'] = newLayerName[0].__str__().__str__()
                self.createLayer(newLayerName[0].__str__().__str__(),
                                 each.getId(), line)
                self.updateItem(newLayerName[0].__str__().__str__(), each)
                each.setLayer(newLayerName[0].__str__().__str__())
        else:
            pass

    def removeLayer(self):
        current = self.ui.layersTreeWidget.currentItem()
        if current != None and current.text(2).__str__() != 'default':
            dic = self.layers[current.text(2).__str__()]
            print dic
            self.ui.layersTreeWidget.removeItemWidget(current, 0)
            self.ui.layersTreeWidget.removeItemWidget(current, 1)
            self.ui.layersTreeWidget.removeItemWidget(current, 2)

            if self.layers.has_key('default'):
                current.setCheckState(
                    0, self.falseTrue(self.layers['default']['blocked'])
                )
                current.setCheckState(
                    1, self.falseTrue(not self.layers['default']['hidden'])
                )
                for each in dic['items']:
                    self.layers['default']['items'].append(each)
                self.layers['default']['items'].sort()
            else:
                for each in dic['items']:
                    self.createLayer('default', each, self.graph_items[each])
                self.layers['default']['items'].sort()
            del self.layers[current.text(2).__str__()]

        elif current == None:
            QtGui.QMessageBox.information(
                self.ui.layersTreeWidget,
                self.trUtf8("Layers"),
                self.trUtf8("Select one layer to remove!")
            )
        else:
            QtGui.QMessageBox.information(
                self.ui.layersTreeWidget,
                self.trUtf8("Layers"),
                self.trUtf8("Cannot remove default layer!")
            )

    def removeAllLayers(self):
        self.ui.layersTreeWidget.clear()
        #print self.layers
        self.layers.clear()

    def removeLayer2(self, name):
        current = self.ui.layersTreeWidget.findItems(name)[2]
        if current != None and current.text(2).__str__() != 'default':
            dic = self.layers[current.text(2).__str__()]
            self.ui.layersTreeWidget.removeItemWidget(current, 0)
            self.ui.layersTreeWidget.removeItemWidget(current, 1)
            self.ui.layersTreeWidget.removeItemWidget(current, 2)
            if self.layers.has_key('default'):
                current.setCheckState(
                    0, self.falseTrue(self.layers['default']['blocked'])
                )
                current.setCheckState(
                    1, self.falseTrue(not self.layers['default']['hidden'])
                )
                for each in dic['items']:
                    self.layers['default']['items'].append(each)
                self.layers['default']['items'].sort()
            else:
                for each in dic['items']:
                    self.createLayer('default', each, self.graph_items[each])
                self.layers['default']['items'].sort()

        elif current == None:
            QtGui.QMessageBox.information(
                self.ui.layersTreeWidget,
                self.trUtf8("Layers"),
                self.trUtf8("Select one layer to remove!")
            )
        else:
            QtGui.QMessageBox.information(
                self.ui.layersTreeWidget,
                self.trUtf8("Layers"),
                self.trUtf8("Cannot remove default layer!")
            )
