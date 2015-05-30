# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from eight import *

from PyQt4 import QtCore, QtGui, QtWebKit
from . import Container
from .icons import icons
from .menu_bar import MenuBar
from .toolbar import Toolbar
from .statusbar import Statusbar
from .databases_table import DatabasesTableWidget
from .gui import horizontal_line, header
from .projects import ProjectListWidget
import sys


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__(None)

        self.buttons = Container()

        # Window title
        self.setWindowTitle("Activity Browser")

        # Small icon in main window titlebar
        self.icon = QtGui.QIcon(icons.pony)
        self.setWindowIcon(self.icon)

        # Clipboard
        self.clip = QtGui.QApplication.clipboard()

        # Layout
        # The top level element is `central_widget`.
        # Inside is a vertical layout `vertical_container`.
        # Inside the vertical layout is a horizontal layout `main_horizontal_box` with two elements and a
        # The enclosing element is `main_horizontal_box`, which contains the
        # left and right panels `left_panel` and `right_panel`.

        self.main_horizontal_box = QtGui.QHBoxLayout()

        self.left_panel = QtGui.QTabWidget()
        self.right_panel = self.build_right_panel()
        self.left_panel.setMovable(True)
        self.right_panel.setMovable(True)

        self.splitter_horizontal = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.splitter_horizontal.addWidget(self.left_panel)
        self.splitter_horizontal.addWidget(self.right_panel)
        self.main_horizontal_box.addWidget(self.splitter_horizontal)

        self.vertical_container = QtGui.QVBoxLayout()
        self.vertical_container.addLayout(self.main_horizontal_box)

        self.central_widget = QtGui.QWidget()
        self.central_widget.setLayout(self.vertical_container)
        self.setCentralWidget(self.central_widget)

        # Layout: extra items outside main layout
        self.menu_bar = MenuBar(self)
        self.toolbar = Toolbar(self)
        self.statusbar = Statusbar(self)

    def add_tab_to_panel(self, obj, label, side):
        panel = self.left_panel if side == 'left' else self.right_panel
        panel.addTab(obj, label)

    def select_tab(self, obj, side):
        panel = self.left_panel if side == 'left' else self.right_panel
        panel.setCurrentIndex(panel.indexOf(obj))

    def build_right_panel(self):
        panel = QtGui.QTabWidget()
        panel.setMovable(True)

        self.inventory_tab_container = self.build_inventory_tab()
        panel.addTab(self.inventory_tab_container, 'Inventory')

        return panel

    def dialog(self, title, label):
        value, ok = QtGui.QInputDialog.getText(self, title, label)
        if ok:
            return value

    def build_inventory_tab(self):
        self.projects_list_widget = ProjectListWidget()
        self.table_databases = DatabasesTableWidget()

        self.buttons.new_project = QtGui.QPushButton('Create New Project')
        self.buttons.new_database = QtGui.QPushButton('Create New Database')

        projects_list_layout = QtGui.QHBoxLayout()
        projects_list_layout.setAlignment(QtCore.Qt.AlignLeft)
        projects_list_layout.addWidget(QtGui.QLabel('Projects:'))
        projects_list_layout.addWidget(header('Boldie'))
        projects_list_layout.addWidget(self.projects_list_widget)
        projects_list_layout.addWidget(self.buttons.new_project)

        databases_table_layout = QtGui.QHBoxLayout()
        databases_table_layout.addWidget(QtGui.QLabel('Databases:'))
        databases_table_layout.addWidget(self.table_databases)
        databases_table_layout.addWidget(self.buttons.new_database)
        databases_table_layout.setAlignment(QtCore.Qt.AlignTop)

        # Overall Layout
        tab_container = QtGui.QVBoxLayout()
        tab_container.addLayout(projects_list_layout)
        tab_container.addWidget(horizontal_line())
        tab_container.addLayout(databases_table_layout)
        tab_container.addStretch(1)

        containing_widget = QtGui.QWidget()
        containing_widget.setLayout(tab_container)

        # Context menus (shown on right click)
        self.table_databases.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        # self.action_delete_database = QtGui.QAction(QtGui.QIcon(icons.context.delete), "delete database", None)
        # self.action_delete_database.triggered.connect(self.delete_database)
        # self.table_databases.addAction(self.action_delete_database)

        # Connections
        # self.table_databases.itemDoubleClicked.connect(self.gotoDoubleClickDatabase)
        # button_add_db.clicked.connect(self.new_database)
        # button_refresh.clicked.connect(self.listDatabases)

        return containing_widget
