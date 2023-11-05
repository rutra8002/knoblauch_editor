import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QFileSystemModel, QTreeView, QVBoxLayout, QWidget, QDockWidget, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QModelIndex

class CodeEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.current_file_path = None

    def initUI(self):
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        newAction = QAction('New', self)
        newAction.triggered.connect(self.newFile)

        openAction = QAction('Open', self)
        openAction.triggered.connect(self.openFile)

        saveAction = QAction('Save', self)
        saveAction.triggered.connect(self.saveFile)

        saveAsAction = QAction('Save As', self)  # Create a "Save As" action
        saveAsAction.triggered.connect(self.saveFileAs)  # Connect it to the saveFileAs method

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)  # Add "Save As" action to the menu

        self.setupFileExplorer()

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Simple Code Editor')
        self.show()

    def setupFileExplorer(self):
        fileModel = QFileSystemModel()
        root_path = os.getcwd()
        fileModel.setRootPath(root_path)

        fileTreeView = QTreeView()
        fileTreeView.setModel(fileModel)
        fileTreeView.setRootIndex(fileModel.index(root_path))

        for column in range(1, 4):
            fileTreeView.header().setSectionHidden(column, True)

        fileExplorerLayout = QVBoxLayout()
        fileExplorerLayout.addWidget(fileTreeView)

        fileExplorerWidget = QWidget()
        fileExplorerWidget.setLayout(fileExplorerLayout)

        dock = QDockWidget("File Explorer", self)
        dock.setWidget(fileExplorerWidget)

        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

        fileTreeView.doubleClicked.connect(self.openFileFromExplorer)

        self.fileModel = fileModel
        self.fileTreeView = fileTreeView

    def newFile(self):
        self.textEdit.clear()
        self.current_file_path = None

    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Python Files (*.py);;Text Files (*.txt);;All Files (*)", options=options)

        if file_name:
            with open(file_name, 'r') as file:
                self.textEdit.setPlainText(file.read())
                self.current_file_path = file_name

    def saveFile(self):
        if self.current_file_path:
            with open(self.current_file_path, 'w') as file:
                file.write(self.textEdit.toPlainText())
        else:
            self.saveFileAs()

    def saveFileAs(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Python Files (*.py);;Text Files (*.txt);;All Files (*)", options=options)

        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.textEdit.toPlainText())
            self.current_file_path = file_name

    def openFileFromExplorer(self, index: QModelIndex):
        file_path = self.fileModel.filePath(index)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                self.textEdit.setPlainText(file.read())
                self.current_file_path = file_path

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = CodeEditor()
    sys.exit(app.exec_())
