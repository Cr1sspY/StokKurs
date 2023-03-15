import sqlite3
import sys
from datetime import datetime

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QLineEdit, QComboBox


class Auth(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.DB = DataBase()
        self.ui = uic.loadUi('forms/auth.ui', self)
        self.setWindowIcon(QIcon('logo.ico'))
        self.ui.show()
        self.btn_enter.clicked.connect(self.auth)
        self.btn_pas.clicked.connect(self.hide_pas)
        self.hide_password = True
        worker = self.auth

    def hide_pas(self):
        self.password = self.ui.edit_password
        if self.hide_password:
            self.password.setEchoMode(QLineEdit.Normal)
            self.hide_password = False
        else:
            self.password.setEchoMode(QLineEdit.Password)
            self.hide_password = True

    def auth(self):
        log = self.ui.edit_login.text()
        password = self.ui.edit_password.text()
        data = self.DB.get_auth_info(log, password)     # если неправильные данные, то вернет False
        if data:
            self.DB.add_entry(datetime.now().strftime('%d.%m.%y %H:%M'), log, True)
            self.ui.hide()
            post, full_name = data[0]
            main_win = Window(post, full_name)
            main_win.setWindowTitle('СТОК')

            main_win.exec()

            return full_name
        else:
            self.error.setStyleSheet("color:red")  # Изменение цвета шрифта на зелёный
            self.error.setText('Ошибка входа')
            self.DB.add_entry(datetime.now().strftime('%d.%m.%y %H:%M'), log, False)


class Order(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = uic.loadUi('forms/table_ord.ui', self)
        self.setWindowIcon(QIcon('logo.ico'))

        con = QSqlDatabase.addDatabase("QSQLITE")
        con.setDatabaseName("stok.db")
        con.open()

        self.model = QSqlQueryModel()   # модель (таблица) без редактирования данных
        self.model.setQuery("SELECT * FROM order1")
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)


class Warehouse(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = uic.loadUi('forms/table_wh.ui', self)
        self.setWindowIcon(QIcon('logo.ico'))

        con = QSqlDatabase.addDatabase("QSQLITE")
        con.setDatabaseName("stok.db")
        con.open()

        self.model = QSqlQueryModel()   # модель (таблица) без редактирования данных
        self.model.setQuery("SELECT * FROM warehouse")
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)


class Service(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = uic.loadUi('forms/table_serv.ui', self)
        self.setWindowIcon(QIcon('logo.ico'))

        con = QSqlDatabase.addDatabase("QSQLITE")
        con.setDatabaseName("stok.db")
        con.open()

        self.model = QSqlQueryModel()   # модель (таблица) без редактирования данных
        self.model.setQuery("SELECT * FROM usluga")
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)


class Info(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = uic.loadUi('forms/info.ui', self)
        self.setWindowIcon(QIcon('logo.ico'))

        self.ui.info_lbl.setText('Заказ оформлен')
        # if pine == 'order':
        #     self.ui.info_lbl.setText('Заказ оформлен')
        # elif pine == 'wh':
        #     self.ui.info_lbl.setText('Запись добавлена')
        self.ui.btn_ok.clicked.connect(self.exit)

    def exit(self):
        self.close()


class Window(QDialog):
    def __init__(self, post, fullName, parent = None):
        super().__init__(parent)
        self.DB = DataBase()
        self.ui = uic.loadUi('forms/main.ui', self)
        self.setWindowIcon(QIcon('logo.ico'))
        self.ui.lbl_role.setText('Роль: ' + post + '\n' + 'ФИО: ' + fullName)
        self.ui.btn_add_order.clicked.connect(self.add_order)
        self.ui.btn_add_wh.clicked.connect(self.add_wh)
        self.ui.btn_ord.clicked.connect(self.orders)
        self.ui.btn_ord_2.clicked.connect(self.orders)
        self.ui.btn_wh.clicked.connect(self.warehouse)
        self.ui.btn_wh_2.clicked.connect(self.warehouse)
        self.ui.btn_usl.clicked.connect(self.services)
        self.ui.btn_exit.clicked.connect(self.exit)

        self.build_combobox_client()
        self.build_combobox_service()
        self.build_serv_cost()
        self.build_combobox_kompl()
        self.build_kompl_cost()

        if post == 'Кассир':
            self.ui.lbl_role.setText('Роль: ' + post)
            self.ui.lbl_name.setText(fullName)
            self.ui.stackedWidget.setCurrentIndex(0)
        elif post == 'Кладовщик':
            self.ui.lbl_role2.setText('Роль: ' + post)
            self.ui.lbl_name_2.setText(fullName)
            self.ui.stackedWidget.setCurrentIndex(1)
            # self.update_table_history()

        self.ui.usluga_box.currentIndexChanged.connect(self.update_serv_cost)
        self.ui.usluga_box.currentIndexChanged.connect(self.update_sum)
        self.update_serv_cost()
        self.ui.kompl_box.currentIndexChanged.connect(self.update_kompl_cost)
        self.ui.kompl_box.currentIndexChanged.connect(self.update_sum)
        self.update_kompl_cost()
        self.update_sum()

    def update_serv_cost(self):
        service = self.ui.usluga_box.currentText()
        self.ui.usl_cost.setText(str(self.DB.get_serv_c(service)[0][0]))

    def update_kompl_cost(self):
        kompl = self.ui.kompl_box.currentText()
        self.ui.kompl_cost.setText(str(self.DB.get_kompl_c(kompl)[0][0]))

    def update_sum(self):
        service_cost = self.ui.usl_cost.text()
        kompl_cost = self.ui.kompl_cost.text()
        summary = int(service_cost) + int(kompl_cost)
        self.ui.summary.setText(str(summary))

    def exit(self):
        self.close()
        auth = Auth()

    def report_order(self):
        s_date = self.ui.start_date.text().split('.')[::-1]
        e_date = self.ui.end_date.text().split('.')[::-1]
        data = self.DB.get_order()
        new_data = {}
        for d in data:
            if d[2].split('.')[-1::-1] <= e_date and d[2].split('.')[-1::-1] >= s_date:
                try:
                    new_data[d[2]] = str(int(new_data[d[2]])+1)
                except Exception:
                    new_data[d[2]] = '1'
        self.table_update(list(new_data.items()), ['Дата', 'Кол-во оказанных услуг'])

    def table_update(self, data, titels):
        numrows = len(data)
        numcols = len(titels)
        self.ui.tableWidget.setColumnCount(numcols)
        self.ui.tableWidget.setRowCount(numrows)
        self.ui.tableWidget.setHorizontalHeaderLabels(titels)

        for row in range(numrows):
            for column in range(numcols):
                self.ui.tableWidget.setItem(row, column, QTableWidgetItem((data[row][column])))
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def add_order(self):
        client = self.ui.client_box.currentText()
        service = self.ui.usluga_box.currentText()
        service_cost = self.ui.usl_cost.text()
        kompl = self.ui.kompl_box.currentText()
        kompl_cost = self.ui.kompl_cost.text()
        summary = int(service_cost) + int(kompl_cost)
        info = self.ui.info.text()
        worker = self.ui.lbl_name.text()

        self.DB.add_order(service, client, service_cost, kompl, kompl_cost, summary, info, worker)
        # pine = 'order'
        self.info_window()
        self.ui.info.setText('')

    def add_wh(self):
        type = self.ui.edit_type.text()
        name = self.ui.edit_name.text()
        count = self.ui.edit_count.value()
        cost = self.ui.edit_cost.value()
        worker = self.ui.lbl_name_2.text()

        self.DB.add_wh(type, name, count, cost, worker)
        # pine = 'wh'
        self.info_window()

    def orders(self):
        orders = Order()
        orders.setWindowTitle('Заказы')

        orders.exec()

    def warehouse(self):
        warehouse = Warehouse()
        warehouse.setWindowTitle('Склад')

        warehouse.exec()

    def services(self):
        services = Service()
        services.setWindowTitle('Услуги')

        services.exec()

    def build_combobox_client(self):
        clients = self.DB.get_client()
        self.client_box.clear()
        if self.client_box is not None:
            self.client_box.addItems(clients)

    def build_combobox_service(self):
        services = self.DB.get_service()
        self.usluga_box.clear()
        if self.usluga_box is not None:
            self.usluga_box.addItems(services)

    def build_serv_cost(self):
        self.usl_cost.clear()
        self.ui.usl_cost.setText(str(self.DB.get_serv_c(self.ui.usluga_box.currentText())))
        self.usl_cost.update()
        print()

    def build_combobox_kompl(self):
        kompls = self.DB.get_kompl()
        self.kompl_box.clear()
        if self.kompl_box is not None:
            self.kompl_box.addItems(kompls)

    def build_kompl_cost(self):
        self.kompl_cost.clear()
        self.ui.kompl_cost.setText(str(self.DB.get_kompl_c(self.ui.kompl_box.currentText())))
        self.kompl_cost.update()
        print()

    def info_window(self):
        info = Info()
        info.setWindowTitle('Информация')

        info.exec()


class DataBase():
    def __init__(self):
        self.con = sqlite3.connect('stok.db')

    def get_order(self):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM order1")
        return cur.fetchall()

    def get_warehouse(self):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM warehouse")
        return cur.fetchall()

    def add_entry(self, time, log, try_entry):
        cur = self.con.cursor()
        cur.execute("INSERT INTO history VALUES (?,?,?)", (time, log, try_entry))
        self.con.commit()

    def get_auth_info(self, log, password):
        cur = self.con.cursor()
        cur.execute(f'SELECT post, full_name FROM worker WHERE login="{log}" and password="{password}"')
        data = cur.fetchall()
        cur.close()
        if data != []:
            return data
        else:
            return False

    def add_order(self, service, client, serv_cost, kompl, kompl_cost, summ, info,worker):
        now = datetime.now()
        times = now.strftime("%H:%M")
        date = now.strftime("%d.%m.20%y")
        id = 1
        try:
            cur = self.con.cursor()
            cur.execute("""INSERT INTO order1 VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?)""", (date, times, client, service,
                                                                                    serv_cost, kompl, kompl_cost, summ,
                                                                                    info, "Новый заказ", worker))
            self.con.commit()
            cur.close()
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

    def add_wh(self, type, name, count, cost, worker):
        now = datetime.now()
        id = 1
        try:
            cur = self.con.cursor()
            cur.execute("""INSERT INTO warehouse VALUES (NULL,?,?,?,?,?)""", (type, name, count, cost, worker))
            self.con.commit()
            cur.close()
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

    def get_client(self):
        clients = []
        cursor = self.con.cursor()
        cursor.execute(f"SELECT `name` FROM client")
        rows = cursor.fetchall()

        for i in rows:
            clients.append(str(i)[2:-3])
        return clients

    def get_service(self):
        services = []
        cursor = self.con.cursor()
        cursor.execute(f"SELECT `Название` FROM usluga")
        rows = cursor.fetchall()

        for i in rows:
            services.append(str(i)[2:-3])
        return services

    def get_serv_c(self, service):
        cur = self.con.cursor()
        cur.execute(f'SELECT Цена FROM usluga WHERE Название="{service}"')
        serv_c = cur.fetchall()
        cur.close()
        return serv_c

    def get_kompl(self):
        kompls = []
        cursor = self.con.cursor()
        cursor.execute(f"SELECT `Наименование` FROM warehouse")
        rows = cursor.fetchall()

        for i in rows:
            kompls.append(str(i)[2:-3])
        return kompls

    def get_kompl_c(self, kompl):
        cur = self.con.cursor()
        cur.execute(f'SELECT Стоимость FROM warehouse WHERE Наименование="{kompl}"')
        kompl_c = cur.fetchall()
        cur.close()
        return kompl_c


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Auth()

    app.exec()

