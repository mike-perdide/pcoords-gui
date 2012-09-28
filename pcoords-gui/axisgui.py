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
    """ This Class is responsible for button Change

    This button is located at the right side of the comboboxes. It calls
    SetAxesOrder in the engine, and after this call update lines to redraw the
    graph.

    It needs to handle lines/engine/axesDict. The axes dict translates the axis
    name in combobox to axis name in image dict.

    """

    def __init__(self, ui, comboList, axesDict, scene, parent=None ):
        #Class Constructor
        QtGui.QWidget.__init__(self, parent)
        self.button = QtGui.QPushButton() #Hold the button object
        self.button.setText("Change") #Label of button

        # Block button to no expand when user resize window
        self.button.setSizePolicy(
            QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Fixed)

        self.button.setGeometry(21, 21, 21, 21) #Size of button

        # Hold comboList, this object contains all of comboboxes in gui. The
        # button needs this to get the axis names.
        self.comboBoxes = comboList

        self.currentComboBoxes = []
        for i in self.comboBoxes:
            self.currentComboBoxes.append(i.currentText().__str__())

        # H lds the correspondent axis name on image file for all names in
        # comboBoxes
        self.dicAxes = axesDict
        self.ui = ui
        self.scene = scene

        # Put the button in the same layout where the combos are located
        ui.horizontalLayout.addWidget(self.button)

        # Add function to respond to signal.
        self.connect(
            self.button,
            QtCore.SIGNAL('pressed()'),
            self.buttonPressed)

        self.semaphore = False

    def buttonPressed(self):
        name_list = [] #This list is responsable for hold names of axesa
        label = "CHANGE"
        for i in self.currentComboBoxes:
            label = label + " " + i
#        print label
        #self.scene.countUndo = self.scene.countUndo + 1
        #self.scene.listUndoStatement.append(label)
        #label2 = "CHANGE"
        #print "CHANGE AXIS"

        for each in self.comboBoxes:
            # Get the name of axis in comboBox
            name_list.append(self.dicAxes[each.currentText().__str__()])
            label = label + " %s " % (each.currentText().__str__())
        #self.scene.listUndoStatement.append(label)
        #print self.scene.listUndoStatement
            #translate is for engine name and store on list

        # Call engine for change axis
        self.picviz.setAxesOrder(self.image, name_list)
        self.lines.clean()
        self.scene.removeGroup()

        self.lines.addLines(
            len(self.image['lines']) / (len(self.image['axeslist']) - 1)
        )

        #self.lines.doSelectable()
        self.lines.update_lines_view(self.horizontalSlider.value())
        self.currentComboBoxes = []
        for i in self.comboBoxes:
            self.currentComboBoxes.append(i.currentText().__str__())
        self.scene.countUndo = len(self.scene.listUndoStatement) #- 1

    def buttonPressed2(self, listAxis):
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
            # Get the name of axis in comboBox,
            name_list.append(self.dicAxes[each.currentText().__str__()])
            #translate is for engine name and store on list

        # Call engine to change axis order
        self.picviz.setAxesOrder(self.image, name_list)

        self.lines.clean()
        self.scene.removeGroup()
        self.lines.addLines(
            len(self.image['lines']) / (len(self.image['axeslist']) - 1)
        )

        #self.lines.doSelectable()
        self.lines.update_lines_view(self.horizontalSlider.value())
        self.currentComboBoxes = []
        for i in self.comboBoxes:
            self.currentComboBoxes.append(i.currentText().__str__())

    def updateAfterRemoveDuplicated(self):
        # Clean the lines of scene, the axes is not deleted
        #self.lines.removeLines()
        #name_list = [] #This list is responsable for hold names of axes
        #for each in self.comboBoxes:
        #    # Get the name of axis in comboBox,
        #    # translate is for engine name and store on list
        #    name_list.append(self.dicAxes[each.currentText().__str__()])
        # Call engine to change axis order
        #self.picviz.setAxesOrder(self.image, name_list)

        self.lines.clean()
        self.scene.removeGroup()
        self.lines.addLines(
            len(self.image['lines']) / (len(self.image['axeslist']) - 1)
        )

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
        # Put the button in the same layout where are located the combos
        self.ui.horizontalLayout.removeWidget(self.button)
        self.button.close()
        self.close()


def addAxes(image, scene, lines, axes_number, ui):
    pen = QtGui.QPen()
    pen.setColor(QtCore.Qt.black)

    i = 0
    while i < axes_number:
        # Draw axes lines
        scene.addLine(
            i * defaults.axiswidth, 0,
            i * defaults.axiswidth, image['height'],
            pen)

    # Removed for 0.1 release. Be back on trunk soon
        #item = selection.SelectionItem(
        #    image,
        #    scene,
        #    lines,
        #    i * defaults.axiswidth,
        #    0)
        #scene.addItem(item)
        i = i + 1
