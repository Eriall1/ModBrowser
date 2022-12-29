from main import MainWindow
from PyQt5.QtWidgets import (QApplication, QWidget, QListWidget,
                             QListWidgetItem, QHBoxLayout, QPushButton,QVBoxLayout, QLineEdit, QLabel, QComboBox,QMainWindow, QTextEdit,QFileDialog)

from PyQt5.QtCore import Qt, QIODevice, QFile, QDataStream
import sys


class DataString(MainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
    
    def initUI(self):
        self.toplevelWidget = QWidget()
        self.topLevel = QVBoxLayout()
        self.toplevelWidget.setLayout(self.topLevel)

        self.importButton = QPushButton('Import')
        self.importButton.clicked.connect(self.importData)

        self.topLevel.addWidget(self.importButton)


        self.setCentralWidget(self.toplevelWidget)
        self.setWindowTitle('From Data String')

    
    def importData(self):
        # open file dialog for user to select file, filtering by .obj files
        fileName = QFileDialog.getOpenFileName(self, 'Open File', filter='*.obj')[0]
        # open file
        file = QFile(fileName)

        if file.open(QIODevice.ReadOnly):
            self.cselected_mods = QListWidget()
            stream = QDataStream(file)
            while not stream.atEnd():
                data = stream.readQVariant()
                item = QListWidgetItem()
                item.setText(data.name)
                item.setData(Qt.UserRole, data)
                self.cselected_mods.addItem(item)
            file.close()
        else:
            print('File not found')
        self.setDLFormat()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataString()
    window.show()
    sys.exit(app.exec_())