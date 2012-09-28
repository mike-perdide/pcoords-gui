from PyQt4 import QtCore, QtGui
from aboutDialogUi import Ui_AboutDialog


class buildAboutPanel (QtGui.QDialog):
    def __init__(self, apiversion, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)
        self.apiversion = apiversion
        self.ui.plainTextEdit.textCursor().insertHtml(self.getAboutDotHTML())

        # about_text = open("PicvizGui/about.html","r")
        # string = about_text.readlines()
        # for each in string:
        #     self.ui.plainTextEdit.textCursor().insertHtml(each)

    def getAboutDotHTML(self):
        variables = {
            "GUIVERSION" : "0.7",
            "REVISION" : "$Id: aboutDialog.py 763 2009-09-08 20:03:38Z gabriel $",
            "APIVERSION" : self.apiversion
            }
        html = """
<html>
<b>Picviz-GUI GUIVERSION<br></b>

<p>
Revision number: REVISION<br/>
API version: APIVERSION<br/>
</p>


<p>URL: <a href="http://www.wallinfire.net/picviz">http://wallinfire.net/picviz</a><br></p>
<p>Help: <a href="mailto:picviz@wallinfire.net">picviz@wallinfire.net</a><br></p>
<p>IRC: #picviz at <a href="http://www.freenode.net">freenode.org</a><br><br></p>

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
