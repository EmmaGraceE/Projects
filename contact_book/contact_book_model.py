from PyQt5.QtCore import qsrand
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import logging
import sys
logging.basicConfig(level=logging.INFO)

class contact_book_model():
    def __init__(self):
        create_connection()



def create_table():
    create_table_query = QSqlQuery()
    result = create_table_query.exec(
        """CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            title VARCHAR(3),
            gender VARCHAR(1),
            first_name VARCHAR(40), 
            last_name VARCHAR(40),
            email VARCHAR(40), 
            phone_number INTEGER(20)
            )
            """
    )

    
def create_connection():
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName("contacts.sqlite")

    if connection.open() == False:
        logging.error("connection failed")
    db = QSqlDatabase.database()
    logging.info(f"database connected: {db.connectionName()}")
    create_table()
    logging.info(f"tables: {db.tables()}")


cb_model = contact_book_model()