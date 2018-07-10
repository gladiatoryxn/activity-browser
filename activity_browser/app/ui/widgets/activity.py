# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets

from .line_edit import SignalledLineEdit, SignalledPlainTextEdit


class DetailsGroupBox(QtWidgets.QGroupBox):
    def __init__(self, label, widget):
        super().__init__(label)
        self.widget = widget
        self.setCheckable(True)
        self.toggled.connect(self.showhide)
        self.setChecked(False)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(widget)
        self.setLayout(layout)
        if isinstance(self.widget, QtWidgets.QTableWidget):
            self.widget.itemChanged.connect(self.toggle_empty_table)

    def showhide(self):
        self.widget.setVisible(self.isChecked())

    def toggle_empty_table(self):
        self.setChecked(bool(self.widget.rowCount()))


class ActivityDataGrid(QtWidgets.QWidget):
    def __init__(self, parent=None, activity=None):
        super(ActivityDataGrid, self).__init__(parent)
        self.activity = activity

        self.grid = self.get_grid()
        self.setLayout(self.grid)
        # self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum))

        if activity:
            self.populate()

    def get_grid(self):
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(QtWidgets.QLabel('Name'), 1, 1)
        self.name_box = SignalledLineEdit(
            key=getattr(self.activity, "key", None),
            field="name",
            parent=self,
        )
        self.name_box.setPlaceholderText("Activity name")
        grid.addWidget(self.name_box, 1, 2, 1, 3)

        # checkbox for enabling editing of activity, default=read-only
        # lambda for user-check defined in Populate function, after required variables in scope
        self.read_only_ch = QtWidgets.QCheckBox('Read-Only', parent=self)
        self.read_only_ch.setChecked(True)

        grid.addWidget(self.read_only_ch, 1, 5)
        #improvement todo: location to be selectable from dropdown rather than free-text
        #but this requires forming a list of valid locations based on selected db..
        grid.addWidget(QtWidgets.QLabel('Location'), 2, 1)
        self.location_box = SignalledLineEdit(
            key=getattr(self.activity, "key", None),
            field="location",
            parent=self,
        )
        self.location_box.setPlaceholderText("ISO 2-letter code or custom name")
        grid.addWidget(self.location_box, 2, 2, 1, -1)

        #todo: also show project to user alongside database
        #improvement todo: allow user to copy open activity to other db, via drop-down menu here
        grid.addWidget(QtWidgets.QLabel('In database'), 3, 1)
        self.database = QtWidgets.QLabel('')
        grid.addWidget(self.database, 3, 2, 1, -1)

        self.comment_box = SignalledPlainTextEdit(
            key=getattr(self.activity, "key", None),
            field="comment",
            parent=self,
        )
        self.comment_groupbox = DetailsGroupBox(
            'Description', self.comment_box
        )
        self.comment_groupbox.setChecked(False)
        grid.addWidget(self.comment_groupbox, 4, 1, 2, -1)

        grid.setAlignment(QtCore.Qt.AlignTop)
        return grid

    def populate(self, activity=None):
        if activity:
            self.activity = activity

        self.read_only_ch.clicked.connect(
            lambda checked, key=self.activity.key: self.readOnlyStateChanged(checked, key))
        self.database.setText(self.activity['database'])
        self.name_box.setText(self.activity['name'])
        self.name_box._key = self.activity.key
        self.location_box.setText(self.activity.get('location', ''))
        self.location_box._key = self.activity.key
        self.comment_box.setPlainText(self.activity.get('comment', ''))
        # the <font> html-tag has no effect besides making the tooltip rich text
        # this is required for line breaks of long comments
        self.comment_groupbox.setToolTip(
            '<font>{}</font>'.format(self.comment_box.toPlainText())
        )
        self.comment_box._before = self.activity.get('comment', '')
        self.comment_box._key = self.activity.key
        self.comment_box.adjust_size()

    def readOnlyStateChanged(self, checked, key):
        """
        When checked=False specific data fields in the tables below become editable
        When checked=True these same fields become read-only
        """
        print("ro state change hit for:", checked, key)

        #