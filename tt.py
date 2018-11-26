#!/usr/bin/python


from PyQt4 import QtGui
from PyQt4 import QtCore

from PyQt4.QtCore import (QDate, QFile, QFileInfo, QIODevice, QString, QStringList, QDir, QTextStream, Qt, SIGNAL)




if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    startDir = QString("")
    startDir = "C:/library/stuff"

    filter = QStringList("")
    filter = ("JPG (*.jpg)");


    #model = QtGui.QDirModel()
    model = QtGui.QFileSystemModel()
    model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot | QDir.AllEntries)
    model.setNameFilters(filter)
    model.setNameFilterDisables(0)
    model.setRootPath(startDir)

    tree = QtGui.QTreeView()
    tree.setModel(model)


    #setDir   = QtCore.QDir(startDir)
    #setDir.setNameFilters(filter)
    #tree.setRootIndex(model.index(QtCore.QDir.path(setDir), 0 ))


    tree.setAnimated(False)
    tree.setIndentation(20)
    tree.setSortingEnabled(True)

    tree.setWindowTitle("Dir View")
    tree.resize(640, 480)
    tree.show()

    sys.exit(app.exec_())