#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2010 Riverbank Computing Limited.
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Riverbank Computing Limited nor the names of
##     its contributors may be used to endorse or promote products
##     derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
##
#############################################################################

###
# Julien Miotte & Feth Arezki tweaked launch_designer.py to be used with
# Majerti projects.
# This file can be redistributed under the original Riverbank terms.
###


import os
import sys
from PyQt4 import QtCore, QtGui


if __name__ != '__main__':
    sys.stderr.write(
        "Not doing anything, %s is meant to be ran directly\n" % __name__
    )
    sys.exit(2)


app = QtGui.QApplication(sys.argv)


# Tell Qt Designer where it can find the directory containing the plugins and
# Python where it can find the widgets.
env = os.environ.copy()
# one last tweak: env['PYQTDESIGNERPATH'] = 'plugins' changed to use
# absolute path
from os.path import join, dirname, abspath
repo_root = abspath(dirname(__file__))
env['PYQTDESIGNERPATH'] = join(repo_root, 'designer_plugins')
env['PYTHONPATH'] = join(repo_root, 'pcoordsgui', 'widgets')
qenv = ['%s=%s' % (name, value) for name, value in env.items()]

# Start Designer.
designer = QtCore.QProcess()
designer.setEnvironment(qenv)

designer_bin = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.BinariesPath)

if sys.platform == 'darwin':
    designer_bin += '/Designer.app/Contents/MacOS/Designer'
else:
    designer_bin += '/designer'

designer.start(designer_bin)
designer.waitForFinished(-1)

exit(designer.exitCode())
