all: resource picviz-gui

resource: picviz.qrc
	pyrcc4 -o PicvizGui/qrc_resources.py picviz.qrc

picviz-gui: picviz.ui
	pyuic4 picviz.ui > PicvizGui/UiPicviz.py
	sed -i 's/..\/..\/..\/..\/..\/..\/..\/usr/\/usr/g' PicvizGui/UiPicviz.py

