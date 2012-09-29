
from PyQt4 import QtCore, QtGui

from build_graphic_dialog_ui import Ui_Dialog_Build
import os
# Pcoords
import pcoords


class Buildpanel(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog_Build()
        self.ui.setupUi(self)
        self.parent = parent
        QtCore.QObject.connect(
            self.ui.buttonFindPathLogFile,
            QtCore.SIGNAL('clicked()'),
            self.defineLogFile)
        QtCore.QObject.connect(
            self.ui.buttonFindPathParser,
            QtCore.SIGNAL('clicked()'),
            self.defineParser)
        QtCore.QObject.connect(
            self.ui.buttonBuild,
            QtCore.SIGNAL('clicked()'),
            self.buildFilePcv)
        QtCore.QObject.connect(
            self.ui.buttonFindDestinationPgdl,
            QtCore.SIGNAL('clicked()'),
            self.savePgdl)
        print "---Build created"

    def defineLogFile(self):
        self.nameLogFile = pcvfile = QtGui.QFileDialog.getOpenFileName(
            None, "Open Log File", "", "")
        self.ui.pathLogfile.setText(self.nameLogFile)

    def defineParser(self):
        self.nameParserFile = pcvfile = QtGui.QFileDialog.getOpenFileName(
            None, "Open Parser File", "", "")
        self.ui.pathParser.setText(self.nameParserFile)

    def savePgdl(self):
        self.namePgdlFile = pgdlfile = QtGui.QFileDialog.getSaveFileName(
            None, "Save Parser File", "/home", "")
        self.ui.pathPgdl.setText(self.namePgdlFile)
        self.parent.pcvfile = self.namePgdlFile

    def buildFilePcv(self):
        self.namePcv = "unknow.pcv"
        self.nameGraphic = "unknow.png"
        dic_TypeParser = {
            0: 'python',
            1: 'perl',
            2: 'bash',
            3: './',
            4: './',
            5: 'java'}
        index = self.ui.comboTypeParser.currentIndex()
        if index != 3 and index != 4:
            commandParse = dic_TypeParser[index] + " " + \
                    self.nameParserFile.__str__() + " " + \
                    self.nameLogFile.__str__() + " > " + \
                    self.namePgdlFile.__str__()
            print "Command: " + commandParse
            os.system(commandParse)
            QtGui.QMessageBox.information(
                self,
                self.trUtf8("Concluded"),
                self.trUtf8("The Pgdl file was created sucessfull!")
            )
            self.close()
        else:
            print "C and C++ still are not implemented"
            pass

        self.parent.image = pcoords.Image(
            str(self.parent.pcvfile), self.parent.filter)
        self.parent.paint_ImageView()
        #commandBuildPcv = "pcv -Tpngcairo " + self.namePcv  + self.nameGraphic
        #os.system(commandBuildPcv)
