import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QMessageBox,
    QCheckBox,
    QHBoxLayout,
    QFrame,
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QPixmap
from admin import AdminPanel
from guard import GuardPanel
import json
import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

CONFIG_FILE = "config.json"

USERS = [
    {
        "role": "Администратор",
        "login": "admin",
        "password": "123",
        "secret": "123",
        "fio": "Иванов И.И.",
    },
    {
        "role": "Вахтер",
        "login": "guard",
        "password": "123",
        "secret": "123",
        "fio": "Петров П.П.",
    },
]


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система контроля доступа")
        self.resize(1000, 600)
        self.move(
            QApplication.desktop().screen().rect().center() - self.rect().center()
        )
        self.init_ui()
        self.load_credentials()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setStyleSheet(
            """
            QWidget {
                background-color: white;
                font-family: "Segoe UI";
            }
            QLabel {
                font-size: 16px;
                color: #2c3e50;
                margin-bottom: 8px;
            }
            QLineEdit, QComboBox {
                padding: 15px;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                font-size: 15px;
                margin-bottom: 15px;
                background-color: #f8f9fa;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #3498db;
                background-color: white;
            }
            QPushButton#loginButton {
                background-color: #FF9800;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
                border-radius: 8px;
                border: none;
                min-width: 120px;
            }
            QPushButton#loginButton:hover {
                background-color: #F57C00;
            }
            QCheckBox {
                font-size: 14px;
                color: #7f8c8d;
                margin-bottom: 15px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 3px;
                border: 1px solid #bdc3c7;
            }
            QCheckBox::indicator:checked {
                background-color: #3498db;
                border: 1px solid #3498db;
            }
        """
        )

        left_widget = QWidget()
        left_widget.setStyleSheet(
            """
            QWidget {
                background-color: #3498db;
                border-radius: 0;
            }
        """
        )
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(60, 60, 60, 60)

        system_name = QLabel("СКУД")
        system_name.setStyleSheet(
            """
            QLabel {
                color: white;
                font-size: 48px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """
        )
        system_name.setAlignment(Qt.AlignCenter)

        system_desc = QLabel("Система контроля\nи управления доступом")
        system_desc.setStyleSheet(
            """
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: 500;
                line-height: 1.4;
            }
        """
        )
        system_desc.setAlignment(Qt.AlignCenter)

        left_layout.addWidget(system_name)
        left_layout.addWidget(system_desc)
        left_layout.addStretch()

        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(80, 80, 80, 80)
        form_widget.setStyleSheet(
            """
            QWidget {
                background-color: white;
            }
        """
        )

        title_label = QLabel("Авторизация")
        title_label.setStyleSheet(
            """
            QLabel {
                font-size: 32px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 40px;
            }
        """
        )
        title_label.setAlignment(Qt.AlignCenter)

        self.role_box = QComboBox()
        self.role_box.addItems(["Администратор", "Вахтер"])
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Пароль")
        self.secret_input = QLineEdit()
        self.secret_input.setPlaceholderText("Секретное слово")
        self.remember_me_checkbox = QCheckBox("Запомнить меня")

        button_container = QHBoxLayout()
        button_container.setSpacing(15)

        self.login_btn = QPushButton("Войти")
        self.login_btn.setObjectName("loginButton")
        self.login_btn.clicked.connect(self.try_login)

        self.clear_btn = QPushButton("Очистить")
        self.clear_btn.setObjectName("clearButton")
        self.clear_btn.setStyleSheet(
            """
            QPushButton#clearButton {
                background-color: #95a5a6;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
                border-radius: 8px;
                border: none;
                min-width: 120px;
            }
            QPushButton#clearButton:hover {
                background-color: #7f8c8d;
            }
            """
        )
        self.clear_btn.clicked.connect(self.clear_form)

        button_container.addWidget(self.clear_btn)
        button_container.addStretch(1)
        button_container.addWidget(self.login_btn)

        self.login_btn.setStyleSheet(
            """
            QPushButton#loginButton {
                background-color: #3498db;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
                border-radius: 8px;
                border: none;
                min-width: 120px;
            }
            QPushButton#loginButton:hover {
                background-color: #217dbb;
            }
            """
        )

        self.emulator_btn = QPushButton("Запустить эмулятор")
        self.emulator_btn.setStyleSheet(
            "font-size: 15px; background: #FF9800; color: white; border-radius: 8px; padding: 10px;"
        )
        self.emulator_btn.clicked.connect(self.launch_emulator)

        form_layout.addWidget(title_label)
        form_layout.addWidget(QLabel("Тип пользователя"))
        form_layout.addWidget(self.role_box)
        form_layout.addWidget(self.login_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.secret_input)
        form_layout.addWidget(self.remember_me_checkbox)
        form_layout.addWidget(self.emulator_btn)
        form_layout.addStretch(1)
        form_layout.addLayout(button_container)

        main_layout.addWidget(left_widget, 1)
        main_layout.addWidget(form_widget, 1)

    def try_login(self):
        role = self.role_box.currentText()
        login = self.login_input.text()
        password = self.password_input.text()
        secret = self.secret_input.text()
        user = next(
            (
                u
                for u in USERS
                if u["role"] == role
                and u["login"] == login
                and u["password"] == password
                and u["secret"] == secret
            ),
            None,
        )
        if user:
            if self.remember_me_checkbox.isChecked():
                self.save_credentials(login, password, role)
            else:
                self.clear_credentials()
            self.hide()
            if role == "Администратор":
                self.panel = AdminPanel(user["fio"])
            else:
                self.panel = GuardPanel(user["fio"])
            self.panel.resize(1920, 1080)
            self.panel.show()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверные данные")

    def save_credentials(self, login, password, role):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump({"login": login, "password": password, "role": role}, f)
        except Exception as e:
            print(f"Error saving credentials: {e}")

    def load_credentials(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "login" in data and "password" in data and "role" in data:
                        self.login_input.setText(data["login"])
                        self.password_input.setText(data["password"])
                        role_index = self.role_box.findText(data["role"])
                        if role_index != -1:
                            self.role_box.setCurrentIndex(role_index)
                        self.remember_me_checkbox.setChecked(True)
            except Exception as e:
                print(f"Error loading credentials: {e}")

    def clear_credentials(self):
        if os.path.exists(CONFIG_FILE):
            try:
                os.remove(CONFIG_FILE)
            except Exception as e:
                print(f"Error clearing credentials: {e}")

    def clear_form(self):
        self.login_input.clear()
        self.password_input.clear()
        self.secret_input.clear()
        self.role_box.setCurrentIndex(0)
        self.remember_me_checkbox.setChecked(False)

    def launch_emulator(self):
        from emulator import Emulator

        self.emulator = Emulator()
        self.emulator.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
