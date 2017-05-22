# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'demo.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import glob, os, sys
import time, getpass

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setWindowTitle(_translate("MainWindow", "PDF Fortress", None))
        MainWindow.resize(500, 300)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.formLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(60, 40, 371, 141))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
    	
    	# Form Elements
    	self.actionDropdown()
    	self.sourcePathFile()
    	self.destinationPathFile()
    	self.passwordText()
    	self.progressBar()
    	self.submitButton()
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def actionDropdown(self):
    	# Label
    	self.actionLabel = QtGui.QLabel(self.formLayoutWidget)
        self.actionLabel.setObjectName(_fromUtf8("actionLabel"))
        self.actionLabel.setText(_translate("MainWindow", "Encrypt/Decrypt", None))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.actionLabel)
        # Dropdown
        self.action = QtGui.QComboBox(self.formLayoutWidget)
        self.action.setObjectName(_fromUtf8("action"))
        self.action.addItems(['Select the Action', 'Encrypt', 'Decrypt'])
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.action)
        # Signal
        self.action.currentIndexChanged.connect(self.submitButtonText)

    def sourcePathFile(self):
    	# Label
    	self.sourcePathLabel = QtGui.QLabel(self.formLayoutWidget)
        self.sourcePathLabel.setObjectName(_fromUtf8("sourcePathLabel"))
        self.sourcePathLabel.setText(_translate("MainWindow", "Source Path", None))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.sourcePathLabel)
        # File Dialog
        self.sourcePath = QtGui.QPushButton(self.formLayoutWidget)
        self.sourcePath.setObjectName(_fromUtf8("sourcePathLineEdit"))
        self.sourcePath.setText(_translate("MainWindow", "click to browse", None))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.sourcePath)
        # Signal
        self.sourcePath.clicked.connect(self.sourcePathfileDialog)

    def sourcePathfileDialog(self):
    	self.sourcePath.setText(QtGui.QFileDialog.getExistingDirectory())
        
    def destinationPathFile(self):
    	# Label
        self.destinationPathLabel = QtGui.QLabel(self.formLayoutWidget)
        self.destinationPathLabel.setObjectName(_fromUtf8("destinationPathLabel"))
        self.destinationPathLabel.setText(_translate("MainWindow", "Destination Path", None))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.destinationPathLabel)
        # File Dialog
        self.destinationPath = QtGui.QPushButton(self.formLayoutWidget)
        self.destinationPath.setObjectName(_fromUtf8("destinationPathLineEdit"))
        self.destinationPath.setText(_translate("MainWindow", "click to browse", None))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.destinationPath)
        # Signal
        self.destinationPath.clicked.connect(self.destinationPathfileDialog)

    def destinationPathfileDialog(self):
    	self.destinationPath.setText(QtGui.QFileDialog.getExistingDirectory())

    def passwordText(self):
    	# Label
    	self.passwordLabel = QtGui.QLabel(self.formLayoutWidget)
        self.passwordLabel.setObjectName(_fromUtf8("passwordLabel"))
        self.passwordLabel.setText(_translate("MainWindow", "Password", None))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.passwordLabel)
        # Password
        self.password = QtGui.QLineEdit(self.formLayoutWidget)
        self.password.setObjectName(_fromUtf8("password"))
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.password)
        

    def progressBar(self):
    	# Progress Bar
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(50, 210, 261, 21))
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))

    def submitButton(self):
    	# Submit button
        self.submit = QtGui.QPushButton(self.centralwidget)
        self.submit.setEnabled(False)
        self.submit.setVisible(False)
        self.submit.setGeometry(QtCore.QRect(330, 200, 111, 41))
        self.submit.setObjectName(_fromUtf8("submit"))
        # Signal
        self.submit.clicked.connect(self.submitSignal)

    def submitSignal(self):

        self.progressBar.setValue(0)
        action = str(self.action.currentText()).lower()
        sourcePath = str(self.sourcePath.text())
        destinationPath = str(self.destinationPath.text())
        password = str(self.password.text())

        Fortress(self, action, sourcePath, destinationPath, password)
    
    def submitButtonText(self, index):

        if self.action.itemText(index) != "Select the Action":
            self.submit.setText(_translate("MainWindow", self.action.currentText(), None))
            self.submit.setEnabled(True)
            self.submit.setVisible(True)
        else:
            self.submit.setEnabled(False)
            self.submit.setVisible(False)

class Fortress: 

    def __init__(self, GUI, action, sourcePath, destinationPath, password):

        # Local variables
        self._files = []
        self._GUI = GUI
        self._action = action
        self._sourcePath = sourcePath + '/'
        self._destinationPath = destinationPath + '/'
        self._password = password

        # print(self._sourcePath, self._destinationPath, self._password, self._action)

        # Invoke Methods
        self.fetchFiles()

        actionAttr = getattr(self, action)
        actionAttr()

    def encrypt(self):

        # Status Message
        status = self._action + "ing : "

        # Progress bar 
        i = 0
        l = len(self._files)
        k = float(100.00 / l)

        # Iterating over files list to decrypt
        for file in self._files:

            # Decrypting the pdf file
            cmd = "pdftk '" + self._sourcePath + file + "' output '" + self._destinationPath + "/" + file + "' user_pw " + self._password #pdftk 'filename' output 'encrypt/filename' user_pwd password
            os.system(cmd)

            # Progress bar
            i += 1
            self._GUI.progressBar.setValue(k * i)
            self._GUI.statusbar.showMessage(status + file)

    def decrypt(self):

        # Status Message
        status = self._action + "ing : "

        # Progress bar 
        i = 0
        l = len(self._files)
        k = float(100.00 / l)

        # Iterating over files list to decrypt
        for file in self._files:

            # Decrypting the pdf file
            cmd = "pdftk '" + self._sourcePath + file + "' input_pw " + self._password +" output '" + self._destinationPath + "/" + file +"'"
            os.system(cmd)

            # Progress bar
            i += 1
            self._GUI.progressBar.setValue(k * i)
            self._GUI.statusbar.showMessage(status + file)

    def fetchFiles(self):
        self._files = [os.path.basename(x) for x in glob.glob(self._sourcePath + "*.pdf")]


if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())