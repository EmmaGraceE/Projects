"""Basic contact book implemented in Python. Follows an MVC pattern, with the
GUI created using PyQt and the SQL database managed by sqlite."""

import sys
from PyQt5.QtWidgets import QAction, QApplication, QDialog, QLabel, QLineEdit, QVBoxLayout, QWidget, QToolBar
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidget, QComboBox
from PyQt5.QtWidgets import QFormLayout, QGridLayout
import logging
from PyQt5.QtWidgets import QCheckBox

logging.basicConfig(level=logging.INFO)


class contact_book_view(QMainWindow):
    """Creates the view used for the contact book."""
    def __init__(self, parent = None):
        super().__init__() 
        self.setWindowTitle("Contact Book")
        self.general_layout = QGridLayout()
        self.create_general_ui()
        self.create_menu()

    def create_general_ui(self):
        self.table = QTableWidget()
        self.general_layout.addWidget(self.table, 1, 0)
        central_widget = QWidget()
        central_widget.setLayout(self.general_layout)
        self.setCentralWidget(central_widget)



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
        """Creates the submenu form used for adding a new record."""
        insert_form = create_insert_form(self)
        

class create_insert_form(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent = parent)
        self.setWindowTitle("Insert Form")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setup_form()
        self.show()
        logging.info("New insert form created")

    def setup_form(self):

        form_layout = QFormLayout()
        # Combo boxes for gender and title.
        title_combo_box = QComboBox()
        title_combo_box.addItems(['Mr', 'Mrs', 'Ms'])
        form_layout.addRow("Title:", title_combo_box)
        gender_combo_box = QComboBox()
        gender_combo_box.addItems(['Male', 'Female'])
        form_layout.addRow("Gender:", gender_combo_box)
        # Manual entry rows.
        form_layout.addRow("First Name:", QLineEdit())
        form_layout.addRow("Last Name:", QLineEdit())
        form_layout.addRow("Email:", QLineEdit())
        
        self.layout.addLayout(form_layout)

def main():
    contact_book_app = QApplication(sys.argv)
    view = contact_book_view()
    view.show()

    sys.exit(contact_book_app.exec())

if __name__ == '__main__':
    main()