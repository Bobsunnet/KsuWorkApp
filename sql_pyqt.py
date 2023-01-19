from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from config import *
import os

basedir = os.path.dirname(__file__)

db = QSqlDatabase("QSQLITE")
db.setDatabaseName(os.path.join(basedir, DB_NAME))
db.open()







