"""Basic contact book implemented in Python. Follows an MVC pattern, with the
GUI created using PyQt and the SQL database managed by sqlite."""

import sys
from PyQt5.QtCore import QLine
from PyQt5.QtWidgets import QAbstractItemView, QAction, QApplication, QDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableView, QVBoxLayout, QWidget, QToolBar
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidget, QComboBox
from PyQt5.QtWidgets import QFormLayout, QGridLayout
import logging
from PyQt5.QtWidgets import QCheckBox
from contact_book_model import ContactModel, create_connection

logging.basicConfig(level=logging.INFO)


class contact_book_view(QMainWindow):
    """The parent window for the contact book."""
    def __init__(self, parent = None):
        super().__init__() 
        self.setWindowTitle("Contact Book")
        self.model = ContactModel()
        self.setFixedSize(700, 400)
        self.layout = QVBoxLayout()
        self.create_general_ui()
        self.create_menu()

    def create_general_ui(self):
        search_layout = QHBoxLayout()
        self.searchbar = QLineEdit()
        self.search_combobox = QComboBox()
        self.search_combobox.addItems(self.model.headers)
        search_layout.addWidget(QLabel("Search: "))
        search_layout.addWidget(self.search_combobox)
        search_layout.addWidget(self.searchbar)
        self.layout.addLayout(search_layout)
        self.table = QTableView()
        self.table.setModel(self.model.model)
        print(self.model.model.rowCount())
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.resizeColumnsToContents()
        self.layout.addWidget(self.table)
        container_widget = QWidget()
        container_widget.setLayout(self.layout)
        self.setCentralWidget(container_widget)



    def create_menu(self):
        """Creates the menu that goes at the top"""
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction("Load new database")

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        exit_action.setShortcut("CTRL+E")
        file_menu.addAction(exit_action)

        insert_action = self.menuBar().addAction('&Insert')
        insert_action.triggered.connect(self.open_insert_form)

        delete_action = self.menuBar().addAction('&Delete')
        delete_action.triggered.connect(self.delete_record)


    def delete_record(self):
        pass
        logging.info("delete action clicked.")

    
    def open_insert_form(self):
        """Creates the su    # pyqt always returns false for sqlite execs that use
    # multiple statements.bmenu form used for adding a new record."""
        insert_form = create_insert_form(self)
        

class create_insert_form(QDialog):
    """Insert form for the contact book."""
    def __init__(self, parent=None):
        super().__init__(parent = parent)
        self.setWindowTitle("Insert Form")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setup_form_ui()
        self.show()
        logging.info("New insert form created")

    def setup_form_ui(self):
        # Form layout
        form_layout = QFormLayout()
        # Create insert form entry boxes.
        self.title_combo_box = QComboBox()
        self.title_combo_box.addItems(['Mr', 'Mrs', 'Ms'])
        self.gender_combo_box = QComboBox()
        self.gender_combo_box.addItems(['Male', 'Female'])
        self.first_name_entry = QLineEdit()
        self.last_name_entry = QLineEdit()
        self.email_entry = QLineEdit()
        self.phone_entry = QLineEdit()
        # Add entry boxes to form.
        form_layout.addRow("&Title:", self.title_combo_box)
        form_layout.addRow("&Gender:", self.gender_combo_box)
        form_layout.addRow("&First Name:", self.first_name_entry)
        form_layout.addRow("&Last Name:", self.last_name_entry)
        form_layout.addRow("&Email:", self.email_entry)
        form_layout.addRow("&Phone Number:", self.phone_entry)
        self.layout.addLayout(form_layout)
        print(form_layout.children())
        # Enter button.
        self.insert_confirm_button = QPushButton("Confirm")
        self.layout.addWidget(self.insert_confirm_button)

    def confirm(self):
        self.record_data = []
        




def main():
    app = QApplication(sys.argv)
    if not create_connection("contacts.sqlite"):
        sys.exit(1)
    win = contact_book_view()
    win.show()


    sys.exit(app.exec())

if __name__ == '__main__':
    main()