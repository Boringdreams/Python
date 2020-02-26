from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
import sys,sqlite3,time
from crypt import *
from backupp import *

import os

class InsertDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(InsertDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Регистрация")

        self.setWindowTitle("Добавить клиента")
        self.setFixedWidth(300)
        self.setFixedHeight(250)

        self.QBtn.clicked.connect(self.addclient)

        layout = QVBoxLayout()

        self.nameinput = QLineEdit()
        self.nameinput.setPlaceholderText("Имя")
        layout.addWidget(self.nameinput)

        self.branchinput = QComboBox()
        self.branchinput.addItem("Выбор 1")
        self.branchinput.addItem("Выбор 2")
        self.branchinput.addItem("Выбор 3")
        self.branchinput.addItem("Выбор 4")
        layout.addWidget(self.branchinput)

        self.seminput = QComboBox()
        self.seminput.addItem("1")
        self.seminput.addItem("2")
        self.seminput.addItem("3")
        layout.addWidget(self.seminput)

        self.mobileinput = QLineEdit()
        self.mobileinput.setPlaceholderText("Мобильный номер")
        layout.addWidget(self.mobileinput)

        self.addressinput = QLineEdit()
        self.addressinput.setPlaceholderText("Адрес")
        layout.addWidget(self.addressinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def addclient(self):

        name = ""
        branch = ""
        sem = -1
        mobile = -1
        address = ""

        name = self.nameinput.text()
        branch = self.branchinput.itemText(self.branchinput.currentIndex())
        sem = self.seminput.itemText(self.seminput.currentIndex())
        mobile = self.mobileinput.text()
        address = self.addressinput.text()
        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            self.c.execute("INSERT INTO client (name,branch,sem,Mobile,address) VALUES (?,?,?,?,?)",(name,branch,sem,mobile,address))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(),'Успешно','Заказ успешно добавлен')
            self.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Ошибка', 'Заказ не добавлен')

class SearchDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(SearchDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Поиск")

        self.setWindowTitle("Поиск клиента")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.searchclient)
        layout = QVBoxLayout()

        self.searchinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.searchinput.setValidator(self.onlyInt)
        self.searchinput.setPlaceholderText("ID")
        layout.addWidget(self.searchinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def searchclient(self):

        searchroll = ""
        searchroll = self.searchinput.text()
        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            result = self.c.execute("SELECT * from client WHERE roll="+str(searchroll))
            row = result.fetchone()
            serachresult = "ID : "+str(row[0])+'\n'+"Имя : "+str(row[1])+'\n'+"Выбор : "+str(row[2])+'\n'+"Ячейка : "+str(row[3])+'\n'+"Адрес : "+str(row[4])
            QMessageBox.information(QMessageBox(), 'Информация', serachresult)
            self.conn.commit()
            self.c.close()
            self.conn.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Ошибка', 'Клиент не найден')

class DeleteDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(DeleteDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Удалить")

        self.setWindowTitle("Удалить клиента")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.deleteclient)
        layout = QVBoxLayout()

        self.deleteinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.deleteinput.setValidator(self.onlyInt)
        self.deleteinput.setPlaceholderText("ID")
        layout.addWidget(self.deleteinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def deleteclient(self):

        delid = ""
        delid = self.deleteinput.text()
        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            self.c.execute("DELETE from client WHERE roll="+str(delid))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(),'Успешно','Удаление успешно')
            self.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Ошибка', 'Невозможно удалить данного клиента')

class LoginDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(LoginDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(400)
        self.setFixedHeight(150)

        layout = QVBoxLayout()

        self.logininput = QLineEdit()
        self.logininput.setEchoMode(QLineEdit.Password)
        self.logininput.setPlaceholderText("Введите логин")
        self.passinput = QLineEdit()
        self.passinput.setEchoMode(QLineEdit.Password)
        self.passinput.setPlaceholderText("Введите пароль")
        self.QBtn = QPushButton()
        self.QBtn.setText("Вход")
        self.setWindowTitle('Login')
        self.QBtn.clicked.connect(self.login)

        title = QLabel("Вход")
        font = title.font()
        font.setPointSize(16)
        title.setFont(font)

        layout.addWidget(title)
        layout.addWidget(self.logininput)
        layout.addWidget(self.passinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def login(self):
        if(self.passinput.text() == "admin" and
            self.logininput.text() == "admin"):
            self.accept()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Неправильный логин или пароль')


class CryptDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(CryptDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(300)
        self.setFixedHeight(100)

        self.setWindowTitle("Зашифровать")
        self.cryptText = QLabel("Файл успешно зашифрован")
        self.grid=QGridLayout(self)
        self.grid.addWidget(self.cryptText,0,0)

        Crypt_db(self)

class BackupDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(BackupDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(300)
        self.setFixedHeight(100)
        try:
            checker = open('encrypt.enc','r')
            self.setWindowTitle("Резервное копирование")
            self.backupText = QLabel("Резервная копия успешно создана")
            backup_db(self)
        except FileNotFoundError:
            self.setWindowTitle("Ошибка")
            self.backupText = QLabel("Нет зашифрованного файла")        
        self.grid=QGridLayout(self)
        self.grid.addWidget(self.backupText,0,0)    

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.conn = sqlite3.connect("database.db")
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS client(roll INTEGER PRIMARY KEY AUTOINCREMENT ,name TEXT,branch TEXT,sem INTEGER,mobile INTEGER,address TEXT)")
        self.c.close()

        file_menu = self.menuBar().addMenu("&Файл")

        self.setWindowTitle("База наших клиентов")

        self.setMinimumSize(800, 600)
        
        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(4)
        #Размер колонок
        self.tableWidget.horizontalHeader().setSectionResizeMode(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        #Автораcширение колонки
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(True)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(("ID", "Имя","Мобильный номер","Адрес"))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        btn_ac_adduser = QAction(QIcon("icon/add.png"), "Добавить клиента", self)
        btn_ac_adduser.triggered.connect(self.insert)
        btn_ac_adduser.setStatusTip("Добавить клиента")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresh = QAction(QIcon("icon/refresh.png"),"Обновить",self)
        btn_ac_refresh.triggered.connect(self.loaddata)
        btn_ac_refresh.setStatusTip("Обновить таблицу")
        toolbar.addAction(btn_ac_refresh)

        btn_ac_search = QAction(QIcon("icon/search.png"), "Поиск", self)
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Поиск клиента")
        toolbar.addAction(btn_ac_search)

        btn_ac_delete = QAction(QIcon("icon/trash.png"), "Удалить", self)
        btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Удалить клиента")
        toolbar.addAction(btn_ac_delete)

        btn_ac_crypt = QAction(QIcon("icon/lock.png"), "Зашифровать базу данных", self)
        btn_ac_crypt.triggered.connect(self.crypt)
        btn_ac_crypt.setStatusTip("Зашифровать базу данных")
        toolbar.addAction(btn_ac_crypt)

        btn_ac_backup = QAction(QIcon("icon/cloud.png"), "Сделать резервную копию", self)
        btn_ac_backup.triggered.connect(self.backup)
        btn_ac_backup.setStatusTip("Сделать резервную копию")
        toolbar.addAction(btn_ac_backup)

        adduser_action = QAction(QIcon("icon/add.png"),"Выбрать клиента", self)
        adduser_action.triggered.connect(self.insert)
        file_menu.addAction(adduser_action)

        searchuser_action = QAction(QIcon("icon/search.png"), "Поиск клиента", self)
        searchuser_action.triggered.connect(self.search)
        file_menu.addAction(searchuser_action)

        deluser_action = QAction(QIcon("icon/trash.png"), "Удалить", self)
        deluser_action.triggered.connect(self.delete)
        file_menu.addAction(deluser_action)


    def loaddata(self):
        self.connection = sqlite3.connect("database.db")
        query = "SELECT roll,name,mobile,address FROM client"
        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        #Формирование таблицы
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number,QTableWidgetItem(str(data)))
        self.connection.close()

    def handlePaintRequest(self, printer):
        document = QTextDocument()
        cursor = QTextCursor(document)
        model = self.table.model()
        table = cursor.insertTable(
            model.rowCount(), model.columnCount())
        for row in range(table.rows()):
            for column in range(table.columns()):
                cursor.insertText(model.item(row, column).text())
                cursor.movePosition(QTextCursor.NextCell)
        document.print_(printer)

    def insert(self):
        dlg = InsertDialog()
        dlg.exec_()

    def delete(self):
        dlg = DeleteDialog()
        dlg.exec_()

    def search(self):
        dlg = SearchDialog()
        dlg.exec_()

    def crypt(self):
        dlg = CryptDialog()
        dlg.exec_()

    def backup(self):
        dlg = BackupDialog()
        dlg.exec_()
        

app = QApplication(sys.argv)
passdlg = LoginDialog()
if(passdlg.exec_() == QDialog.Accepted):
    window = MainWindow()
    window.show()
    window.loaddata()
sys.exit(app.exec_())