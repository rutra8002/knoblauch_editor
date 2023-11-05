import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog

class CodeEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        newAction = QAction('New', self)
        newAction.triggered.connect(self.newFile)

        openAction = QAction('Open', self)
        openAction.triggered.connect(self.openFile)

        saveAction = QAction('Save', self)
        saveAction.triggered.connect(self.saveFile)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Simple Code Editor')
        self.show()

    def newFile(self):
        self.textEdit.clear()

    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Python Files (*.py);;Text Files (*.txt);;All Files (*)", options=options)

        if file_name:
            with open(file_name, 'r') as file:
                self.textEdit.setPlainText(file.read())

    def saveFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Python Files (*.py);;Text Files (*.txt);;All Files (*)", options=options)

        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.textEdit.toPlainText())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = CodeEditor()
    sys.exit(app.exec_())
