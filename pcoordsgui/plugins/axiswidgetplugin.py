"""
File: designer_plugin.py
      Example of how designer.py can be used to easily generate Qt4 Designer
      plugins.
Copyright: 2011-2012 Feth Arezki <feth dot arezki at majerti dot fr>
           2011-2012 Julien Miotte <mike dot perdide at gmail dot com>
License: This file is released under the GPLv3
         http://www.gnu.org/licenses/gpl-3.0.txt
"""
from pcoordsgui.widgets.axis_widget import PyAxisWidget

from pcoordsgui.plugins.designer import plugin

_MODULE_INCLUDE = 'pcoordsgui.axis_widget'

AXIS_WIDGET = plugin(PyAxisWidget, "axis_widget", _MODULE_INCLUDE)