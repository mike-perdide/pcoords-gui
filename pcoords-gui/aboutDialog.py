from PyQt4 import QtGui
from aboutDialogUi import Ui_AboutDialog


class buildAboutPanel (QtGui.QDialog):
    def __init__(self, apiversion, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)
        self.apiversion = apiversion
        self.ui.plainTextEdit.textCursor().insertHtml(self.getAboutDotHTML())

        # about_text = open("PcoordsGui/about.html","r")
        # string = about_text.readlines()
        # for each in string:
        #     self.ui.plainTextEdit.textCursor().insertHtml(each)

    def getAboutDotHTML(self):
        variables = {
            "GUIVERSION": "0.7",
            "APIVERSION": self.apiversion
            }
        html = """
<html>
<b>Pcoords-GUI GUIVERSION<br></b>

<p>
API version: APIVERSION<br/>
</p>


<p>URL: <a href="http://www.wallinfire.net/pcoords">
            http://wallinfire.net/pcoords
        </a>
<br></p>
<p>Help: <a href="mailto:pcoords@wallinfire.net">
            pcoords@wallinfire.net
        </a>
<br></p>
<p>IRC: #pcoords at <a href="http://www.freenode.net">
            freenode.org
        </a>
<br><br></p>

<p><b>Maintainers:</b> <br>
Gabriel "EsCoVa" Cavalcante <br>
Sebastien "toady" Tricaud <br> <br>
</p>

<p><b>Contributor:</b> <br>
Victor "vitao_nw" Amaducci
</p>
</html>
                       """
        for key in variables:
            html = html.replace(key, str(variables[key]))
        return html
