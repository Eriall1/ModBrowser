import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QListWidget,
                             QListWidgetItem, QHBoxLayout, QPushButton,QVBoxLayout, QTextEdit, QLabel, QComboBox)
from PyQt5.QtCore import Qt

from CurseForgeAPy import CurseForgeAPI
from CurseForgeAPy.SchemaClasses import Mod, ModSearchSortField, SortOrder

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.api = CurseForgeAPI("$2a$10$r1yzodsjerK60f/Ed9wIeedoxIgUpEzwqATilRvPEe54bovrccCSW")

        # Create the list widget and set its selection mode
        self.list_widget = QListWidget(self)
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)

        
        self.list_selected = QListWidget(self)
        self.list_selected.setSelectionMode(QListWidget.SingleSelection)

        # Connect the itemDoubleClicked signal to the switch
        self.list_widget.itemDoubleClicked.connect(self.switch)
        # Connect the itemDoubleClicked signal to the switch
        self.list_selected.itemDoubleClicked.connect(self.switch)

        # when an item is added, run the switch function
        self.list_widget.model().rowsInserted.connect(self.onAddWidget)
        self.list_selected.model().rowsInserted.connect(self.onAddSelected)

        # Set up the layout
        toplevel = QVBoxLayout(self)
        layout = QHBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addWidget(self.list_selected)

        layout1 = QHBoxLayout()
        InputLayout = QVBoxLayout()
        ChoiceLayout = QVBoxLayout()
        versionLayout = QVBoxLayout()

        SearchLayout = QVBoxLayout()

        # add button
        self.searchLabel = QLabel("Push to search:")
        self.searchButton = QPushButton("Search")
        self.searchButton.setFixedHeight(30)
        self.searchButton.setFixedWidth(200)
        SearchLayout.addWidget(self.searchLabel)
        SearchLayout.addWidget(self.searchButton)
        self.searchButton.clicked.connect(self.search)

        # add text box
        self.modNameLabel = QLabel("Mod Name")
        self.modName = QTextEdit()
        self.modName.setFixedHeight(30)
        self.modName.setFixedWidth(200)
        InputLayout.addWidget(self.modNameLabel)
        InputLayout.addWidget(self.modName)

        # add combo box
        self.modTypeLabel = QLabel("Sort By")
        self.modType = QComboBox()
        self.modType.addItems(ModSearchSortField.__members__.keys())
        self.modType.setFixedHeight(30)
        self.modType.setFixedWidth(200)
        ChoiceLayout.addWidget(self.modTypeLabel)
        ChoiceLayout.addWidget(self.modType)

        
        # add second combo box
        self.versionLabel = QLabel("Sort Order")
        self.version = QComboBox()
        self.version.addItems([i.strip() for i in """
        Minecraft 1.20
        1.20-Snapshot
        Minecraft 1.19
        1.19.3
        1.19.2
        1.19.1
        1.19
        1.19-Snapshot
        Minecraft 1.18
        1.18.2
        1.18.1
        1.18
        1.18-Snapshot
        Minecraft 1.17
        1.17.1
        1.17
        1.17-Snapshot
        Minecraft 1.16
        1.16.5
        1.16.4
        1.16.3
        1.16.3
        1.16.1
        1.16
        1.16-Snapshot
        Minecraft 1.15
        1.15.2
        1.15.1
        1.15
        1.15-Snapshot
        Minecraft 1.14
        1.14.4
        1.14.3
        1.14.2
        1.14.1
        1.14
        1.14-Snapshot
        Minecraft 1.13
        1.13.2
        1.13.1
        1.13
        1.13-Snapshot
        Minecraft 1.12
        1.12.2
        1.12.1
        1.12
        1.12-Snapshot
        Minecraft 1.11
        1.11.2
        1.11.1
        1.11
        1.11-Snapshot
        Minecraft 1.10
        1.10.2
        1.10.1
        1.10
        1.10-Snapshot
        Minecraft 1.9
        1.9.4
        1.9.3
        1.9.2
        1.9.1
        1.9
        1.9-Snapshot
        Minecraft 1.8
        1.8.9
        1.8.8
        1.8.7
        1.8.6
        1.8.5
        1.8.4
        1.8.3
        1.8.2
        1.8.1
        1.8
        1.8-Snapshot
        Minecraft 1.7
        1.7.10
        1.7.9
        1.7.8
        1.7.7
        1.7.6
        1.7.5
        1.7.4
        1.7.3
        1.7.2
        Minecraft 1.6
        1.6.4
        1.6.2
        1.6.1
        Minecraft 1.5
        1.5.2
        1.5.1
        1.5.0
        Minecraft 1.4
        1.4.7
        1.4.6
        1.4.5
        1.4.4
        1.4.2
        Minecraft 1.3
        1.3.2
        1.3.1
        Minecraft 1.2
        1.2.5
        1.2.4
        1.2.3
        1.2.2
        1.2.1
        Minecraft 1.1
        1.1.0
        Minecraft 1.0
        1.0.0
        1.0""".split("\n")])
        self.version.setFixedHeight(30)
        self.version.setFixedWidth(200)
        versionLayout.addWidget(self.versionLabel)
        versionLayout.addWidget(self.version)


        layout1.addLayout(InputLayout)
        layout1.addLayout(ChoiceLayout)
        layout1.addLayout(versionLayout)
        layout1.addLayout(SearchLayout)

        toplevel.addLayout(layout1)
        toplevel.addLayout(layout)
        self.setLayout(toplevel)

    def search(self):
        currentSearch = self.modName.toPlainText()
        self.list_widget.clear()
        mods = self.api.searchMods(gameId=432, gameVersion=self.version.currentText(),searchFilter=currentSearch, sortField=6, sortOrder=SortOrder.Descending).data
        for mod in mods:
            item = QListWidgetItem(mod.name)
            item.setData(Qt.UserRole, mod)
            self.list_widget.addItem(item)

    def which(self, item: QListWidgetItem):
        items = self.list_widget.findItems(item.text(), Qt.MatchExactly)
        if items:
            return "widget"
        else :
            return "selected"

    def onAddWidget(self, index):
        item = self.list_widget.item(index.row())

    def onAddSelected(self, index, start, end):
        print(start)
        item = self.list_selected.item(start)
        print(item.data(Qt.UserRole))

    def switch(self, item):
        if self.which(item) == "widget":
            self.list_widget.takeItem(self.list_widget.row(item))
            self.list_selected.addItem(item)
        else:
            self.list_selected.takeItem(self.list_selected.row(item))
            self.list_widget.addItem(item)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
