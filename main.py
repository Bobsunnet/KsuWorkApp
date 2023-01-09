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
        self.buttons_setup()
        self.layout_setup()


    def table_view_setup(self):
        self.model = refDB.QSqlTableModel(db=refDB.db)
        self.model.setTable('refugees')
        self.model.setEditStrategy(refDB.QSqlTableModel.EditStrategy.OnFieldChange)
        self.model.sort(0, Qt.SortOrder.DescendingOrder)
        self.model.setHeaderData(1, Qt.Orientation.Horizontal, 'LSUKR')
        self.model.setHeaderData(2, Qt.Orientation.Horizontal, 'Ім\'я')
        self.model.setHeaderData(3, Qt.Orientation.Horizontal, 'Країна')
        self.model.setHeaderData(4, Qt.Orientation.Horizontal, 'Детально')
        self.model.select()

        self.table_view = QtWidgets.QTableView()
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
        # buttons_layout.addWidget(self.btn_save_all) пока нет функционала
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
        text_safe = re.sub(r'\D+', '', text) #allows only digits to go through filter
        filtered_string = 'contact_id LIKE "%{}%"'.format(text_safe)
        self.filter_model(filtered_string)

    def btn_new_row_clicked(self):
        operation_res = dbConnector.insert_into_refugees()
        if operation_res[0] == 'Success':
            self.btn_show_all_clicked()
        elif operation_res[0] == 'integrity_error':
            self.draw_new_line_error_message(operation_res[1])
        elif operation_res[0] is False:
            self.draw_general_error_message(operation_res[1])

    def draw_new_line_error_message(self, exception_message):
        error_msg = QtWidgets.QMessageBox()
        error_msg.setWindowTitle('Помилка бази даних')
        error_msg.setText('Неможливо створити новий рядок тому,\nщо є попередній з незаповеним LSUKR')
        error_msg.setInformativeText(f'{exception_message}')
        error_msg.setIcon(QtWidgets.QMessageBox.Critical)

        error_msg.exec_()

    def draw_general_error_message(self, exception_message):
        generalDB_error_msg = QtWidgets.QMessageBox()
        generalDB_error_msg.setWindowTitle('Помилка бази даних')
        generalDB_error_msg.setText(f'Помилка в роботі з базою даних')
        generalDB_error_msg.setInformativeText(f'{exception_message}')

        generalDB_error_msg.exec_()

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
        pass

    def buttons_setup(self):
        self.lbl_finder = QtWidgets.QLabel()
        self.lbl_finder.setMaximumWidth(70)
        self.lbl_finder.setText('Пошук по ID')

        self.le_finder = QtWidgets.QLineEdit()
        self.le_finder.setMaximumWidth(500)

        self.btn_finder = QtWidgets.QPushButton()
        # self.btn_finder.setMaximumWidth(100)
        self.btn_finder.setText('Знайти')
        self.btn_finder.clicked.connect(self.btn_finder_clicked)

        self.btn_new_row = QtWidgets.QPushButton()
        # self.btn_new_row.setMaximumWidth(100)
        self.btn_new_row.setText('+')
        self.btn_new_row.clicked.connect(self.btn_new_row_clicked)

        self.btn_save_all = QtWidgets.QPushButton()
        # self.btn_save_all.setMaximumWidth(100)
        self.btn_save_all.setText('Зберегти')
        self.btn_save_all.clicked.connect(self.btn_save_clicked)

        self.btn_show_all = QtWidgets.QPushButton()
        # self.btn_show_all.setMaximumWidth(100)
        self.btn_show_all.setText('Показати все')
        self.btn_show_all.clicked.connect(self.btn_show_all_clicked)

        self.btn_delete_row = QtWidgets.QPushButton()
        # self.btn_delete_row.setMaximumWidth(100)
        self.btn_delete_row.setText('Видалити')
        self.btn_delete_row.clicked.connect(self.btn_delete_row_clicked)


    def setup_ui(self):
        self.setWindowTitle('Table Main Window')
        self.setMinimumSize(800, 400)



app = QtWidgets.QApplication(sys.argv)

mainWindow = TableWindow()
mainWindow.show()

sys.exit(app.exec_())


