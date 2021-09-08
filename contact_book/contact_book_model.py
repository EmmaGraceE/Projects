from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
import logging
import sys

from PyQt5.QtWidgets import QMessageBox
logging.basicConfig(level=logging.INFO)

class ContactModel():
    """Layer between the view and database."""
    def __init__(self):
        self.model = self.create_model()


    def create_model(self):
        model = QSqlTableModel()
        model.setTable('contacts')
        model.setEditStrategy(QSqlTableModel.OnFieldChange)
        model.select() # Populate model with data from SetTable table.
        self.headers = ["ID", "Gender", "Title", "First Name", "Last Name", "Email", "Phone Number"]
        for count, header in enumerate(self.headers):
            model.setHeaderData(count, Qt.Horizontal, header)
        return model


def create_table():
    create_table_query = QSqlQuery()
    result = create_table_query.exec(
        """CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            gender VARCHAR(1),
            title VARCHAR(3),
            first_name VARCHAR(40), 
            last_name VARCHAR(40),
            email VARCHAR(40), 
            phone_number INTEGER(20)
            )
            """
    )
    logging.info(f"query status: {result}")
    
def create_connection(db_path):
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(db_path)
    if not connection.open():
        QMessageBox.warning(
            None,
            "RP Contact",
            f"Database Error: {connection.lastError().text()}",
        )
        return False
    create_table()
    return True


