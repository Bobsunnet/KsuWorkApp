from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import dbConnector
import sys
import re
import refDB


class TableWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(TableWindow, self).__init__()
        self.setup_ui()
        self.table_view_setup()
        self.btns_setup()
        self.layout_setup()


    def table_view_setup(self):
        self.table_view = QtWidgets.QTableView()
        # self.setCentralWidget(self.table_view)
        # self.table_view.setGeometry(0, 35, 800,365)

        self.model = refDB.QSqlTableModel(db=refDB.db)
        self.model.setTable('refugees')
        self.model.setEditStrategy(refDB.QSqlTableModel.EditStrategy.OnFieldChange)
        self.model.sort(0, Qt.SortOrder.DescendingOrder)
        self.model.select()

        self.table_view.setModel(self.model)
        self.table_view.resizeColumnsToContents()
        self.table_view.resizeRowsToContents()

        # self.table_view.selectionModel().selectionChanged.connect(self.cell_changed)
        self.table_view.selectionModel().currentChanged.connect(self.current_cell_changed)

    def layout_setup(self):
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout_widget = QtWidgets.QWidget()

        main_Vlayout = QtWidgets.QVBoxLayout()
        main_Vlayout.addWidget(buttons_layout_widget)
        main_Vlayout.addWidget(self.table_view)

        buttons_layout.addWidget(self.lbl_finder)
        buttons_layout.addWidget(self.le_finder)
        buttons_layout.addWidget(self.btn_finder)
        buttons_layout.addWidget(self.btn_new_row)
        buttons_layout.addWidget(self.btn_save_all)
        buttons_layout.addWidget(self.btn_show_all)
        buttons_layout.addWidget(self.btn_delete_row)

        buttons_layout_widget.setLayout(buttons_layout)

        main_widget = QtWidgets.QWidget()
        main_widget.setLayout(main_Vlayout)

        self.setCentralWidget(main_widget)


    def current_cell_changed(self, current, previous):
        cell_value = self.model.data(self.model.index(previous.row(), previous.column()))
        current_row = previous.row()
        contact_ids = [self.model.data(self.model.index(row, 1)) for row in range(self.model.rowCount())
                       if row != current_row]
        if cell_value in contact_ids:
            self.btn_show_all_clicked()


    # def cell_changed(self, selected, deselected):
    #     for cell in deselected.indexes():
    #         print(f'cell row: {cell.row()}, column: {cell.column()} changed')

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
        self.lbl_finder = QtWidgets.QLabel()
        # self.lbl_finder.setGeometry(4,0, 70, 30)
        self.lbl_finder.setText('Пошук по ID')

        self.le_finder = QtWidgets.QLineEdit()
        # self.le_finder.setGeometry(71, 0, 70, 30)

        self.btn_finder = QtWidgets.QPushButton()
        # self.btn_finder.setGeometry(150,0, 60, 30)
        self.btn_finder.setText('Знайти')
        self.btn_finder.clicked.connect(self.btn_finder_clicked)

        self.btn_new_row = QtWidgets.QPushButton()
        # self.btn_new_row.setGeometry(220, 3, 40, 24)
        self.btn_new_row.setText('+')
        self.btn_new_row.clicked.connect(self.btn_new_row_clicked)

        self.btn_save_all = QtWidgets.QPushButton()
        # self.btn_save_all.setGeometry(270, 0, 60, 30)
        self.btn_save_all.setText('Зберегти')
        self.btn_save_all.clicked.connect(self.btn_save_clicked)

        self.btn_show_all = QtWidgets.QPushButton()
        # self.btn_show_all.setGeometry(340, 0, 80, 30)
        self.btn_show_all.setText('Показати все')
        self.btn_show_all.clicked.connect(self.btn_show_all_clicked)

        self.btn_delete_row = QtWidgets.QPushButton()
        # self.btn_delete_row.setGeometry(430, 0, 60, 30)
        self.btn_delete_row.setText('Видалити')
        self.btn_delete_row.clicked.connect(self.btn_delete_row_clicked)


    def setup_ui(self):
        self.setWindowTitle('Table Main Window')
        self.setMinimumSize(800, 400)



app = QtWidgets.QApplication(sys.argv)

mainWindow = TableWindow()
mainWindow.show()

sys.exit(app.exec_())


