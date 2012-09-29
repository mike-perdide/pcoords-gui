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


if __name__ == "__main__":
    app = QApplication(sys.argv)

    pcoords_app = MainWindow()
    pcoords_app.init_view()
    pcoords_app.create_window_after_init_view()

    if not pcoords_app.image:
        #if not pcvFileBuilded:
        pcoords_app.empty_ImageView()
        print "*** Could not create image. Exiting."
        #sys.exit(1)
    if pcoords_app.image:
        pcoords_app.paint_ImageView()

    sys.exit(app.exec_())
