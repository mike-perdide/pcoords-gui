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


class AxisButton(QtGui.QWidget):
    """ This Class is responsible for button Change

    This button is located at the right side of the comboboxes. It calls
    SetAxesOrder in the engine, and after this call update lines to redraw the
    graph.

    It needs to handle lines/engine/axesDict. The axes dict translates the axis
    name in combobox to axis name in image dict.

    """

    def __init__(self, ui, comboList, axesDict, scene, parent=None):
        #Class Constructor
        QtGui.QWidget.__init__(self, parent)

        # Hold the button object
        self.button = QtGui.QPushButton()

        # Label of button
        self.button.setText("Change")

        # Block button to no expand when user resize window
        self.button.setSizePolicy(
            QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Fixed)

        # Size of button
        self.button.setGeometry(21, 21, 21, 21)

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
        # This list is responsible for holding the names of the axes
        name_list = []
        label = "CHANGE"
        for i in self.currentComboBoxes:
            label = label + " " + i

        for each in self.comboBoxes:
            # Get the name of axis in comboBox
            name_list.append(self.dicAxes[each.currentText().__str__()])
            label = label + " %s " % (each.currentText().__str__())

        # Call engine for change axis
        self.pcoords.setAxesOrder(self.image, name_list)
        self.lines.clean()
        self.scene.removeGroup()

        self.lines.addLines(
            len(self.image['lines']) / (len(self.image['axeslist']) - 1)
        )

        self.lines.update_lines_view(self.horizontalSlider.value())
        self.currentComboBoxes = []
        for i in self.comboBoxes:
            self.currentComboBoxes.append(i.currentText().__str__())
        self.scene.countUndo = len(self.scene.listUndoStatement)

    def buttonPressed2(self, listAxis):
        # This list is responsible for holding the names of the axes
        name_list = []
        j = 0
        for i in self.comboBoxes:
            index = i.findText(listAxis[j])
            i.setCurrentIndex(index)
            j = j + 1

        for each in self.comboBoxes:
            # Get the name of axis in comboBox,
            name_list.append(self.dicAxes[each.currentText().__str__()])
            #translate is for engine name and store on list

        # Call engine to change axis order
        self.pcoords.setAxesOrder(self.image, name_list)

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
        self.lines.clean()
        self.scene.removeGroup()
        self.lines.addLines(
            len(self.image['lines']) / (len(self.image['axeslist']) - 1)
        )

        #self.lines.doSelectable()
        self.lines.update_lines_view(self.horizontalSlider.value())

    def setLines(self, scene_lines, line_number):
        """Presenting Lines"""
        self.lines = scene_lines
        self.linenb = line_number

    def setImage(self, scene_image):
        """Presenting image file"""
        self.image = scene_image

    def setCurrentEngine(self, engine):
        """Presenting current import"""
        self.pcoords = engine

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
        scene.addLine(i * defaults.axiswidth, 0,
                      i * defaults.axiswidth, image['height'],
                      pen)

        i = i + 1
