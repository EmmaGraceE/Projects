"""Basic contact book implemented in Python. Follows an MVC pattern, with the
GUI created using PyQt and the SQL database managed by sqlite."""

import sys
from PyQt5.QtWidgets import QAction, QApplication, QDialog, QLineEdit, QShortcut, QVBoxLayout, QWidget, QToolBar
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QFormLayout
import logging

logging.basicConfig(level=logging.INFO)
class contact_book_view(QMainWindow):
    """Creates the view used for the contact book."""
    def __init__(self, parent = None):
        super().__init__() 
        self.setWindowTitle("Contact Book")
        self.general_layout = QVBoxLayout()
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.create_menu()

    def create_menu(self):
        """Creates the menu that goes at the top"""
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction("Load new database")

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        exit_action.setShortcut("CTRL+E")
        file_menu.addAction(exit_action)

        insert_action = self.menuBar().addAction("&Insert")
        insert_action.triggered.connect(self.open_insert_form)
    
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