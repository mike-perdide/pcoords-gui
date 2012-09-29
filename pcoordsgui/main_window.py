#!/usr/bin/env python
#
######################
# Frontend for Pcoords
######################
# (C) 2008 Sebastien Tricaud
#     2009 Victor Amaducci
#     2009 Gabriel Cavalcante
#     2012 Julien Miotte

import sys

# QT
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMainWindow

# Pcoords
import pcoords

# UI
from pcoordsgui import axisgui, export
from pcoordsgui import line_graphics_item
from pcoordsgui.pcoords_graphics_scene import myScene
from pcoordsgui.build_graphic_dialog import Buildpanel
from pcoordsgui.set_width_dialog import buildWidthPanel
from pcoordsgui.select_axis_id_dialog import buildSelectIdPanel
from pcoordsgui.about_dialog import buildAboutPanel

from pcoordsgui.main_window_ui import Ui_MainWindow

# check for psyco
try:
    import psyco
    psyco.full()
except ImportError:
    print 'Running without psyco (http://psyco.sourceforge.net/).'


class MainWindow(QMainWindow):
    """Describes the pcoords main window."""

    def __init__(self, pcvfile=None, filters=None, parent=None):
        """Initialization method."""
        QMainWindow.__init__(self, parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.scene = QtGui.QGraphicsScene()
        self.comboboxes = {}
        self.image = 0
        self.comboList = []
        self.buttonChange = []
        self.axes_number = 0
        self.filters = None

        if pcvfile:
            self.setPcvFile(pcvfile, filters=filters)
        else:
            self.openPcvFile()

        self.exporter = export.ExportGraph()
        self.connectSignals()

        self.setWindowTitle("Pcoords Frontend [%s]" % pcvfile)
        self.show()

    def setPcvFile(self, pcvfile, filters=None):
        self.image = pcoords.Image(str(pcvfile), filters)

        if filters:
            self.filters = filters

        self.paint_ImageView()

    def connectSignals(self):
        """Connect the objects to the slots."""
        ui = self.ui

        ui.actionSave.triggered.connect(self.exportToPGDL)
        ui.actionExport_png.triggered.connect(self.exportToPNG)
        ui.action_Build.triggered.connect(self.Buildgraphic)
        ui.action_Open.triggered.connect(self.openPcvFile)
        ui.action_Quit.triggered.connect(self.close)

        ui.zoomButtonPlus.clicked.connect(self.plusZoom)
        ui.zoomButtonLess.clicked.connect(self.plusZoom)

        ui.axisIncreaseButton.clicked.connect(self.increaseAxisDialog)
        ui.setWidthButton.clicked.connect(self.changeWidthDialog)
        ui.QCheckAntiAliasing.clicked.connect(self.antiAliasing)

        ui.actionUndo.triggered.connect(self.undoProcess)
        ui.actionRedo.triggered.connect(self.redoProcess)

        ui.action_About.triggered.connect(self.showCredits)

        ui.actionZoomin.triggered.connect(self.plusZoom)
        ui.actionZoomout.triggered.connect(self.lessZoom)

        ui.actionLine_width.triggered.connect(self.changeWidthDialog)

        ui.actionViewLayers.toggled.connect(self.viewLayers)
        ui.actionViewTable.toggled.connect(self.viewTable)

    def Buildgraphic(self):
        """Shows the buildpanel."""
        test = Buildpanel(self)
        test.show()

    def openPcvFile(self):
        """Opens the PCV file with a QFileDialog."""
        self.pcvfile = QtGui.QFileDialog.getOpenFileName(
            None,
            "Open Pcoords graph", "",
            "Pcoords Files (*.pgdl *.pcv)")
        self.image = pcoords.Image(str(self.pcvfile), self.filters)
        self.destroyComboBoxes()
        self.paint_ImageView()

    def antiAliasing(self):
        """Activate or deactivate the anti-aliasing."""
        graphics_view = self.ui.graphicsView
        is_checked = self.ui.QCheckAntiAliasing.isChecked()
        graphics_view.setRenderHint(QtGui.QPainter.Antialiasing, is_checked)

    def destroyComboBoxes(self):
        for each in self.comboList:
            each.close()
        for each in self.buttonChange:
            each.Close()

    def showCredits(self):
        """Show the credits in the about dialog."""
        panel = buildAboutPanel(pcoords.Version(), self)
        panel.show()
        del panel

    def viewLayers(self, checked):
        """Display the layers box."""
        if checked:
            self.ui.LayersBox.show()
        else:
            self.ui.LayersBox.hide()

    def viewTable(self, checked):
        if checked:
            self.ui.tableWidget.show()
        else:
            self.ui.tableWidget.hide()

    def sortLayers(self):
        self.ui.layersTreeWidget.sortItems(2, 0)

    def redoProcess(self):
        try:
            if self.scene.countUndo < 0:
                QtGui.QMessageBox.information(
                    self, self.trUtf8("Redo"),
                    self.trUtf8("There isn't Statement to Redo!")
                )
            else:
                statementList = self.scene.listUndoStatement
                cmd = str(statementList[self.scene.countUndo])
                strList = cmd.split()
                command = ''.join(strList[:1])

                if command == "COLOR":
                    num = (len(strList) - 1) / 2
                    for i in range(1, len(strList) - 1, 2):
                        self.scene.brushSelection2(strList[i], strList[i + 1],
                                                   num)
                    self.scene.countUndo = self.scene.countUndo + 1

                elif command == "SHOWALL":
                    num_selected_lines = int(''.join(strList[2:]))
                    for i in range(num_selected_lines):
                        for j in range(self.scene.axes_number - 1):
                            self.scene.hideSelected2(''.join(strList[1:2]))
                            self.scene.countUndo = self.scene.countUndo - 1
                            cmd = str(statementList[len(statementList)
                                                    - self.scene.countUndo])
                            strList = cmd.split()

                elif command == "HIDE":
                    num_selected_lines = len(strList)

                    for i in range(1, num_selected_lines, 1):
                        self.scene.hideSelected2(strList[i])

                    self.scene.countUndo = self.scene.countUndo + 1

                elif command == "ZOOM+":
                    self.plusZoom2()
                    self.scene.countUndo = self.scene.countUndo + 1

                elif command == "ZOOM-":
                    self.lessZoom2()
                    self.scene.countUndo = self.scene.countUndo + 1

                elif command == "CHANGE":
                    listParam = []
                    num_selected_lines = len(strList)

                    for i in range(1, num_selected_lines, 3):
                        listParam.append(strList[i])
                        listParam.append(strList[i + 1])
                        listParam.append(strList[i + 2])
                        self.axisButton.buttonPressed2(listParam)
                        listParam = []

                    self.scene.countUndo = self.scene.countUndo + 1

                elif command == "WIDTH":
                    num_selected_lines = len(strList) - 1
                    for i in range(1, num_selected_lines, 3):
                        self.scene.changeWidth2(strList[i], strList[i + 1])
                    self.scene.countUndo = self.scene.countUndo + 1

                elif command == "ADDLAYER":
                    self.scene.addLayer(strList[1], strList[2], strList[3])
                    self.scene.countUndo = self.scene.countUndo + 1

                elif command == "REMOVELAYER":
                    self.scene.removeLayer2(strList[1])
                    self.scene.countUndo = self.scene.countUndo + 1

        except:
            QtGui.QMessageBox.information(
                self, self.trUtf8("Redo"),
                self.trUtf8("There isn't Statement to Redo!"))
            if self.scene.countUndo > (len(statementList) - 1):
                self.scene.countUndo = len(statementList) - 1

    def undoProcess(self):
        try:
            if self.scene.countUndo < 0:
                QtGui.QMessageBox.information(
                    self, self.trUtf8("Undo"),
                    self.trUtf8("There isn't Statement to Undo!"))
                self.scene.countUndo = 0

            else:
                statementList = self.scene.listUndoStatement
                cmd = str(statementList[self.scene.countUndo - 1])
                strList = cmd.split()
                command = ''.join(strList[:1])
                if command == "COLOR":
                    num = (len(strList) - 1) / 2
                    for i in range(len(strList) - 1, 1, -2):
                        self.scene.brushSelection2(strList[i - 1],
                                                   strList[i], num)
                    self.scene.countUndo = self.scene.countUndo - 1

                elif command == "SHOWALL":
                    num_selected_lines = int(''.join(strList[2:]))
                    for i in range(num_selected_lines):
                        for j in range(self.scene.axes_number - 1):
                            self.scene.hideSelected2(''.join(strList[1:2]))
                            self.scene.countUndo = self.scene.countUndo + 1
                            cmd = str(statementList[len(statementList)
                                                    - self.scene.countUndo])
                            strList = cmd.split()
                    self.scene.countUndo = self.scene.countUndo + 1

                elif command == "HIDE":
                    num_selected_lines = (len(strList) - 1)
                    for i in range(num_selected_lines, 0, -1):
                        self.scene.showAllLines2(strList[i])
                    self.scene.countUndo = self.scene.countUndo - 1

                elif command == "ZOOM+":
                    self.lessZoom2()
                    self.scene.countUndo = self.scene.countUndo - 1

                elif command == "ZOOM-":
                    self.plusZoom2()
                    self.scene.countUndo = self.scene.countUndo - 1

                elif command == "CHANGE":
                    listParam = []
                    num_selected_lines = len(strList)

                    for i in range(num_selected_lines - 1, 0, -3):
                        listParam.append(strList[i - 2])
                        listParam.append(strList[i - 1])
                        listParam.append(strList[i])
                        self.axisButton.buttonPressed2(listParam)
                        listParam = []
                    self.scene.countUndo = self.scene.countUndo - 1

                elif command == "WIDTH":
                    num_selected_lines = len(strList) - 1
                    for i in range(num_selected_lines, 0, -3):
                        self.scene.changeWidth2(strList[i - 2],
                                                strList[i - 1])
                    self.scene.countUndo = self.scene.countUndo - 1

                elif command == "ADDLAYER":
                    self.scene.removeLayer2(strList[1])
                    self.scene.countUndo = self.scene.countUndo - 1

                elif command == "REMOVELAYER":
                    i = 1
                    while not strList[i] and not strList[i]:
                        i += 1
                    for j in range(i):
                        self.scene.createLayer(
                            strList[1], strList[2 + j],
                            strList[2 + (i - 1)])
                    self.scene.countUndo = self.scene.countUndo - 1

        except:
            QtGui.QMessageBox.information(
                self, self.trUtf8("Undo"),
                self.trUtf8("There isn't Statement to Undo!"))

    def changeWidthDialog(self):
        panel = buildWidthPanel(self)
        panel.show()
        del panel

    def increaseAxisDialog(self):
        panel = buildSelectIdPanel(self)
        panel.show()
        del panel

    def plusZoom(self):
        self.ui.graphicsView.scale(1.15, 1.15)
        self.line.decreaseWidth()

        for i in range(len(self.scene.listUndoStatement) - 1,
                       self.scene.countUndo - 1, -1):
            del self.scene.listUndoStatement[i]

        self.scene.listUndoStatement.append("ZOOM+")
        self.scene.countUndo = len(self.scene.listUndoStatement)

    def plusZoom2(self):
        self.ui.graphicsView.scale(1.15, 1.15)
        self.line.decreaseWidth()

    def lessZoom(self):
        self.ui.graphicsView.scale(1 / 1.15, 1 / 1.15)
        self.line.increaseWidth()

        for i in range(len(self.scene.listUndoStatement) - 1,
                       self.scene.countUndo - 1, -1):
            del self.scene.listUndoStatement[i]

        self.scene.listUndoStatement.append("ZOOM-")
        self.scene.countUndo = len(self.scene.listUndoStatement)

    def lessZoom2(self):
        self.ui.graphicsView.scale(1 / 1.15, 1 / 1.15)
        self.line.increaseWidth()

    def empty_ImageView(self):
        tableHeader = []

        self.ui.tableWidget.setHorizontalHeaderLabels(tableHeader)
        self.ui.tableWidget.horizontalHeader().setResizeMode(
            QtGui.QListView.Adjust, QtGui.QHeaderView.Interactive)
        self.ui.tableWidget.verticalHeader().hide()
        self.ui.tableWidget.setShowGrid(True)
        self.ui.tableWidget.setSelectionBehavior(
            QtGui.QAbstractItemView.SelectRows)

    def exportToPGDL(self):
        self.exporter.asPGDL(self.image)

    def exportToPNG(self):
        self.exporter.asPNG(self.scene)

    def paint_ImageView(self):
        self.scene = myScene(self.ui.graphicsView)
        self.scene.setBackgroundBrush(QtCore.Qt.white)
        self.scene.getUi(self.ui, self.image)
        self.ui.graphicsView.setScene(self.scene)
        self.ui.graphicsView.setDragMode(2)

        ui = self.ui
        ui.hideSelectionButton.clicked.connect(self.scene.hideSelected)
        ui.brushButton.clicked.connect(self.scene.brushSelection)
        ui.showOnlyButton.clicked.connect(self.scene.hideNotSelected)
        ui.showAllButton.clicked.connect(self.scene.showAllLines)

        ui.actionHide.triggered.connect(self.scene.hideSelected)
        ui.actionBrush.triggered.connect(self.scene.brushSelection)
        ui.actionShow_only.triggered.connect(self.scene.hideNotSelected)
        ui.actionShow_all.triggered.connect(self.scene.showAllLines)

        #Layer Buttons
        ui.layersTreeWidget.itemClicked.connect(self.scene.selectLayer)
        ui.sortLayerButton.clicked.connect(self.sortLayers)
        ui.removeLayerButton.clicked.connect(self.scene.removeLayer)
        ui.addLayerButton.clicked.connect(self.scene.addLayer)
        ui.selectLayerButton.clicked.connect(self.scene.doSelectLayer)

        self.axes_number = len(self.image['axeslist'])
        i = 0
        tableHeader = []
        comboList = []
        # Handler of engine/ComboBox axis name translate
        axesDict = {}

        # Flag for not duplicate lines!
        dictFull = False

        while i < self.axes_number:
            combo = axisgui.AxisName(self.ui, self)
            self.ui.horizontalLayout.addWidget(combo)
            combo.show()
            temp_index = 0
            for axis in self.image['axeslist']:
                #itemlabel = "teste"
                itemlabel = combo.setItemName(
                    self.image['axes'][axis]['label'],
                    self.image['axes'][axis]['id'])
                # set the combo names
                if not dictFull:
                    if (self.image['axes'][axis]['label']):
                        axesDict[self.image['axes'][axis]['label']] = axis
                        #Add translate for dict if it have label
                    else:
                        # Add translate if it not have label
                        axesDict['axis%d' % temp_index] = axis
                if i == 0:
                    tableHeader.append(itemlabel)
                    self.ui.tableWidget.insertColumn(
                                            self.ui.tableWidget.columnCount())
                temp_index = temp_index + 1

            # Set the flag in first iteration
            dictFull = True
            combo.setCurrentIndex(i)
            comboList.append(combo)
            i = i + 1

        # Add a button in Horizontal Layout
        self.axisButton = axisgui.AxisButton(self.ui, comboList, axesDict,
                                             self.scene, self)
        self.scene.getButton(self.axisButton)
        self.ui.horizontalSlider.setPageStep(1)
        self.ui.horizontalSlider.setMinimum(0)
        linenb = 0
        self.comboList = comboList
        for self.line in self.image['lines']:
            linenb = linenb + 1
        self.ui.horizontalSlider.setMaximum(linenb / (self.axes_number - 1))
        self.ui.horizontalSlider.setValue(linenb / (self.axes_number - 1))

        axisgui.addAxes(self.image, self.scene, self.line, self.axes_number,
                        self.ui)

        self.ui.tableWidget.setHorizontalHeaderLabels(tableHeader)

        self.ui.tableWidget.horizontalHeader().setResizeMode(
            QtGui.QListView.Adjust, QtGui.QHeaderView.Interactive)

        self.ui.tableWidget.verticalHeader().hide()
        self.ui.tableWidget.setShowGrid(True)
        self.ui.tableWidget.setSelectionBehavior(
                                            QtGui.QAbstractItemView.SelectRows)

        self.line = line_graphics_item.Line(self.scene, self.image,
                                            self.axes_number, self.ui,
                                            self.comboList)
        self.line.addLines(linenb)

        self.connect(self.ui.horizontalSlider,
                     QtCore.SIGNAL('valueChanged(int)'),
                     self.line.update_lines_view)
        self.axisButton.setLines(self.line, linenb)
        self.axisButton.setImage(self.image)
        self.axisButton.setCurrentEngine(pcoords)
        self.axisButton.setSlider(self.ui.horizontalSlider)
        self.buttonChange.append(self.axisButton)

    def closeEvent(self, event):
        self.scene.clearSelection()
        event.accept()
