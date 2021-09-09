
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlRecord, QSqlTableModel
import logging
import sys




from PyQt5.QtWidgets import QMessageBox
logging.basicConfig(level=logging.INFO)

class ContactModel():
    """Layer between the view and database."""
    def __init__(self):
        self.model = self.create_model()


    def create_model(self):
        """Sets up a QSLTable model for the contacts table."""
        model = QSqlTableModel()
        model.setTable('contacts')
        model.setEditStrategy(QSqlTableModel.OnFieldChange)
        model.select() # Populate model with data from SetTable table.
        self.headers = ["ID", "Gender", "Title", "First Name", "Last Name", 
        "Email", "Phone Number"]
        for count, header in enumerate(self.headers):
            model.setHeaderData(count, Qt.Horizontal, header)

        return model

    def insert_record(self, new_record_dict):
        insert_query = QSqlQuery()
        insert_query.prepare("""
        INSERT INTO contacts (gender,title,first_name,last_name,email,phone_number)
        VALUES (:gender, :title, :first_name, :last_name, :email, :phone_number);""")

        insert_query.bindValue(":gender", new_record_dict["gender"])
        insert_query.bindValue(":title", new_record_dict["title"])
        insert_query.bindValue(":first_name", new_record_dict["first_name"])
        insert_query.bindValue(":last_name", new_record_dict["last_name"])
        insert_query.bindValue(":email", new_record_dict["email"])
        insert_query.bindValue(":phone_number", new_record_dict["phone_number"])
        print(insert_query.boundValues())
        if insert_query.exec():
            logging.info("insert query made.")
            self.model.select() # reload the model with new values.
            return True
        logging.error("insert query failed.")
        return False

    def delete_record(self, row):
        """Takes a row index and then removes the corresponding record from the
        contacts database."""
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()


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


