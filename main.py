from PyQt5.QtWidgets import *
import mysql.connector
from stylesheet import *


def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='k7119zamu',
            database='telegram'
        )
        return connection
    except mysql.connector.Error as e:
        print('Xato sodir bo‘ldi:', e)


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.logins = list()

        self.setMinimumSize(400, 500)

        login_label = QLabel('Login')
        password_label = QLabel("Password")

        login_label.setMinimumWidth(100)
        password_label.setMinimumWidth(100)

        ok_btn = QPushButton('Ok')

        self.login_line = QLineEdit()
        self.password_line = QLineEdit()

        self.password_line.setEchoMode(QLineEdit.Password)

        login_layout = QHBoxLayout()
        login_layout.addWidget(login_label)
        login_layout.addWidget(self.login_line)

        password_layout = QHBoxLayout()
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_line)

        main_layout = QVBoxLayout()
        main_layout.addLayout(login_layout)
        main_layout.addLayout(password_layout)
        main_layout.addWidget(ok_btn)

        self.login_line.setStyleSheet(login_line_style)
        self.password_line.setStyleSheet(password_line_style)
        login_label.setStyleSheet(label_style)
        password_label.setStyleSheet(label_style)
        ok_btn.setStyleSheet(button_style)

        ok_btn.clicked.connect(self.open_new_window)

        widget = QWidget()
        widget.setLayout(main_layout)

        self.setCentralWidget(widget)

    def open_new_window(self):
        login = self.login_line.text()
        password = self.password_line.text()

        conn = get_connection()
        curs = conn.cursor()

        curs.execute('SELECT * FROM whatsapp WHERE login = %s AND password = %s', (login, password))
        informations = curs.fetchone()

        curs.close()
        conn.close()

        if informations:
            print('Login muvaffaqiyatli amalga oshirildi.')
            new_window = NewWindow()
            new_window.show()
            self.logins.append(new_window)
        else:
            print('Login yoki parol noto\'g\'ri.')
            QMessageBox.warning(self, 'Xato', 'Login yoki parol noto\'g\'ri.')


class NewWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(700, 900)

        self.receiver = QLineEdit()
        self.receiver.setPlaceholderText('Qabul qiluvchi nickneymini kiriting: ')

        self.inchat = QTextEdit()
        self.outchat = QTextEdit()

        inchat_label = QLabel('Sizga kelgan habar')
        outchat_label = QLabel('Siz yuboradigan habar')

        send_btn = QPushButton('Send')

        inchat_layout = QVBoxLayout()
        inchat_layout.addWidget(inchat_label)
        inchat_layout.addWidget(self.inchat)

        outchat_layout = QVBoxLayout()
        outchat_layout.addWidget(outchat_label)
        outchat_layout.addWidget(self.outchat)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.receiver)
        main_layout.addLayout(inchat_layout)
        main_layout.addLayout(outchat_layout)
        main_layout.addWidget(send_btn)

        self.receiver.setStyleSheet(receiver_style)
        self.inchat.setStyleSheet(text_edit_style)
        self.outchat.setStyleSheet(text_edit_style)
        inchat_label.setStyleSheet(label_style)
        outchat_label.setStyleSheet(label_style)
        send_btn.setStyleSheet(button_style)

        send_btn.clicked.connect(self.send_message)

        self.setLayout(main_layout)

    def send_message(self):
        ...


app = QApplication([])
main = LoginWindow()
main.show()
app.exec_()
