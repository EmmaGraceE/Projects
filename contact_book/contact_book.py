"""Basic contact book implemented in Python. Follows an MVC pattern, with the
GUI created using PyQt and the SQL database managed by sqlite."""

from os import error, name
import sys
from email_validator import validate_email, EmailNotValidError
from PyQt5.QtWidgets import *
import logging

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
        """Creates the searchbar and table."""
        # Searchbar set-up.
        search_layout = QHBoxLayout()
        self.searchbar = QLineEdit()
        self.search_combo = QComboBox()
        self.search_combo.addItems(self.model.headers)
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_db)
        search_layout.addWidget(self.searchbar)
        search_layout.addWidget(self.search_combo)
        search_layout.addWidget(self.search_button)
        self.layout.addLayout(search_layout)

        # Tableview set-up.
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
        file_menu.addAction(exit_action)
        
        insert_action = self.menuBar().addAction('&Insert')
        insert_action.triggered.connect(self.open_insert_form)

        delete_action = self.menuBar().addAction('&Delete')
        delete_action.setShortcut("DELETE")
        delete_action.triggered.connect(self.delete_record)


    def search_db(self):
        """Filters the database to only show values that match the search
        value."""
        # Filters all rows that have given value in column.
        self.model.filter_model(self.search_combo.currentText(),
        self.searchbar.text())


    def delete_record(self):
        """Gets the current row selected and then calls the delete_record function 
        to remove that record from the model and sql database."""
        row = self.table.currentIndex().row()
        if row < 0:
            return
        message_box = QMessageBox.warning(self, "Delete contact?", "Are you sure\
 you want to delete this contact?", QMessageBox.Yes | QMessageBox.No)
        if message_box == QMessageBox.Yes:
            self.model.delete_record(row)

    
    def open_insert_form(self):
        """Creates the su    # pyqt always returns false for sqlite execs that use
    # multiple statements.bmenu form used for adding a new record."""
        insert_form = create_insert_form(self)
        if insert_form.exec() == QDialog.Accepted:
            self.model.insert_record(insert_form.new_record)



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
        form_layout.addRow("&Gender:", self.gender_combo_box)
        form_layout.addRow("&Title:", self.title_combo_box)
        form_layout.addRow("&First Name:", self.first_name_entry)
        form_layout.addRow("&Last Name:", self.last_name_entry)
        form_layout.addRow("&Email:", self.email_entry)
        form_layout.addRow("&Phone Number:", self.phone_entry)
        self.layout.addLayout(form_layout)
        print(form_layout.children())
        # Enter button.
        self.insert_confirm_button = QPushButton("Confirm")
        self.insert_confirm_button.clicked.connect(self.run_validation_checks)
        self.layout.addWidget(self.insert_confirm_button)


    def run_validation_checks(self):
        """Saves the insertion form details as a dictionary"""
        self.new_record = {"gender": self.gender_combo_box.currentText(),
        "title":self.title_combo_box.currentText(), 
        "first_name": self.first_name_entry.text(),
        "last_name": self.last_name_entry.text(), 
        "email": self.email_entry.text(),
        "phone_number": self.phone_entry.text()}
        validation_tests = ValidationTests(self.new_record)

        # Load error message and allow for redo.
        error_text = (f"The following errors were found:\n\
 {validation_tests.final_error_report}\n\n Do you want to change any details?")
        message_box = QMessageBox.warning(self, "Errors found", error_text,
         QMessageBox.Yes | QMessageBox.No)
        if message_box == QMessageBox.Yes:
            return
        self.close_dialog()

    
    def close_dialog(self):
        super().accept()

class ValidationTests():
    """Contains a variety of validation tests for the input form."""
    def __init__(self, testing_record):
        """Initialise the ValidationTests class, expects the new record in the
        form of a dictionary."""
        self.errors_found = False
        self.error_reports = []
        self.name_test(testing_record["first_name"], "first name")
        self.name_test(testing_record["last_name"], "last name")
        self.email_test(testing_record["email"])
        self.phone_number_test(testing_record["phone_number"])
        if self.errors_found == True:
            self.final_error_report = '\n'.join(self.error_reports)
            

    
    def name_test(self, name, name_type):
        """Name test for both first and last names."""
        error_report = None
        for char in name:
            if char.isdigit():
                error_report = f"{name_type} has numbers"
                break
        if len(name) <=3:
            if error_report != None:
                error_report += " and is under 3 characters."
            else:
                error_report = f"{name_type} is under 3 characters."
        if error_report != None:
            self.errors_found = True
            self.error_reports.append(error_report)

    def email_test(self, email_str):
        try:
            validate_email(email_str)
        except EmailNotValidError:
            self.errors_found = True
            error_report = "The email address does not follow a valid format."
            self.error_reports.append(error_report)

    def phone_number_test(self, phone_num):
        error_report = None
        if len(phone_num) > 15:
            self.errors_found = True
            error_report = "phone number appears to be too long "
        for char in(phone_num):
            if not char.isdigit():
                if error_report == None:
                    error_report = "phone number contains non-numeric values."
                    break
                else:
                    error_report += "and has non-numeric values."
                    break
        if error_report != None:
            self.error_reports.append(error_report)

def main():
    app = QApplication(sys.argv)
    if not create_connection("contacts.sqlite"):
        sys.exit(1)
    win = contact_book_view()
    win.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()