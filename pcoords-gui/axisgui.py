from PyQt4 import QtCore, QtGui

import selection, defaults


#class AxisName(QtGui.QWidget):
class AxisName(QtGui.QComboBox):

    def __init__(self, ui, parent=None):
        QtGui.QWidget.__init__(self, parent)
                #self.combo = QtGui.QComboBox(parent)
        #self.combo = combo
        #ui.horizontalLayout.addWidget(self)
                #ui.horizontalLayout.addItem(combo)
        #self.connect(self.combo, QtCore.SIGNAL('currentIndexChanged(int)'),
        #        self.indexChanged)

    def setItemName(self, label, id): #Set the item name in Combo Box
        itemlabel = ""
        if label:
            itemlabel = label
        else:
            itemlabel = "axis%d" % id
        self.addItem(itemlabel)
        return itemlabel

    def indexChanged(self, id):
        print "Change axis id: %d" % id

    #def setCurrentIndex(self, i):
    #    self.setCurrentIndex(i)

    def getCurrentIndex(self):
        return self.currentIndex()


class AxisButton(QtGui.QWidget):
    #This Class is responsable for button Change, located at rigth side of comboboxes.
    #This Button call SetAxesOrder in the engine, and after this call update lines to redraw the graph.
    #It needs to handle lines/engine/axesDict
    #The axes dict translate the axis name in combobox to axis name in image dict.

    def __init__(self, ui, comboList, axesDict, scene, parent=None ):
        #Class Constructor
        QtGui.QWidget.__init__(self, parent)
        self.button = QtGui.QPushButton() #Hold the button object
        self.button.setText("Change") #Label of button
        self.button.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed) #Block button to no expand when user resize window
        self.button.setGeometry(21, 21, 21, 21) #Size of button

        self.comboBoxes = comboList #Hold comboList, this object contains all of comboboxes in gui. The button need this to get axis names.
        self.currentComboBoxes = []
        for i in self.comboBoxes:
            self.currentComboBoxes.append(i.currentText().__str__())

        self.dicAxes = axesDict #H lds the correspondent axis name on image file for all names in comboBoxes
        self.ui = ui
        self.scene = scene
        ui.horizontalLayout.addWidget(self.button) #Put the button in the same layout where are located the combos
        self.connect(self.button, QtCore.SIGNAL('pressed()'), self.buttonPressed) #Add function to respond an signal.
        self.semaphore = False

    def buttonPressed(self):
        #self.lines.removeLines() #Clean the lines of scene, the axes is not deleted
        name_list = [] #This list is responsable for hold names of axesa
        label = "CHANGE"
        for i in self.currentComboBoxes:
            label = label + " " + i
#        print label
        #self.scene.countUndo = self.scene.countUndo + 1
        #self.scene.listUndoStatement.append(label)
        #label2 = "CHANGE"
        #print "CHANGE AXIS"

            #for i in range(len(self.scene.listUndoStatement) - 1, self.scene.countUndo - 1, -1):
            #    del self.scene.listUndoStatement[i]

        for each in self.comboBoxes:
            name_list.append(self.dicAxes[each.currentText().__str__()]) #Get the name of axis in comboBox,
            label = label + " %s " % (each.currentText().__str__())
        #self.scene.listUndoStatement.append(label)
        #print self.scene.listUndoStatement
            #translate is for engine name and store on list
        self.picviz.setAxesOrder(self.image, name_list) #Call engine for change axis
        self.lines.clean()
        self.scene.removeGroup()
        self.lines.addLines(len(self.image['lines']) / (len(self.image['axeslist']) - 1))
        #self.lines.doSelectable()
        self.lines.update_lines_view(self.horizontalSlider.value())
        self.currentComboBoxes = []
        for i in self.comboBoxes:
            self.currentComboBoxes.append(i.currentText().__str__())
        self.scene.countUndo = len(self.scene.listUndoStatement) #- 1

    def buttonPressed2(self, listAxis):
        #self.lines.removeLines() #Clean the lines of scene, the axes is not deleted
        name_list = [] #This list is responsable for hold names of axesa
        #label = "CHANGE"
        #for i in range(len(listAxis) - 1):
        j = 0
        for i in self.comboBoxes:
            index = i.findText(listAxis[j])
            i.setCurrentIndex(index)
            j = j + 1

        #print label
        for each in self.comboBoxes:
            name_list.append(self.dicAxes[each.currentText().__str__()]) #Get the name of axis in comboBox,
            #translate is for engine name and store on list
        self.picviz.setAxesOrder(self.image, name_list) #Call engine for change axis
        self.lines.clean()
        self.scene.removeGroup()
        self.lines.addLines(len(self.image['lines']) / (len(self.image['axeslist']) - 1))
        #self.lines.doSelectable()
        self.lines.update_lines_view(self.horizontalSlider.value())
        self.currentComboBoxes = []
        for i in self.comboBoxes:
            self.currentComboBoxes.append(i.currentText().__str__())

    def updateAfterRemoveDuplicated(self):
        #self.lines.removeLines() #Clean the lines of scene, the axes is not deleted
        #name_list = [] #This list is responsable for hold names of axes
        #for each in self.comboBoxes:
        #    name_list.append(self.dicAxes[each.currentText().__str__()]) #Get the name of axis in comboBox,
            #translate is for engine name and store on list
        #self.picviz.setAxesOrder(self.image, name_list) #Call engine for change axis
        self.lines.clean()
        self.scene.removeGroup()
        self.lines.addLines(len(self.image['lines']) / (len(self.image['axeslist']) - 1))
        #self.lines.doSelectable()
        self.lines.update_lines_view(self.horizontalSlider.value())

    def setLines(self, scene_lines, line_number): #Presenting Lines
        self.lines = scene_lines
        self.linenb = line_number

    def setImage(self, scene_image): #Presenting image file
        self.image = scene_image

    def setCurrentEngine(self, engine): #Presenting current import
        self.picviz = engine

    def setSlider(self, slider):
        self.horizontalSlider = slider

    def Close(self):
        self.ui.horizontalLayout.removeWidget(self.button) #Put the button in the same layout where are located the combos
        self.button.close()
        self.close()


def addAxes(image, scene, lines, axes_number, ui):
    pen = QtGui.QPen()
    pen.setColor(QtCore.Qt.black)

    i = 0
    while i < axes_number:
        scene.addLine(i * defaults.axiswidth, 0, i * defaults.axiswidth, image['height'], pen) #Draw axes lines
    # Removed for 0.1 release. Be back on trunk soon
        #item = selection.SelectionItem(image, scene, lines, i * defaults.axiswidth , 0)
            #scene.addItem(item)
        i = i + 1
