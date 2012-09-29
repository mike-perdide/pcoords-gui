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

from PyQt4.QtGui import QApplication

from pcoordsgui.main_window import MainWindow
from pcoordsgui.utils import get_pcv_filename


if __name__ == "__main__":
    app = QApplication(sys.argv)

    pcvfile = None
    filters = None

    if len(sys.argv) > 1:
        pcvfile = sys.argv[1]

    if len(sys.argv) > 2:
        filtertable = sys.argv[2:]
        filters = ' '.join(filtertable)

    if not pcvfile:
        pcvfile = get_pcv_filename()

    if pcvfile:
        pcoords_app = MainWindow(pcvfile=pcvfile, filters=filters)
        pcoords_app.show()

        sys.exit(app.exec_())
