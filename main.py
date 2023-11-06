import sys
import os
from python_highlighter import PythonHighlighter
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QFileSystemModel, QTreeView, \
    QVBoxLayout, QWidget, QDockWidget, QMessageBox, QMenu, QInputDialog, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QModelIndex

class CodeEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.current_file_path = None

        self.highlighter = PythonHighlighter(self.textEdit.document())

        self.textEdit.setTabStopWidth(4 * self.textEdit.fontMetrics().width(' '))


    def initUI(self):
        # Load the style sheet
        with open('style.qss', 'r') as file:
            self.setStyleSheet(file.read())

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        font = self.textEdit.font()
        font.setStyleHint(QFont.TypeWriter)
        font.setFamily("Courier")
        font.setPointSize(12)
        self.textEdit.setFont(font)

        newAction = QAction('New', self)
        newAction.triggered.connect(self.newFile)

        openAction = QAction('Open', self)
        openAction.triggered.connect(self.openFile)

        saveAction = QAction('Save', self)
        saveAction.triggered.connect(self.saveFile)

        saveAsAction = QAction('Save As', self)
        saveAsAction.triggered.connect(self.saveFileAs)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)

        self.setupFileExplorer()

        self.fileTreeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.fileTreeView.customContextMenuRequested.connect(self.showContextMenu)

        self.fileTreeView.installEventFilter(self)

        self.renaming_item = None

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
        self.current_file_path = self.fileModel.filePath(index)
        if os.path.isfile(self.current_file_path):
            with open(self.current_file_path, 'r') as file:
                self.textEdit.setPlainText(file.read())

    def showContextMenu(self, pos):
        index = self.fileTreeView.indexAt(pos)

        if index.isValid():
            menu = QMenu(self)
            open_action = QAction('Open', self)
            open_action.triggered.connect(lambda: self.openFileFromExplorer(index))
            menu.addAction(open_action)
            delete_action = QAction('Delete', self)
            delete_action.triggered.connect(lambda: self.deleteFileFromExplorer(index))
            menu.addAction(delete_action)
            rename_action = QAction('Rename', self)
            rename_action.triggered.connect(lambda: self.renameFileFromExplorer(index))
            menu.addAction(rename_action)
        else:
            menu = QMenu(self)
            new_file_action = QAction('New File', self)
            new_file_action.triggered.connect(self.showNewFileDialog)
            menu.addAction(new_file_action)

        menu.exec_(self.fileTreeView.mapToGlobal(pos))

    def renameFileFromExplorer(self, index):
        item = self.fileModel.index(index.row(), 0, index.parent())
        item_path = self.fileModel.filePath(item)
        new_name, ok = QInputDialog.getText(self, "Rename", "Enter a new name (with extension):", QLineEdit.Normal, os.path.basename(item_path))
        if ok and new_name:
            new_item_path = os.path.join(os.path.dirname(item_path), new_name)
            if os.path.exists(new_item_path):
                QMessageBox.critical(self, "Error", "A file with that name already exists.")
            else:
                os.rename(item_path, new_item_path)

    def eventFilter(self, obj, event):
        if event.type() == event.KeyPress and event.key() == Qt.Key_Return:
            if self.renaming_item:
                self.renameFileFromExplorer(self.renaming_item)
                self.renaming_item = None
        return False



    def deleteFileFromExplorer(self, index: QModelIndex):
        file_path = self.fileModel.filePath(index)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
            except OSError as e:
                QMessageBox.critical(self, "Error", f"Failed to delete the file: {str(e)}")
            else:
                self.fileModel.remove(index)

    def showNewFileDialog(self):
        new_file_name, ok = QInputDialog.getText(self, "New File", "Enter the name of the new file (with extension):", QLineEdit.Normal, "")
        if ok and new_file_name:
            new_file_path = os.path.join(os.getcwd(), new_file_name)
            with open(new_file_path, 'w') as file:
                file.write("")

    def createNewFile(self):
        new_file_name, _ = QFileDialog.getSaveFileName(self, "Create New File", "", "Text Files (*.txt);;All Files (*)")
        if new_file_name:
            with open(new_file_name, 'w') as file:
                file.write("")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = CodeEditor()
    sys.exit(app.exec_())
