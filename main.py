from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import dbConnector
import sys
import re
import sql_pyqt
import stylesheet
from backupper import write_backup


HEADERS_NAMES = ['LSUKR', 'Ім\'я', 'Країна', 'Детально']


class TextWidget(QtWidgets.QTextEdit):
    def __init__(self):
        super().__init__()
        self.linked_cell = None

    def link_cell(self, cell: tuple):
        self.linked_cell = cell

    def get_linked_cell(self):
        return self.linked_cell


class TableWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(TableWindow, self).__init__()
        self.setup_ui()
        self.table_view_setup()
        self.widgets_setup()
        self.layout_setup()

        write_backup()

    def table_view_setup(self):
        self.model = sql_pyqt.QSqlTableModel(db=sql_pyqt.db)
        self.model.setTable('refugees')

        self.model.setEditStrategy(sql_pyqt.QSqlTableModel.EditStrategy.OnFieldChange)
        self.model.sort(0, Qt.SortOrder.DescendingOrder)
        # self.model.removeColumns(5,1)

        for i, name in enumerate(HEADERS_NAMES):
            self.model.setHeaderData(i+1, Qt.Orientation.Horizontal, name)

        self.model.select()

        self.table_view = QtWidgets.QTableView()
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setStyleSheet(stylesheet.horizontal_header)
        self.table_view.verticalHeader().setStyleSheet(stylesheet.vertical_header)

        self.table_view.hideColumn(0)
        # self.table_view.hideColumn(5)

        # адаптивность ширини столбцов
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)


        #при нажатии на ячейку срабатывает ивентлуп
        self.table_view.selectionModel().currentChanged.connect(self.cell_highlighted)

    def widgets_setup(self):
        # _______________________________________BUTTONS_LAYER__________________________________
        self.label_finder = QtWidgets.QLabel()
        self.label_finder.setMaximumWidth(90)
        self.label_finder.setStyleSheet(stylesheet.label_finder)
        self.label_finder.setText('Пошук по ID')

        self.lnedit_finder = QtWidgets.QLineEdit()
        self.lnedit_finder.setStyleSheet(stylesheet.line_edit)
        self.lnedit_finder.setPlaceholderText('LSUKR')
        self.lnedit_finder.textChanged.connect(self.btn_finder_clicked)
        self.lnedit_finder.setMaximumWidth(500)

        self.btn_finder = QtWidgets.QPushButton()
        self.btn_finder.setStyleSheet(stylesheet.button_general)
        self.btn_finder.setText('Знайти')
        self.btn_finder.clicked.connect(self.btn_finder_clicked)

        self.btn_new_row = QtWidgets.QPushButton()
        self.btn_new_row.setStyleSheet(stylesheet.button_general)
        self.btn_new_row.setText('+')
        self.btn_new_row.clicked.connect(self.btn_new_row_clicked)

        self.btn_save_all = QtWidgets.QPushButton()
        self.btn_save_all.setStyleSheet(stylesheet.button_general)
        self.btn_save_all.setText('Зберегти')
        self.btn_save_all.clicked.connect(self.btn_save_clicked)

        self.btn_show_all = QtWidgets.QPushButton()
        self.btn_show_all.setStyleSheet(stylesheet.button_general)
        self.btn_show_all.setText('Показати все')
        self.btn_show_all.clicked.connect(self.btn_show_all_clicked)

        self.btn_delete_row = QtWidgets.QPushButton()
        self.btn_delete_row.setStyleSheet(stylesheet.button_delete)
        self.btn_delete_row.setText('Видалити')
        self.btn_delete_row.clicked.connect(self.btn_delete_row_clicked)

        # __________________________________TEXT_LAYER_________________________
        self.text_widget = TextWidget()
        # self.text_widget.setMaximumHeight(90)
        self.text_widget.cursorPositionChanged.connect(self.change_cell_text)
        self.text_widget.setAcceptRichText(False)
        self.text_widget.setStyleSheet(stylesheet.text_edit)

        self.label_info = QtWidgets.QLabel()
        self.label_info.setText('К-ть рядків: \n\n\nДата редагування: \n')
        self.label_info.setStyleSheet(stylesheet.label_info)

        self.lnedit_date = QtWidgets.QLineEdit()
        self.lnedit_date.setStyleSheet(stylesheet.line_edit)
        # self.lnedit_date.setPlaceholderText('date')
        self.lnedit_date.returnPressed.connect(self.change_date_value)
        self.lnedit_date.setMaximumWidth(120)


    def layout_setup(self):
        #________________________________BUTTONS_LAYOUT___________________________________
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.setContentsMargins(10,10,300,10)
        # buttons_layout.setSpacing(10)

        buttons_layout.addWidget(self.label_finder)
        buttons_layout.addWidget(self.lnedit_finder)
        buttons_layout.addWidget(self.btn_finder)
        buttons_layout.addWidget(self.btn_new_row)
        # buttons_layout.addWidget(self.btn_save_all) пока нет функционала
        buttons_layout.addWidget(self.btn_show_all)
        buttons_layout.addWidget(self.btn_delete_row)
        # ________________________________TEXTWIDGET_LAYOUT___________________________________
        text_edit_layout = QtWidgets.QHBoxLayout()
        text_edit_layout.setContentsMargins(0, 10, 300, 10)

        label_date_layout = QtWidgets.QVBoxLayout()
        label_date_layout.addWidget(self.lnedit_date)
        label_date_layout.addWidget(self.label_info)

        text_edit_layout.addLayout(label_date_layout)
        text_edit_layout.addWidget(self.text_widget)

        #________________________________MAIN_LAYOUT___________________________________________
        main_layout = QtWidgets.QVBoxLayout()

        main_layout.addLayout(buttons_layout)
        main_layout.addLayout(text_edit_layout)
        main_layout.addWidget(self.table_view)

        main_layout_widget = QtWidgets.QWidget()
        main_layout_widget.setLayout(main_layout)

        self.setCentralWidget(main_layout_widget)

    # __________________________________ LOGIC _______________________________________

    def cell_highlighted(self, current, previous):
        current_row, current_col = current.row(), current.column()
        self.text_widget.link_cell((current_row, current_col))
        #меняем текст в виджете
        self.change_text_widget(current_row, current_col)
        self.draw_label_info(current_row)
        # self.label_cell_change(current_row, current_col)

        self._chek_lsukr(previous.row(), previous.column())

    def _chek_lsukr(self, row, col):
        cell_value = self.model.data(self.model.index(row, col))
        current_row = row
        # создаем список всех LSUKR и сравниваем есть ли уже такой как в измененной ячейке
        lsukr_list = [self.model.data(self.model.index(row, 1)) for row in range(self.model.rowCount())
                      if row != current_row]
        if cell_value in lsukr_list:
            self.btn_show_all_clicked()

    def draw_label_info(self, row):
        date_record = self.model.data(self.model.index(row,5))
        self.lnedit_date.setText(str(date_record))
        self.label_info.setText(f'К-ть рядків: \n{self.model.rowCount()}\n\nДата редагування: \n{date_record}')

    def change_text_widget(self, row, col):
        text = self.model.data(self.model.index(row, col))
        self.text_widget.setText(str(text))

    def get_linked_cell(self):
        return self.text_widget.get_linked_cell()

    def change_cell_text(self):
        text = self.text_widget.toPlainText()
        linked_cell = self.get_linked_cell()
        if linked_cell:
            row, col = linked_cell
            self.model.setData(self.model.index(row, col), text)

    def change_date_value(self):
        date = self.lnedit_date.text()
        linked_cell = self.get_linked_cell()
        if linked_cell:
            row = linked_cell[0]
            self.model.setData(self.model.index(row, 5),date)
            self.draw_label_info(row)

    def filter_model(self, s):
        self.model.setFilter(s)

    def btn_finder_clicked(self):
        text = self.lnedit_finder.text()
        text_safe = re.sub(r'\D+', '', text)  # allows only digits to go through filter
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
        self.lnedit_finder.setText('')
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

    def setup_ui(self):
        self.setWindowTitle('Table Main Window')
        self.setMinimumSize(1000, 600)


app = QtWidgets.QApplication(sys.argv)

mainWindow = TableWindow()
mainWindow.show()

sys.exit(app.exec_())
