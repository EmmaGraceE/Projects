"""Basic contact book implemented in Python. Follows an MVC pattern, with the
GUI created using PyQt and the SQL database managed by sqlite."""

import sys
from PyQt5.QtWidgets import QAction, QApplication, QShortcut, QVBoxLayout, QWidget, QToolBar
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence


class contact_book_view(QMainWindow):
    """Creates the view used for the contact book."""
    def __init__(self):
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
        insert_action.triggered.connect(self.insert_form)
    
    def insert_form(self):
        """Creates the submenu form used for adding a new record."""
        print("print")



def main():
    contact_book_app = QApplication(sys.argv)
    view = contact_book_view()
    view.show()

    sys.exit(contact_book_app.exec())

if __name__ == '__main__':
    main()