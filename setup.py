#!/usr/bin/env python

import os, glob
from distutils.core import setup
from distutils.command.install import install

_VERSION="0.7"

data_files = []
files = ['icons/width.png', 'icons/less.png', 'icons/brush.png', 'icons/hide.png', 'icons/lesszoom.png', 'icons/lock.png', 'icons/more.png', 'icons/morezoom.png']
data_files.append(('/usr/share/picviz-gui/icons', files))

class my_install(install):
   def init_siteconfig(self):
        config = open("PicvizGui/siteconfig.py", "w")
        print >> config, "prefix = '%s'" % os.path.abspath(self.prefix)
        print >> config, "version = '%s'" % _VERSION
        config.close()

   def run(self):
        os.umask(022)
        self.init_siteconfig()
        install.run(self)

setup(name="picviz-gui",
      version=_VERSION,
      maintainer = "Sebastien Tricaud",
      maintainer_email = "toady@gscore.org",
      url = "http://www.wallinfire.net/picviz",
      data_files=data_files,
      packages=[ 'PicvizGui' ],
      scripts=[ "picviz-gui" ],
      cmdclass={ 'install': my_install } )

