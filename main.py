from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import dbConnector
import sys
import re
import refDB as rdb


class TableWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(TableWindow, self).__init__()
        self.setup_ui()
        self.table_view_setup()
        self.btns_setup()


    def table_view_setup(self):
        self.table_view = QtWidgets.QTableView(self)
        # self.setCentralWidget(self.table_view)
        self.table_view.setGeometry(0, 35, 800,365)

        self.model = rdb.QSqlTableModel(db=rdb.db)
        self.model.setTable('refugees')
        self.model.setEditStrategy(rdb.QSqlTableModel.EditStrategy.OnManualSubmit)
        self.model.sort(0, Qt.SortOrder.DescendingOrder)
        self.model.select()

        self.table_view.setModel(self.model)
        self.table_view.resizeColumnsToContents()
        self.table_view.resizeRowsToContents()


    def filter_model(self, s):
        self.model.setFilter(s)

    def btn_finder_clicked(self):
        text = self.le_finder.text()
        text_safe = re.sub(r'\D+', '', text)
        filtered_string = 'contact_id LIKE "%{}%"'.format(text_safe)
        self.filter_model(filtered_string)

    def btn_new_row_clicked(self):
        dbConnector.insert_into_refugees()
        self.btn_show_all_clicked()

    def btn_show_all_clicked(self):
        self.le_finder.setText('')
        self.btn_finder_clicked()

    def btn_delete_row_clicked(self):
        indexes = self.table_view.selectionModel().selectedRows()
        contact_id = None
        for index in sorted(indexes):
            contact_id = self.model.data(self.model.index(index.row(), 1))
        self.delete_row(contact_id)

    def delete_row(self, contact_id):
        dbConnector.delete_row(contact_id)
        self.btn_show_all_clicked()

    def btn_save_clicked(self):
        self.model.submitAll()

    def btns_setup(self):
        self.lbl_finder = QtWidgets.QLabel(self)
        self.lbl_finder.setGeometry(4,0, 50, 30)
        self.lbl_finder.setText('Search')

        self.le_finder = QtWidgets.QLineEdit(self)
        self.le_finder.setGeometry(51, 0, 70, 30)

        self.btn_finder = QtWidgets.QPushButton(self)
        self.btn_finder.setGeometry(130,0, 40, 30)
        self.btn_finder.setText('FInd')
        self.btn_finder.clicked.connect(self.btn_finder_clicked)

        self.btn_new_row = QtWidgets.QPushButton(self)
        self.btn_new_row.setGeometry(190, 3, 40, 24)
        self.btn_new_row.setText('+')
        self.btn_new_row.clicked.connect(self.btn_new_row_clicked)

        self.btn_save_all = QtWidgets.QPushButton(self)
        self.btn_save_all.setGeometry(240, 0, 40, 30)
        self.btn_save_all.setText('Save')
        self.btn_save_all.clicked.connect(self.btn_save_clicked)

        self.btn_show_all = QtWidgets.QPushButton(self)
        self.btn_show_all.setGeometry(290, 0, 40, 30)
        self.btn_show_all.setText('Show')
        self.btn_show_all.clicked.connect(self.btn_show_all_clicked)

        self.btn_delete_row = QtWidgets.QPushButton(self)
        self.btn_delete_row.setGeometry(340, 0, 40, 30)
        self.btn_delete_row.setText('Delete')
        self.btn_delete_row.clicked.connect(self.btn_delete_row_clicked)


    def setup_ui(self):
        self.setWindowTitle('Table Main Window')
        self.setMinimumSize(800, 400)



app = QtWidgets.QApplication(sys.argv)

mainWindow = TableWindow()
mainWindow.show()

sys.exit(app.exec_())


