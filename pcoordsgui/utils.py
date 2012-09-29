from PyQt4.QtGui import QFileDialog


def get_pcv_filename():
    """Opens the PCV file with a QFileDialog."""
    return QFileDialog.getOpenFileName(None,
                                       "Open Pcoords graph", "",
                                       "Pcoords Files (*.pgdl *.pcv)")
