
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import os, sys, subprocess

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):

    width = 600
    height = 300

    def setupUi(self, MainWindow):
        # Main Window
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setWindowTitle(_translate("MainWindow", "PDF Fortress", None))
        MainWindow.setFixedSize(self.width, self.height)
        self.center(MainWindow)

        # Checking the prerequisites
        if Prerequisites.isTool('pdftk'):
            self.centralWidget(MainWindow)
        else:
            Prerequisites.showWidget(MainWindow)
        
         # Progress Bar
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)
        self.progressBar.setVisible(False)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))

        # Status Bar
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        self.statusbar.addPermanentWidget(self.progressBar)
        MainWindow.setStatusBar(self.statusbar)

        # Connect Mainwindow
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def centralWidget(self, MainWindow):
        # Central Widget
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        # Grid Layout Widget
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(5, 5, 590, 270))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))

        # Grid Layout
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

        # Horizontal Layout
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))

        # Vertical Layout
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        
        # Form Elements
        self.fileList()
        self.checkAll()
        self.addFile()
        self.removeFile()
        self.encryptFile()
        self.decryptFile()
        self.mergeFile()
        self.splitFile()

        # Adding up the Layout
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        # Setting Central Widget
        MainWindow.setCentralWidget(self.centralwidget)

    def center(self, window):
        frameGm = window.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        window.move(frameGm.topLeft())

    ############################################################
    def selectedFiles(self):
        indexes = []
        count = self.list.model().rowCount()
        for row in range(count):
            item = self.list.model().item(row)
            if item.checkState() == QtCore.Qt.Checked:
                index = QtCore.QPersistentModelIndex(item.index())    
                indexes.append((index, item.text()))

        return indexes

    def inputFilesJoin(self):
        indexes = self.selectedFiles()
        list = ["'"+str(index[1])+"'" for index in indexes ]
        return (" ").join(list)

    def outputFileName(self):
        dlg = QFileDialog()
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.setViewMode(QFileDialog.List)
        dlg.setNameFilter('PDF (*.pdf)')

        if dlg.exec_():
            return dlg.selectedFiles()

    def outputDirName(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        dlg.setViewMode(QFileDialog.List)
        dlg.setOption(QFileDialog.ShowDirsOnly, True)


        if dlg.exec_():
            return dlg.selectedFiles()

    def messageBox(self, icon, title, text, button = QMessageBox.Ok, detailed = None):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(button)
        if detailed:
            msg.setDetailedText(detailed.decode("utf-8"))
        msg.exec_()

    def messageBuilder(self, message, error = None):
        if error:
            self.messageBox(QMessageBox.Critical, message.title() + " Error", "Failed while trying to " + message + " the file(s)", button = QMessageBox.Ok, detailed = error)
        else:
            self.messageBox(QMessageBox.Information, message.title() + " Successful", "File(s) you were trying to " + message + " has been completed", button = QMessageBox.Ok)

        self.progressBar.setVisible(False)

    def fileCountChecker(count):
        def decorator(functionName):
            def wrapper(self):
                indexes = self.selectedFiles()
                selectedCount = len(indexes)
                addedCount = self.list.model().rowCount()

                if selectedCount == 1 and count == 1:
                    functionName(self)
                elif selectedCount >= 1 and count == 0:
                    functionName(self)
                elif selectedCount > 1 and count == 2:
                    functionName(self)
                else:
                    if addedCount == 0:
                        self.messageBox(QMessageBox.Warning, "Error", "Please add files to make any action", button = QMessageBox.Ok)
                    elif selectedCount == 0:
                        self.messageBox(QMessageBox.Warning, "Error", "Please select atleast one or more files", button = QMessageBox.Ok)
                    elif count == 1:
                        self.messageBox(QMessageBox.Warning, "Error", "Please select only one file", button = QMessageBox.Ok)
                    else:
                        self.messageBox(QMessageBox.Warning, "Error", "Please select more than one files", button = QMessageBox.Ok)
            return wrapper
        return decorator

    #########################################################

    # FILE ARENA
    def fileList(self):
        # List View Widget
        self.list = QListView(self.gridLayoutWidget)
        self.list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.list.setSelectionMode(QAbstractItemView.NoSelection)
        self.horizontalLayout.addWidget(self.list)
        # Standard Model
        self.model = QStandardItemModel()
        self.list.setModel(self.model)
        self.files = []
        self.model.itemChanged.connect(self.fileListSignals)

    def fileListSignals(self):
        ''' updates the select all checkbox based on the listview '''
        model = self.list.model()
        items = [model.item(index) for index in range(model.rowCount())]

        if all(item.checkState() == QtCore.Qt.Checked for item in items):
            self.checkAllBox.setTristate(False)
            self.checkAllBox.setCheckState(QtCore.Qt.Checked)
            self.checkAllBox.setText("Uncheck All")
        elif any(item.checkState() == QtCore.Qt.Checked for item in items):
            self.checkAllBox.setTristate(True)
            self.checkAllBox.setCheckState(QtCore.Qt.PartiallyChecked)
            self.checkAllBox.setText("Check All")
        else:
            self.checkAllBox.setTristate(False)
            self.checkAllBox.setCheckState(QtCore.Qt.Unchecked)
            self.checkAllBox.setText("Check All")

    # Check All
    def checkAll(self):
        self.checkAllBox = QCheckBox('Check All', self.gridLayoutWidget)
        self.checkAllBox.setChecked(False)
        self.checkAllBox.setTristate(False)
        self.checkAllBox.clicked.connect(self.checkAllSignals)
        self.verticalLayout.addWidget(self.checkAllBox)

    def checkAllSignals(self):
        ''' updates the listview based on select all checkbox '''
        model = self.list.model()
        modelCount = model.rowCount()

        if modelCount > 0:

            if self.checkAllBox.checkState() == Qt.Checked:
                state = Qt.Checked
                self.checkAllBox.setText("Uncheck All")
            elif self.checkAllBox.checkState() == Qt.PartiallyChecked and len(self.selectedFiles) == 0:
                state = Qt.Checked
            elif self.checkAllBox.checkState() == Qt.PartiallyChecked and len(self.selectedFiles) > 0:
                state =  Qt.Unchecked
            else:
                state = Qt.Unchecked
                self.checkAllBox.setText("Check All")

            for index in range(modelCount):
                item = model.item(index)
                if item.isCheckable():
                    item.setCheckState(state)
        else:
            self.checkAllBox.setCheckState(QtCore.Qt.Unchecked)
            self.checkAllBox.setText("Check All")

    # ADD FILES
    def addFile(self):
        # File Dialog
        self.addFile = QPushButton(self.gridLayoutWidget)
        self.addFile.setObjectName(_fromUtf8("addFileBtn"))
        self.addFile.setText(_translate("MainWindow", "Add", None))
        self.verticalLayout.addWidget(self.addFile)
        # Signal
        self.addFile.clicked.connect(self.addFileSignal)

    def addFileSignal(self):

        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFiles)
        dlg.setViewMode(QFileDialog.List)
        dlg.setNameFilter('PDF (*.pdf)')

        if dlg.exec_():
            files = dlg.selectedFiles()

            for file in files:
                if file not in self.files:
                    item = QStandardItem(file)
                    item.setCheckable(True)
                    item.setDragEnabled(True)
                    item.setCheckState(Qt.Unchecked)
                    self.model.appendRow(item)
                    self.files.append(file)

    # REMOVE FILES
    def removeFile(self):
        # File Dialog
        self.removeFile = QPushButton(self.gridLayoutWidget)
        self.removeFile.setObjectName(_fromUtf8("removeFileBtn"))
        self.removeFile.setText(_translate("MainWindow", "Remove", None))
        self.verticalLayout.addWidget(self.removeFile)
        # Signal
        self.removeFile.clicked.connect(self.removeFileSignal)

    @fileCountChecker(0)
    def removeFileSignal(self):

        indexes = self.selectedFiles()
        for index in indexes:
            self.list.model().removeRow(index[0].row())
            self.files.remove(index[1])

        self.checkAllBox.setCheckState(QtCore.Qt.Unchecked)
        self.checkAllBox.setText("Check All")
        self.checkAllBox.setTristate(False)

    def passwordDialog(self):

        self.diaPopup = QDialog()
        self.diaPopup.setWindowTitle("PDF Password")
        self.diaPopup.setWindowModality(Qt.ApplicationModal)
        self.diaPopup.setFixedSize(400,100)
        self.center(self.diaPopup)

        self.diaHorizontalLayoutWidget = QtWidgets.QWidget(self.diaPopup)
        self.diaHorizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 380, 80))
        self.diaHorizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.diaHorizontalLayout = QtWidgets.QHBoxLayout(self.diaHorizontalLayoutWidget)
        self.diaHorizontalLayout.setObjectName("horizontalLayout")

        # Label
        self.diaPasswordLabel = QLabel(self.diaHorizontalLayoutWidget)
        self.diaPasswordLabel.setObjectName(_fromUtf8("passwordLabel"))
        self.diaPasswordLabel.setText("Enter Password")
        self.diaHorizontalLayout.addWidget(self.diaPasswordLabel)
        # Password
        self.password = QLineEdit(self.diaHorizontalLayoutWidget)
        self.password.setObjectName(_fromUtf8("password"))
        self.password.setEchoMode(QLineEdit.Password)
        self.diaHorizontalLayout.addWidget(self.password)
        # Button
        self.diaButton = QPushButton(self.diaHorizontalLayoutWidget)
        self.diaButton.setObjectName(_fromUtf8("encryptFileBtn"))
        self.diaHorizontalLayout.addWidget(self.diaButton)
        self.diaButton.clicked.connect(self.passwordDialogSignal)

    def passwordDialogSignal(self):
        if self.password.text():
            self.diaPopup.close()

    # ENCRYPT
    def encryptFile(self):
        # File Dialog
        self.encryptFile = QPushButton(self.gridLayoutWidget)
        self.encryptFile.setObjectName(_fromUtf8("encryptFileBtn"))
        self.encryptFile.setText(_translate("MainWindow", "Encrypt", None))
        self.verticalLayout.addWidget(self.encryptFile)
        # Signal
        self.encryptFile.clicked.connect(self.encryptFileSignal)

    @fileCountChecker(0)
    def encryptFileSignal(self):
        
        self.passwordDialog()
        self.diaButton.setText("Encrypt")
        self.diaPopup.exec_()

        # Progress bar 
        i = 0
        l = len(self.selectedFiles())
        k = float(100.00 / l)
        self.progressBar.setVisible(True)

        if self.password.text():
            indexes = self.selectedFiles()
            outputDir = self.outputDirName()
            password = self.password.text()

            if outputDir:
                for index in indexes:
                    fileName = os.path.split(index[1])
                    dirPath = outputDir[0]
                    cmd = "pdftk '" + index[1] + "' output '" + dirPath + "/" + fileName[1] + "' user_pw " + password
                    process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

                    # Progress bar
                    i += 1
                    self.progressBar.setValue(k * i)

                self.messageBuilder("encrypt", process.stderr)

    # DECRYPT
    def decryptFile(self):
        # File Dialog
        self.decryptFile = QPushButton(self.gridLayoutWidget)
        self.decryptFile.setObjectName(_fromUtf8("decryptFileBtn"))
        self.decryptFile.setText(_translate("MainWindow", "Decrypt", None))
        self.verticalLayout.addWidget(self.decryptFile)
        # Signal
        self.decryptFile.clicked.connect(self.decryptFileSignal)

    @fileCountChecker(0)
    def decryptFileSignal(self):

        self.passwordDialog()
        self.diaButton.setText("Decrypt")
        self.diaPopup.exec_()

        # Progress bar 
        i = 0
        l = len(self.selectedFiles())
        k = float(100.00 / l)
        self.progressBar.setVisible(True)

        if self.password.text():
            indexes = self.selectedFiles()
            outputDir = self.outputDirName()
            password = self.password.text()

            if outputDir:
                for index in indexes:
                    fileName = os.path.split(index[1])
                    dirPath = outputDir[0]
                    cmd = "pdftk '" + index[1] + "' input_pw '" + password + "' output '" + dirPath + "/" + fileName[1] + "'"
                    process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

                    # Progress bar
                    i += 1
                    self.progressBar.setValue(k * i)

                self.messageBuilder("decrypt", process.stderr)

    # SPLIT
    def splitFile(self):
        # File Dialog
        self.splitFile = QPushButton(self.gridLayoutWidget)
        self.splitFile.setObjectName(_fromUtf8("splitFileBtn"))
        self.splitFile.setText(_translate("MainWindow", "Split", None))
        self.verticalLayout.addWidget(self.splitFile)
        # Signal
        self.splitFile.clicked.connect(self.splitFileSignal)

    @fileCountChecker(1)
    def splitFileSignal(self):

        outputFiles = self.outputFileName()

        if outputFiles:
            cmd = "pdftk " + self.inputFilesJoin() + " burst output '" + str(outputFiles[0]) + "_%02d.pdf' compress"
            process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            self.messageBuilder("split", process.stderr)

    # MERGE
    def mergeFile(self):
        # File Dialog
        self.mergeFile = QPushButton(self.gridLayoutWidget)
        self.mergeFile.setObjectName(_fromUtf8("mergeFileBtn"))
        self.mergeFile.setText(_translate("MainWindow", "Merge", None))
        self.verticalLayout.addWidget(self.mergeFile)
        # Signal
        self.mergeFile.clicked.connect(self.mergeFileSignal)

    @fileCountChecker(2)
    def mergeFileSignal(self):

        outputFiles = self.outputFileName()

        if outputFiles:
            cmd = "pdftk " + self.inputFilesJoin() + " cat output '" + str(outputFiles[0]) + ".pdf'"
            process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            self.messageBuilder("merge", process.stderr)        

class Prerequisites:
    
    @staticmethod    
    def isTool(name):
        try:
            devnull = open(os.devnull)
            subprocess.Popen([name], stdout=devnull, stderr=devnull).communicate()
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                return False
        return True

    @staticmethod
    def showWidget(MainWindow):
        textBrowser = QTextBrowser(MainWindow)
        textBrowser.setGeometry(QtCore.QRect(10, 10, 580, 280))
        textBrowser.setObjectName(_fromUtf8("textBrowser"))
        textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600;\">PDFtk is required, please install it<br /></span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-style:italic; text-decoration: underline;\">1.For Ubuntu</span><span style=\" font-size:9pt;\">, Run the below command in terminal <pre>sudo apt-get install pdftk</pre></span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-style:italic; text-decoration: underline;\">2. For Windows</span>,</p> <pre style=\" font-size:9pt;\">https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/pdftk_server-2.02-win-setup.exe</pre>"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-style:italic; text-decoration: underline;\">3. For Mac</span>,</p> <pre style=\" font-size:9pt;\">https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/pdftk_server-2.02-mac_osx-10.6-setup.pkg</pre>"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))

if __name__ == "__main__":
       
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())