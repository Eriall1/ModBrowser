import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QListWidget,
                             QListWidgetItem, QHBoxLayout, QPushButton,QVBoxLayout, QLineEdit, QLabel, QComboBox,QMainWindow)
from PyQt5.QtCore import Qt

import threading

from env import APIKEY

from CurseForgeAPy import CurseForgeAPI
from CurseForgeAPy.SchemaClasses import ModSearchSortField, SortOrder, GetModResponse, Mod, GetModFileResponse, FileRelationType, GetModFilesRequestBody,GetFilesResponse, ModLoaderType, File, ApiResponseCode

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.seenmods = []

        self.centerWidget = QWidget(self)
        self.setCentralWidget(self.centerWidget)

        self.api = CurseForgeAPI(APIKEY)

        self.current_search = []

        self.cselected_mods = None

        self.cversion = ""

        self.setInitLayout()

    def setInitLayout(self):
        # Set up the layout
        toplevel = QVBoxLayout(self.centerWidget)
        layout1 = QHBoxLayout(self.centerWidget)
        layout = QHBoxLayout(self.centerWidget)
        bottomLayer = QHBoxLayout(self.centerWidget)

        # Create the list widget and set its selection mode
        self.list_widget = QListWidget(self.centerWidget)
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)

        
        self.list_selected = QListWidget(self.centerWidget)
        self.list_selected.setSelectionMode(QListWidget.SingleSelection)

        # Connect the itemDoubleClicked signal to the switch
        self.list_widget.itemDoubleClicked.connect(self.switch)
        # Connect the itemDoubleClicked signal to the switch
        self.list_selected.itemDoubleClicked.connect(self.switch)

        # when an item is added, run the switch function
        self.list_widget.model().rowsInserted.connect(self.onAddWidget)
        self.list_selected.model().rowsInserted.connect(self.onAddSelected)

        layout.addWidget(self.list_widget)
        layout.addWidget(self.list_selected)

        InputLayout = QVBoxLayout(self.centerWidget)
        ChoiceLayout = QVBoxLayout(self.centerWidget)
        versionLayout = QVBoxLayout(self.centerWidget)
        SearchLayout = QVBoxLayout(self.centerWidget)

        # add button
        searchLabel = QLabel("Push to search:", self.centerWidget)
        searchButton = QPushButton("Search",self.centerWidget)
        searchButton.setFixedHeight(30)
        searchButton.setFixedWidth(200)
        searchButton.clicked.connect(self.search)
        SearchLayout.addWidget(searchLabel)
        SearchLayout.addWidget(searchButton)

        # add text box
        modNameLabel = QLabel("Mod Name",self.centerWidget)
        self.modName = QLineEdit(self.centerWidget)
        # prevent multiple lines and disallow line breaks
        self.modName.setEchoMode(QLineEdit.Normal)
    

        self.modName.setFixedHeight(30)
        self.modName.setFixedWidth(200)
        InputLayout.addWidget(modNameLabel)
        InputLayout.addWidget(self.modName)

        # add combo box
        modTypeLabel = QLabel("Sort By",self.centerWidget)
        modType = QComboBox(self.centerWidget)
        modType.addItems(ModSearchSortField.__members__.keys())
        modType.setFixedHeight(30)
        modType.setFixedWidth(200)
        ChoiceLayout.addWidget(modTypeLabel)
        ChoiceLayout.addWidget(modType)

        
        # add second combo box
        versionLabel = QLabel("Version",self.centerWidget)
        self.version = QComboBox(self.centerWidget)
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
        versionLayout.addWidget(versionLabel)
        versionLayout.addWidget(self.version)

        # add button
        dlButton = QPushButton("Download!",self.centerWidget)
        dlButton.setFixedHeight(30)
        dlButton.setFixedWidth(200)
        dlButton.clicked.connect(self.download)
        bottomLayer.addWidget(dlButton)


        layout1.addLayout(InputLayout)
        layout1.addLayout(ChoiceLayout)
        layout1.addLayout(versionLayout)
        layout1.addLayout(SearchLayout)

        toplevel.addLayout(layout1)
        toplevel.addLayout(layout)
        toplevel.addLayout(bottomLayer)

    def getDependencies(self, modid: int):
        if modid in self.seenmods:
            return
        self.seenmods.append(modid)


        mod: Mod = self.api.getMod(modid).data

        ids = []
        for i in mod.latestFilesIndexes:
            if self.cversion in i.gameVersion and i.modLoader == ModLoaderType.Forge:
                ids.append(i.fileId)
        if ids == []:
            return

        files: GetFilesResponse = self.api.getFiles(GetModFilesRequestBody(ids))

        

        if not isinstance(files, ApiResponseCode): 
            files = files.data

        files = sorted(files, key=lambda x: x.fileName, reverse=True)
        file: File = files[0]

        dependecies = file.dependencies
        for depend in dependecies:
            dependid = depend.modId
            dependRele = depend.relationType

            if dependRele in (FileRelationType.RequiredDependency, FileRelationType.Include):
                self.getDependencies(dependid)


    
    def setDLFormat(self):
        central_widget = self.centralWidget()
        central_widget.deleteLater()
        self.setCentralWidget(None)

        #region Downlaod Format
        self.DlWidget = QWidget()
        self.dlLayout = QHBoxLayout(self.DlWidget)
        self.dlC1 = QVBoxLayout(self.DlWidget)
        self.dlC2 = QVBoxLayout(self.DlWidget)
        self.dlC3 = QVBoxLayout(self.DlWidget)
    

        #labels
        self.dlC1.addWidget(QLabel("Mods to Download"))
        self.dlC2.addWidget(QLabel("Dependencies"))
        dlbutton = QPushButton("Download!")
        self.dlC3.addWidget(dlbutton)

        dlbutton.clicked.connect(self.downloadAll)

        #list widgets
        self.cselected_mods.setFixedWidth(200)
        
        self.dependancies = QListWidget()
        self.dependancies.setFixedWidth(500)

        #iterate through cselected_mods and add dependencies to dependancies
        for i in range(self.cselected_mods.count()):
            item = self.cselected_mods.item(i)
            mod: Mod = item.data(Qt.UserRole)

            ids = []
            for i in mod.latestFilesIndexes:
                if self.cversion in i.gameVersion and i.modLoader == ModLoaderType.Forge:
                    ids.append(i.fileId)

            files: GetFilesResponse = self.api.getFiles(GetModFilesRequestBody(ids))

            if not isinstance(files, ApiResponseCode): 
                files = files.data

            files = sorted(files, key=lambda x: x.fileName, reverse=True)
            file: File = files[0]
            dependecies = file.dependencies

            threads = []
            for depend in dependecies:
                dependid = depend.modId
                t = threading.Thread(target=self.getDependencies, args=(dependid,))
                t.start()
                threads.append(t)

            for t in threads:
                t.join()

            for modid in self.seenmods:
                mod = self.api.getMod(modid).data
                item = QListWidgetItem(mod.name)
                item.setData(Qt.UserRole, mod)
                self.dependancies.addItem(item)
            

                

        #Add
        self.dlC1.addWidget(self.cselected_mods)
        self.dlC2.addWidget(self.dependancies)
        

        self.dlLayout.addLayout(self.dlC1)
        self.dlLayout.addLayout(self.dlC2)
        self.dlLayout.addLayout(self.dlC3)

        
        self.setCentralWidget(self.DlWidget)
        #endregion

    def deepcopy(self, original_list_widget):
        # Add items to the original list widget

        # Create a new list widget
        copied_list_widget = QListWidget()

        # Iterate through the items in the original list widget
        for index in range(original_list_widget.count()):
            # Get the item at the current index
            original_item = original_list_widget.item(index)
            # Create a new item with the same text and other properties
            copied_item = QListWidgetItem(original_item.text())
            copied_item.setIcon(original_item.icon())
            copied_item.setData(Qt.UserRole, original_item.data(Qt.UserRole))
            # Add the new item to the copied list widget
            copied_list_widget.addItem(copied_item)
        
        return copied_list_widget


    def download(self):
        self.cselected_mods = []
        self.cversion = self.version.currentText()
        for i in range(self.list_selected.count()):
            item = self.list_selected.item(i)
            mod = item.data(Qt.UserRole)
            self.cselected_mods.append(mod)

        self.cselected_mods = self.deepcopy(self.list_selected)
        self.setDLFormat()
    
    def downloadAll(self):
        #iterate through dependancies and fetch each item
        urls = []
        for i in range(self.dependancies.count()):
            item = self.dependancies.item(i)
            mod: Mod = item.data(Qt.UserRole)
            ids = []
            for i in mod.latestFilesIndexes:
                if self.cversion in i.gameVersion and i.modLoader == ModLoaderType.Forge:
                    ids.append(i.fileId)

            files: GetFilesResponse = self.api.getFiles(GetModFilesRequestBody(ids))

            if not isinstance(files, ApiResponseCode): 
                files = files.data

            files = sorted(files, key=lambda x: x.fileName, reverse=True)
            file: File = files[0]

            urls.append(file.downloadUrl)
        
        for i in range(self.cselected_mods.count()):
            item = self.cselected_mods.item(i)
            mod: Mod = item.data(Qt.UserRole)
            ids = []
            for i in mod.latestFilesIndexes:
                if self.cversion in i.gameVersion and i.modLoader == ModLoaderType.Forge:
                    ids.append(i.fileId)

            files: GetFilesResponse = self.api.getFiles(GetModFilesRequestBody(ids))

            if not isinstance(files, ApiResponseCode): 
                files = files.data

            files = sorted(files, key=lambda x: x.fileName, reverse=True)
            file: File = files[0]

            urls.append(file.downloadUrl)
        
        urls = list(set(urls))
        print(urls)

    def search(self):
        currentSearch = self.modName.text()
        currentVersion = self.version.currentText()
        self.list_widget.clear()
        mods = self.api.searchMods(gameId=432, gameVersion=currentVersion if currentVersion != "" else None,searchFilter=currentSearch, sortField=6, sortOrder=SortOrder.Descending).data
        for mod in mods:
            item = QListWidgetItem(mod.name)
            self.current_search.append(mod.name)
            item.setData(Qt.UserRole, mod)
            self.list_widget.addItem(item)

    def which(self, item: QListWidgetItem):
        items = self.list_widget.findItems(item.text(), Qt.MatchExactly)
        if items:
            return "widget"
        else:
            return "selected"

    def onAddWidget(self, index):
        item = self.list_widget.item(index.row())

    def onAddSelected(self, index, start, end):
        item = self.list_selected.item(start)

    def switch(self, item):
        if self.which(item) == "widget":
            self.list_widget.takeItem(self.list_widget.row(item))
            self.list_selected.addItem(item)
        else:
            self.list_selected.takeItem(self.list_selected.row(item))
            self.list_widget.insertItem(self.csearchrow(item), item)

    def csearchrow(self, item):
        return self.current_search.index(item.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
