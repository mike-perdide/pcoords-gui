from PyQt4 import QtGui


class ExportGraph:
    """
    Export the graph stored in the datastructure
    into an external file.
    """
    def __init__(self):
        return None

    def __getAxisposLabel(self, image, pos):
        return image['axes'][image['axeslist'][pos]]['label']

    def __getLineProperties(self, line):
        props = []
        if line['color'] != "#000000":
            props.append('color')
        if line['penwidth'] != 1.0:
            props.append('penwidth')
        if line['layer'] != "":
            props.append('layer')

        return props

    def asPNG(self, scene):
        path = QtGui.QFileDialog.getSaveFileName(
            None, "Save Png", "", "Png File (*.png)")

        if path:
            pixmap = QtGui.QPixmap(scene.width() + 20, scene.height() + 20)
            painter = QtGui.QPainter(pixmap)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            scene.render(painter)
            painter.end()
            pixmap.save(path);

    def asPGDL(self, image):
        path = QtGui.QFileDialog.getSaveFileName(
            None, "Save PGDL", "", "Picviz File (*.pgdl)")

        if path:
            fp = open(path, "w")
            fp.write("axes {\n")
            for axis in image['axeslist']:
                fp.write("    "
                         + image['axes'][axis]['type']
                         + " "
                         + image['axes'][axis]['label']
                         + ";\n")

            fp.write("}\n")
            fp.write("data {\n")
            strpos = 2
            axispos = 0
            for line in image['lines']:
#                print str(line)
                if line['hidden'] == 1:
                    continue
                if axispos == 0:
                    fp.write("    ")
                if strpos == len(image['axeslist']):
                    fp.write("%s=\"%s\", " %
                             (self.__getAxisposLabel(image, axispos),
                              line['x1_strval'])
                            )
                    fp.write("%s=\"%s\"" %
                             (self.__getAxisposLabel(image, axispos + 1),
                              line['x2_strval'])
                            )
                    # Write properties
                    props = self.__getLineProperties(line)
                    i = 1
                    if props:
                        fp.write(" [")
                    for prop in props:
                        key = prop
                        if key == "layer":
                            key = "inlayer"
                        if i == len(props):
                            fp.write("%s=\"%s\"]" % (key, line[prop]))
                        else:
                            fp.write("%s=\"%s\"," % (key, line[prop]))
                        i += 1

                    fp.write(";\n")
                    strpos = 2
                    axispos = 0
                else:
                    fp.write("%s=\"%s\", " %
                             (self.__getAxisposLabel(image, axispos),
                              line['x1_strval'])
                            )
                    strpos += 1
                    axispos += 1
            fp.write("}\n")
            fp.close()
