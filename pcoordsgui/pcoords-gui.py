#!/usr/bin/env python
#
######################
# Frontend for Pcoords
######################
# (C) 2008 Sebastien Tricaud
#     2009 Victor Amaducci
#     2009 Gabriel Cavalcante

# Python libs
import sys
import string

# QT
from PyQt4 import QtCore, QtGui


# Pcoords
import pcoords

# UI
from pcoordsgui import axisgui, export, lines, UiPcoords
from pcoordsgui.buildgraphicgui import Buildpanel
from pcoordsgui.UiPcoords import Ui_MainWindow
from pcoordsgui.myScene import myScene
from pcoordsgui.setWidthDialog import buildWidthPanel
from pcoordsgui.selectAxisIdDialog import buildSelectIdPanel
from pcoordsgui.aboutDialog import buildAboutPanel
#class Timeout:
#    def __init__(self, last):
#        self.last_timeout = last
#
#    def canActivate(self, time):
#        if int(time) - self.last_timeout > 1:
#            print "update: %d-%d" % (int(time), self.last_timeout)
#        self.last_timeout = int(time)
#
#    def getTimeout(self):
#        return self.last_timeout
#
#    def updateTimeout(self):
#        self.last_timeout = int(time.time())

# check for psyco
try:
    import psyco
    psyco.full()
except ImportError:
    print 'Running without psyco (http://psyco.sourceforge.net/).'


class PcoordsApp(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = UiPcoords.Ui_MainWindow()
        self.ui.setupUi(self)
        #self = QtGui.QMainWindow(self)
        self.scene = QtGui.QGraphicsScene()
        self.comboboxes = {}
        self.image = 0
        self.comboList = []
        self.buttonChange = []
        self.exporter = export.ExportGraph()
        #addLines(window, image)

    def ComboIndexChange(widget):
        pass
#    print "foo"

    def Buildgraphic(self):
        test = Buildpanel(self)
        test.show()
        print '+Buildgraphic'

    def init_view(self, pcvFileBuilded):
        self.axes_number = 0
        self.filter = None
        if len(sys.argv) < 2:
            self.pcvfile = "New.pcv"
            pass
        else:
            self.pcvfile = sys.argv[1]
            if len(sys.argv) > 2:
                self.filtertable = sys.argv[2:]
                self.filter = string.join(self.filtertable, " ")
            self.image = pcoords.Image(str(self.pcvfile), self.filter)

    def openPcvFile(self):
        self.pcvfile = QtGui.QFileDialog.getOpenFileName(
            None,
            "Open Pcoords graph", "",
            "Pcoords Files (*.pgdl *.pcv)")
        self.image = pcoords.Image(str(self.pcvfile), self.filter)
        #print self.image
        self.destroyComboBoxes()
        self.paint_ImageView()

    def antiAliasing(self):
        if (self.ui.QCheckAntiAliasing.isChecked()):
            self.ui.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing,
                                               True)
        else:
            self.ui.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing,
                                               False)

    def destroyComboBoxes(self):
        for each in self.comboList:
            each.close()
        for each in self.buttonChange:
            each.Close()
        #print "Image"
        #print self.image
        #if self.image:
        #    del self.image

    def showCredits(self):
        panel = buildAboutPanel(pcoords.Version(), self)
        panel.show()
        del panel

    def create_window_after_init_view(self):
        #pcoords.Debug()
        self.ui.setupUi(self)
        self.setWindowTitle("Pcoords Frontend [%s]" % (self.pcvfile))
        self.show()

        #self.matrix = QtGui.QMatrix() #Natrix to apply Zoom on GraphicsView

        #scene.setSceneRect(0, 0, 875, 500)
        self.connect(self.ui.actionSave, QtCore.SIGNAL('triggered()'),
                     self.exportToPGDL)
        self.connect(self.ui.actionExport_png, QtCore.SIGNAL('triggered()'),
                     self.exportToPNG)
        self.connect(self.ui.action_Build, QtCore.SIGNAL('triggered()'),
                     self.Buildgraphic)
        self.connect(self.ui.action_Open, QtCore.SIGNAL('triggered()'),
                     self.openPcvFile)
        self.connect(self.ui.action_Quit, QtCore.SIGNAL('triggered()'),
                     self.Close)
        self.connect(self.ui.zoomButtonPlus, QtCore.SIGNAL('clicked()'),
                     self.plusZoom)
        self.connect(self.ui.zoomButtonLess, QtCore.SIGNAL('clicked()'),
                     self.lessZoom)

        self.connect(self.ui.axisIncreaseButton, QtCore.SIGNAL('clicked()'),
                     self.increaseAxisDialog)
        self.connect(self.ui.setWidthButton, QtCore.SIGNAL('clicked()'),
                     self.changeWidthDialog)
        self.connect(self.ui.QCheckAntiAliasing, QtCore.SIGNAL('clicked()'),
                     self.antiAliasing)

        self.connect(self.ui.actionUndo, QtCore.SIGNAL('triggered()'),
                     self.undoProcess)
        self.connect(self.ui.actionRedo, QtCore.SIGNAL('triggered()'),
                     self.redoProcess)

        self.connect(self.ui.action_About, QtCore.SIGNAL('triggered()'),
                     self.showCredits)

        self.connect(self.ui.actionZoomin, QtCore.SIGNAL('triggered()'),
                     self.plusZoom)
        self.connect(self.ui.actionZoomout, QtCore.SIGNAL('triggered()'),
                     self.lessZoom)
        self.connect(self.ui.actionLine_width, QtCore.SIGNAL('triggered()'),
                     self.changeWidthDialog)

        self.connect(self.ui.actionViewLayers, QtCore.SIGNAL('toggled(bool)'),
                     self.viewLayers)
        self.connect(self.ui.actionViewTable, QtCore.SIGNAL('toggled(bool)'),
                     self.viewTable)

    def viewLayers(self, checked):
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
            #print "In Redo %d" % (self.scene.countUndo)
            if self.scene.countUndo < 0:
                QtGui.QMessageBox.information(
                    self, self.trUtf8("Redo"),
                    self.trUtf8("There isn't Statement to Redo!")
                )
            else:
                statementList = self.scene.listUndoStatement
                cmd = str(statementList[self.scene.countUndo])
                strList = cmd.split()
                string = ''.join(strList[:1])

                if string == "COLOR":
                    num = (len(strList) - 1) / 2
                    for i in range(1, len(strList) - 1, 2):
                        self.scene.brushSelection2(strList[i], strList[i + 1],
                                                   num)
                    self.scene.countUndo = self.scene.countUndo + 1

                elif string == "SHOWALL":
                    num_selected_lines = int(''.join(strList[2:]))
                    for i in range(num_selected_lines):
                        for j in range(self.scene.axes_number - 1):
                            self.scene.hideSelected2(''.join(strList[1:2]))
                            self.scene.countUndo = self.scene.countUndo - 1
                            cmd = str(statementList[len(statementList)
                                                    - self.scene.countUndo])
                            strList = cmd.split()

                elif string == "HIDE":
                    num_selected_lines = len(strList)

                    for i in range(1, num_selected_lines, 1):
                        self.scene.hideSelected2(strList[i])

                    self.scene.countUndo = self.scene.countUndo + 1
                elif string == "ZOOM+":
                    self.plusZoom2()
                    self.scene.countUndo = self.scene.countUndo + 1
                elif string == "ZOOM-":
                    self.lessZoom2()
                    self.scene.countUndo = self.scene.countUndo + 1
                elif string == "CHANGE":
                    listParam = []
                    num_selected_lines = len(strList)

                    for i in range(1, num_selected_lines, 3):
                        listParam.append(strList[i])
                        listParam.append(strList[i + 1])
                        listParam.append(strList[i + 2])
                        self.axisButton.buttonPressed2(listParam)
                        listParam = []

                    self.scene.countUndo = self.scene.countUndo + 1

                    #listParam = []
                    #for i in range(self.scene.axes_number):
                #        listParam.append(strList[i + 1])
                #    print "Param CHANGE"
                #    print strList
                #    self.axisButton.buttonPressed2(listParam)
                #    self.scene.countUndo = self.scene.countUndo + 1
                elif string == "WIDTH":
                    #print "width"
                    num_selected_lines = len(strList) - 1
                    for i in range(1, num_selected_lines, 3):
                        self.scene.changeWidth2(strList[i], strList[i + 1])
                    self.scene.countUndo = self.scene.countUndo + 1
                elif string == "ADDLAYER":
                    sel.scene.addLayer(strList[1], strList[2], strList[3])
                    self.scene.countUndo = self.scene.countUndo + 1
                elif string == "REMOVELAYER":
                        self.scene.removeLayer2(strList[1])
            #            print "REMOVE LAYER %s" % (strList[1])
                        self.scene.countUndo = self.scene.countUndo + 1

            #print self.scene.countUndo
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
                string = ''.join(strList[:1])
                if string == "COLOR":
                    num = (len(strList) - 1) / 2
                    for i in range(len(strList) - 1, 1, -2):
                        self.scene.brushSelection2(strList[i - 1],
                                                   strList[i], num)
                    self.scene.countUndo = self.scene.countUndo - 1

                elif string == "SHOWALL":
                    num_selected_lines = int(''.join(strList[2:]))
                    for i in range(num_selected_lines):
                        for j in range(self.scene.axes_number - 1):
                            self.scene.hideSelected2(''.join(strList[1:2]))
                            self.scene.countUndo = self.scene.countUndo + 1
                            cmd = str(statementList[len(statementList)
                                                    - self.scene.countUndo])
                            strList = cmd.split()
                    self.scene.countUndo = self.scene.countUndo + 1

                elif string == "HIDE":
                        num_selected_lines = (len(strList) - 1)
                        for i in range(num_selected_lines, 0, -1):
                            self.scene.showAllLines2(strList[i])
                        self.scene.countUndo = self.scene.countUndo - 1
                elif string == "ZOOM+":
                    self.lessZoom2()
                    self.scene.countUndo = self.scene.countUndo - 1
                elif string == "ZOOM-":
                    self.plusZoom2()
                    self.scene.countUndo = self.scene.countUndo - 1
                elif string == "CHANGE":
                        listParam = []
                        num_selected_lines = len(strList)
            #            print "selected %d" % (num_selected_lines)
                        for i in range(num_selected_lines - 1, 0, -3):
                            #self.scene.hideSelected2(strList[i])
                            listParam.append(strList[i - 2])
                            listParam.append(strList[i - 1])
                            listParam.append(strList[i])
                            self.axisButton.buttonPressed2(listParam)
                            listParam = []
                        self.scene.countUndo = self.scene.countUndo - 1
                    #listParam = []
                    #for i in range(self.scene.axes_number):
                    #    listParam.append(strList[i + 1])
                    #self.axisButton.buttonPressed2(listParam)
                    #self.scene.countUndo = self.scene.countUndo - 1
                elif string == "WIDTH":
                        num_selected_lines = len(strList) - 1
                        for i in range(num_selected_lines, 0, -3):
                            self.scene.changeWidth2(strList[i - 2],
                                                    strList[i - 1])
                        self.scene.countUndo = self.scene.countUndo - 1
                elif string == "ADDLAYER":
                        self.scene.removeLayer2(strList[1])
            #            print "REMOVE LAYER %s" % (strList[1])
                        self.scene.countUndo = self.scene.countUndo - 1
                elif string == "REMOVELAYER":
                        i = 1
                        while not strList[i] and not strList[i]:
                            i += 1
                        for j in range(i):
                            self.scene.createLayer(
                                strList[1], strList[2 + j],
                                strList[2 + (i - 1)])
                        self.scene.countUndo = self.scene.countUndo - 1
            #    print self.scene.countUndo

        except:
            QtGui.QMessageBox.information(
                self, self.trUtf8("Undo"),
                self.trUtf8("There isn't Statement to Undo!"))
                #self.ui.setMenuBar(self.menubar)

    def changeWidthDialog(self):
        panel = buildWidthPanel(self)
        panel.show()
        del panel

    def increaseAxisDialog(self):
        panel = buildSelectIdPanel(self)
        panel.show()
        del panel

    def plusZoom(self):
        #self.matrix.scale(2, 2)
        #self.ui.graphicsView.setMatrix(self.matrix)
        self.ui.graphicsView.scale(1.15, 1.15)
        self.line.decreaseWidth()

        for i in range(len(self.scene.listUndoStatement) - 1,
                       self.scene.countUndo - 1, -1):
            del self.scene.listUndoStatement[i]

        self.scene.listUndoStatement.append("ZOOM+")
#        self.scene.countUndo = self.scene.countUndo + 1
        self.scene.countUndo = len(self.scene.listUndoStatement)

    def plusZoom2(self):
        #self.matrix.scale(2, 2)
        #self.ui.graphicsView.setMatrix(self.matrix)
        self.ui.graphicsView.scale(1.15, 1.15)
        self.line.decreaseWidth()
        #print "ZOOM+"

    def lessZoom(self):
        #self.matrix.scale(0.5, 0.5)
        #self.ui.graphicsView.setMatrix(self.matrix)
        self.ui.graphicsView.scale(1 / 1.15, 1 / 1.15)
        self.line.increaseWidth()

        for i in range(len(self.scene.listUndoStatement) - 1,
                       self.scene.countUndo - 1, -1):
            del self.scene.listUndoStatement[i]

        #print "ZOOM-"
        self.scene.listUndoStatement.append("ZOOM-")
        #self.scene.countUndo = self.scene.countUndo + 1
        self.scene.countUndo = len(self.scene.listUndoStatement)

    def lessZoom2(self):
        #self.matrix.scale(0.5, 0.5)
        #self.ui.graphicsView.setMatrix(self.matrix)
        self.ui.graphicsView.scale(1 / 1.15, 1 / 1.15)
        self.line.increaseWidth()
        #print "ZOOM-"

    def empty_ImageView(self):
        tableHeader = []
        comboList = []

        # Handler of engine/ComboBox axis name translate
        axesDict = {}

        # Flag for not duplicate lines!
        dictFull = False
        # combo = axisgui.AxisName(self.ui, self)
        # combo.show()
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
        #self.ui.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing)
        self.ui.graphicsView.setScene(self.scene)
        self.ui.graphicsView.setDragMode(2)

        self.connect(self.ui.hideSelectionButton, QtCore.SIGNAL('clicked()'),
                     self.scene.hideSelected)
        self.connect(self.ui.brushButton, QtCore.SIGNAL('clicked()'),
                     self.scene.brushSelection)
        self.connect(self.ui.showOnlyButton, QtCore.SIGNAL('clicked()'),
                     self.scene.hideNotSelected)
        self.connect(self.ui.showAllButton, QtCore.SIGNAL('clicked()'),
                     self.scene.showAllLines)

        self.connect(self.ui.actionHide, QtCore.SIGNAL('triggered()'),
                     self.scene.hideSelected)
        self.connect(self.ui.actionBrush, QtCore.SIGNAL('triggered()'),
                     self.scene.brushSelection)
        self.connect(self.ui.actionShow_only, QtCore.SIGNAL('triggered()'),
                     self.scene.hideNotSelected)
        self.connect(self.ui.actionShow_all, QtCore.SIGNAL('triggered()'),
                     self.scene.showAllLines)

        #Layer Buttons
        self.connect(self.ui.layersTreeWidget,
                     QtCore.SIGNAL('itemClicked(QTreeWidgetItem*, int)'),
                     self.scene.selectLayer)
        self.connect(self.ui.sortLayerButton,
                     QtCore.SIGNAL('clicked()'),
                     self.sortLayers)
        self.connect(self.ui.removeLayerButton,
                     QtCore.SIGNAL('clicked()'),
                     self.scene.removeLayer)
        self.connect(self.ui.addLayerButton,
                     QtCore.SIGNAL('clicked()'),
                     self.scene.addLayer)
        self.connect(self.ui.selectLayerButton,
                     QtCore.SIGNAL('clicked()'),
                     self.scene.doSelectLayer)

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
            #if(not self.line['hidden']):
            linenb = linenb + 1
        self.ui.horizontalSlider.setMaximum(linenb / (self.axes_number - 1))
        self.ui.horizontalSlider.setValue(linenb / (self.axes_number - 1))

        #ui.menubar.hide()

        axisgui.addAxes(self.image, self.scene, self.line, self.axes_number,
                        self.ui)

        self.ui.tableWidget.setHorizontalHeaderLabels(tableHeader)

        self.ui.tableWidget.horizontalHeader().setResizeMode(
            QtGui.QListView.Adjust, QtGui.QHeaderView.Interactive)

        self.ui.tableWidget.verticalHeader().hide()
        self.ui.tableWidget.setShowGrid(True)
        self.ui.tableWidget.setSelectionBehavior(
                                            QtGui.QAbstractItemView.SelectRows)

        self.line = lines.Line(self.scene, self.image, self.axes_number,
                               self.ui, self.comboList)
        self.line.addLines(linenb)

        self.connect(self.ui.horizontalSlider,
                     QtCore.SIGNAL('valueChanged(int)'),
                     self.line.update_lines_view)
        self.axisButton.setLines(self.line, linenb)
        self.axisButton.setImage(self.image)
        self.axisButton.setCurrentEngine(pcoords)
        self.axisButton.setSlider(self.ui.horizontalSlider)
        self.buttonChange.append(self.axisButton)

    def Close(self):
        print "Closing Window!"
        self.close()

    def closeEvent(self, event):
        self.scene.clearSelection()
        event.accept()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    PCoords = PcoordsApp()
    PCoords.init_view(None)
    PCoords.create_window_after_init_view()
    if not PCoords.image:
        #if not pcvFileBuilded:
        PCoords.empty_ImageView()
        print "*** Could not create image. Exiting."
        #sys.exit(1)
    if PCoords.image:
        PCoords.paint_ImageView()
    sys.exit(app.exec_())