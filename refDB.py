from PyQt5.QtSql import QSqlDatabase, QSqlTableModel

import os

basedir = os.path.dirname(__file__)

db = QSqlDatabase("QSQLITE")
db.setDatabaseName(os.path.join(basedir, 'refuges.db'))
db.open()







