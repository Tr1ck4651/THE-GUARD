import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QLineEdit,
    QMessageBox,
    QTextEdit,
    QGroupBox,
    QRadioButton,
    QButtonGroup,
    QFrame,
    QScrollArea,
    QSizePolicy,
    QProgressBar,
    QInputDialog,
)
from PyQt5.QtCore import Qt, QTimer, QDateTime, QPropertyAnimation, QEasingCurve, QPoint
from PyQt5.QtGui import QColor, QPalette, QFont, QIcon, QPainter, QLinearGradient
import json
import random
import os
import uuid
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Emulator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Эмулятор СКУД")
        self.setMinimumSize(1200, 800)
        self.employees = self.load_employees()
        self.guests = self.load_guests()
        self.history = []
        self.stats = {"entered": 0, "exited": 0}
        self.current_visitors = {}  
        self.init_ui()

        self.simulation_timer = QTimer()
        self.simulation_timer.timeout.connect(self.simulate_traffic)

        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.remaining_time = 12 * 60 * 60  
        self.is_running = False

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        control_panel = QFrame()
        control_panel.setObjectName("controlPanel")
        control_panel.setStyleSheet(
            """
            #controlPanel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2c3e50, stop:1 #34495e);
                border-radius: 14px;
                padding: 18px;
            }
            QLabel {
                color: white;
                font-size: 13px;
                font-weight: bold;
                margin-bottom: 2px;
            }
            QLineEdit {
                padding: 6px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 6px;
                background: rgba(255, 255, 255, 0.1);
                color: white;
                font-size: 12px;
                min-width: 180px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
                background: rgba(255, 255, 255, 0.2);
            }
            QPushButton {
                padding: 6px 0;
                border: none;
                border-radius: 6px;
                background: #3498db;
                color: white;
                font-size: 12px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background: #2980b9;
            }
            QRadioButton {
                color: white;
                font-size: 12px;
                padding: 2px;
            }
            QRadioButton::indicator {
                width: 14px;
                height: 14px;
                border-radius: 7px;
                border: 1px solid white;
            }
            QRadioButton::indicator:checked {
                background: #3498db;
            }
            QGroupBox {
                color: white;
                font-size: 13px;
                font-weight: bold;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                margin-top: 12px;
                margin-bottom: 12px;
                padding: 10px 12px 10px 12px;
            }
            QProgressBar {
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 6px;
                text-align: center;
                background: rgba(255, 255, 255, 0.1);
                color: white;
                font-size: 11px;
            }
            QProgressBar::chunk {
                background: #3498db;
                border-radius: 5px;
            }
        """
        )
        control_layout = QVBoxLayout(control_panel)
        control_layout.setSpacing(14)
        control_layout.setContentsMargins(10, 10, 10, 10)
        title = QLabel("Эмулятор СКУД")
        title.setStyleSheet(
            """
            font-size: 20px;
            font-weight: bold;
            color: white;
            margin-bottom: 10px;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
        """
        )
        title.setAlignment(Qt.AlignCenter)
        control_layout.addWidget(title)

        timer_group = QGroupBox("Таймер")
        timer_layout = QVBoxLayout()
        timer_layout.setSpacing(7)
        timer_layout.setContentsMargins(8, 8, 8, 8)

        self.timer_label = QLabel("12:00:00")
        self.timer_label.setStyleSheet(
            """
            font-size: 18px;
            font-weight: bold;
            color: white;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
        """
        )
        self.timer_label.setAlignment(Qt.AlignCenter)
        timer_layout.addWidget(self.timer_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(12 * 60 * 60)
        self.progress_bar.setValue(12 * 60 * 60)
        timer_layout.addWidget(self.progress_bar)

        self.start_btn = QPushButton("Запустить")
        self.start_btn.setStyleSheet(
            """
            QPushButton {
                background: #e74c3c;
                color: white;
                font-size: 12px;
                font-weight: bold;
                padding: 6px;
                border-radius: 6px;
                margin-top: 5px;
            }
            QPushButton:hover {
                background: #c0392b;
            }
        """
        )
        self.start_btn.clicked.connect(self.toggle_timer)
        timer_layout.addWidget(self.start_btn)

        timer_group.setLayout(timer_layout)
        control_layout.addWidget(timer_group)

        role_group = QGroupBox("Выберите роль")
        role_layout = QVBoxLayout()
        role_layout.setSpacing(2)
        role_layout.setContentsMargins(8, 8, 8, 8)
        self.role_buttons = QButtonGroup()

        self.employee_radio = QRadioButton("Сотрудник")
        self.guest_radio = QRadioButton("Гость")
        self.group_radio = QRadioButton("Группа гостей")

        self.role_buttons.addButton(self.employee_radio)
        self.role_buttons.addButton(self.guest_radio)
        self.role_buttons.addButton(self.group_radio)

        self.employee_radio.setStyleSheet("font-size: 12px;")
        self.guest_radio.setStyleSheet("font-size: 12px;")
        self.group_radio.setStyleSheet("font-size: 12px;")

        role_layout.addWidget(self.employee_radio)
        role_layout.addWidget(self.guest_radio)
        role_layout.addWidget(self.group_radio)
        role_group.setLayout(role_layout)
        control_layout.addWidget(role_group)

        id_label = QLabel("ID:")
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Введите ID")
        self.id_input.setFixedHeight(30)
        self.id_input.setMinimumWidth(220)
        self.id_input.setMaximumWidth(400)
        control_layout.addWidget(id_label)
        control_layout.addWidget(self.id_input)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        self.enter_btn = QPushButton("Вход")
        self.exit_btn = QPushButton("Выход")
        self.enter_btn.setFixedHeight(28)
        self.exit_btn.setFixedHeight(28)
        self.enter_btn.setMinimumWidth(0)
        self.exit_btn.setMinimumWidth(0)
        self.enter_btn.setMaximumWidth(16777215)
        self.exit_btn.setMaximumWidth(16777215)
        self.enter_btn.clicked.connect(self.enter_event)
        self.exit_btn.clicked.connect(self.exit_event)
        buttons_layout.addWidget(self.enter_btn)
        buttons_layout.addWidget(self.exit_btn)
        control_layout.addLayout(buttons_layout)

        stats_group = QGroupBox("Статистика")
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(7)
        stats_layout.setContentsMargins(8, 8, 8, 8)
        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.ax = self.canvas.figure.add_subplot(111)
        self.update_graph()
        self.canvas.setFixedHeight(90)
        self.canvas.setMinimumWidth(0)
        self.canvas.setMaximumWidth(16777215)
        stats_layout.addWidget(self.canvas)
        self.stats_entered = QLabel("Вошло: 0")
        self.stats_exited = QLabel("Вышло: 0")
        self.stats_entered.setStyleSheet("font-size: 12px;")
        self.stats_exited.setStyleSheet("font-size: 12px;")
        stats_layout.addWidget(self.stats_entered)
        stats_layout.addWidget(self.stats_exited)
        stats_group.setLayout(stats_layout)
        control_layout.addWidget(stats_group)

        memo_group = QGroupBox("Памятка")
        memo_layout = QVBoxLayout()
        memo_layout.setSpacing(2)
        memo_layout.setContentsMargins(8, 8, 8, 8)
        memo_text = QLabel(
            "1. Нажмите 'Запустить' для начала работы эмулятора\n"
            "2. Выберите роль (Сотрудник/Гость/Группа гостей)\n"
            "3. Введите ID посетителя\n"
            "4. Нажмите 'Вход' или 'Выход'\n"
            "5. Следите за статистикой\n"
            "6. Эмулятор автоматически закроется через 12 часов"
        )
        memo_text.setStyleSheet("color: white; font-size: 11px; line-height: 1.2;")
        memo_layout.addWidget(memo_text)
        memo_group.setLayout(memo_layout)
        control_layout.addWidget(memo_group)

        control_layout.addStretch()
        main_layout.addWidget(control_panel, 1)

        history_panel = QFrame()
        history_panel.setObjectName("historyPanel")
        history_panel.setStyleSheet(
            """
            #historyPanel {
                background: white;
                border-radius: 24px;
                padding: 20px;
            }
            QLabel {
                color: #2c3e50;
                font-size: 16px;
            }
        """
        )
        history_layout = QVBoxLayout(history_panel)

        history_title = QLabel("История событий")
        history_title.setStyleSheet(
            """
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
        """
        )
        history_title.setAlignment(Qt.AlignCenter)
        history_layout.addWidget(history_title)

        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        self.history_text.setStyleSheet(
            """
            QTextEdit {
                border: 2px solid #e0e0e0;
                border-radius: 12px;
                padding: 10px;
                font-size: 14px;
                background: #f8f9fa;
            }
        """
        )
        history_layout.addWidget(self.history_text)

        main_layout.addWidget(history_panel, 2)

    def log_event(self, message):
        current_time = QDateTime.currentDateTime().toString("dd.MM.yyyy HH:mm:ss")
        self.history.append({"time": current_time, "message": message})
        self.history_text.append(f"[{current_time}] {message}")
        self.save_history()
        self.update_graph()

    def update_stats(self, action):
        if action == "вход":
            self.stats["entered"] += 1
            self.stats_entered.setText(f"Вошло: {self.stats['entered']}")
        else:
            self.stats["exited"] += 1
            self.stats_exited.setText(f"Вышло: {self.stats['exited']}")

    def enter_event(self):
        role = (
            "Сотрудник"
            if self.employee_radio.isChecked()
            else "Гость" if self.guest_radio.isChecked() else "Группа гостей"
        )
        id = self.id_input.text()

        if not id:
            QMessageBox.warning(self, "Ошибка", "Введите ID")
            return

        if id in self.current_visitors:
            QMessageBox.warning(self, "Ошибка", "Этот посетитель уже находится внутри")
            return

        current_time = QDateTime.currentDateTime().toString("dd.MM.yyyy HH:mm:ss")

        if role == "Сотрудник":
            employee = next((e for e in self.employees if e["id"] == id), None)
            if employee:
                name = f"{employee['first_name']} {employee['last_name']}"
                self.current_visitors[id] = {"role": role, "name": name}
                self.history.append(
                    {
                        "id": id,
                        "role": role,
                        "name": name,
                        "action": "вход",
                        "time": current_time,
                    }
                )
                self.log_event(f"Вход сотрудника: {name}")
                self.update_stats("вход")
            else:
                QMessageBox.warning(self, "Ошибка", "Сотрудник не найден")
        elif role == "Гость":
            guest = next(
                (
                    g
                    for g in self.guests
                    if g["id"] == id and not g.get("is_group", False)
                ),
                None,
            )
            if guest:
                name = f"{guest['first_name']} {guest['last_name']}"
                self.current_visitors[id] = {"role": role, "name": name}
                self.history.append(
                    {
                        "id": id,
                        "role": role,
                        "name": name,
                        "action": "вход",
                        "time": current_time,
                    }
                )
                self.log_event(f"Вход гостя: {name}")
                self.update_stats("вход")
            else:
                QMessageBox.warning(self, "Ошибка", "Гость не найден")
        else:  
            group = next(
                (g for g in self.guests if g["id"] == id and g.get("is_group", False)),
                None,
            )
            if group:
                current_date = QDateTime.currentDateTime().toString("yyyy-MM-dd")
                if group["date_from"] <= current_date <= group["date_to"]:
                    name = group["group_name"]
                    self.current_visitors[id] = {
                        "role": role,
                        "name": name,
                        "members": group["members"],
                    }
                    self.history.append(
                        {
                            "id": id,
                            "role": role,
                            "name": name,
                            "action": "вход",
                            "time": current_time,
                            "members": group["members"],
                        }
                    )
                    self.log_event(
                        f"Вход группы гостей: {name} ({len(group['members'])} человек)"
                    )
                    self.update_stats("вход")
                else:
                    QMessageBox.warning(self, "Ошибка", "Срок действия пропуска истек")
            else:
                QMessageBox.warning(self, "Ошибка", "Группа не найдена или не одобрена")

        self.save_history()

    def exit_event(self):
        role = (
            "Сотрудник"
            if self.employee_radio.isChecked()
            else "Гость" if self.guest_radio.isChecked() else "Группа гостей"
        )
        id = self.id_input.text()

        if not id:
            QMessageBox.warning(self, "Ошибка", "Введите ID")
            return

        if id not in self.current_visitors:
            QMessageBox.warning(self, "Ошибка", "Этот посетитель не находится внутри")
            return

        visitor = self.current_visitors[id]
        if visitor["role"] != role:
            QMessageBox.warning(
                self,
                "Ошибка",
                f"Неверная роль. Посетитель зарегистрирован как {visitor['role']}",
            )
            return

        current_time = QDateTime.currentDateTime().toString("dd.MM.yyyy HH:mm:ss")
        name = visitor["name"]

        self.history.append(
            {
                "id": id,
                "role": role,
                "name": name,
                "action": "выход",
                "time": current_time,
            }
        )
        self.log_event(f"Выход {role.lower()}: {name}")
        self.update_stats("выход")

        del self.current_visitors[id]

        self.save_history()

    def simulate_traffic(self):
        if not self.is_running:
            return

        action = random.choice(["вход", "выход"])
        role = random.choice(["Гость", "Группа гостей"])

        if action == "вход":
            if role == "Гость":
                available_guests = [
                    g
                    for g in self.guests
                    if not g.get("is_group", False)
                    and g["id"] not in self.current_visitors
                ]
                if not available_guests:
                    return
                guest = random.choice(available_guests)
                id = guest["id"]
                name = f"{guest['first_name']} {guest['last_name']}"
            else:  
                available_groups = [
                    g
                    for g in self.guests
                    if g.get("is_group", False) and g["id"] not in self.current_visitors
                ]
                if not available_groups:
                    return
                group = random.choice(available_groups)
                id = group["id"]
                name = group["group_name"]
        else:  
            available_visitors = {
                k: v for k, v in self.current_visitors.items() if v["role"] == role
            }
            if not available_visitors:
                return
            id = random.choice(list(available_visitors.keys()))
            name = available_visitors[id]["name"]

        current_time = QDateTime.currentDateTime().toString("dd.MM.yyyy HH:mm:ss")

        if action == "вход":
            self.current_visitors[id] = {"role": role, "name": name}
        else:
            del self.current_visitors[id]

        self.history.append(
            {
                "id": id,
                "role": role,
                "name": name,
                "action": action,
                "time": current_time,
            }
        )

        self.log_event(
            f"{'Вход' if action == 'вход' else 'Выход'} {role.lower()}: {name}"
        )
        self.update_stats(action)
        self.save_history()

    def load_employees(self):
        if os.path.exists("employees.json"):
            with open("employees.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def load_guests(self):
        guests = []

        if os.path.exists("requests.json"):
            with open("requests.json", "r", encoding="utf-8") as f:
                requests = json.load(f)
                for req in requests:
                    if (
                        req.get("status") == "approved"
                    ):  
                        if req.get("type") == "individual":
                           
                            guest = {
                                "id": req.get(
                                    "pass_id"
                                ),  
                                "is_group": False,
                                "first_name": req.get("first_name", ""),
                                "last_name": req.get("last_name", ""),
                                "date_from": req.get("date_from"),
                                "date_to": req.get("date_to"),
                            }
                            guests.append(guest)
                        elif req.get("type") == "group":
                         
                            group = {
                                "id": req.get(
                                    "pass_id"
                                ), 
                                "is_group": True,
                                "group_name": f"Группа {req.get('pass_id')}",
                                "members": req.get("visitors", []),
                                "date_from": req.get("date_from"),
                                "date_to": req.get("date_to"),
                            }
                            guests.append(group)
        return guests

    def save_history(self):
        with open("traffic_history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def toggle_timer(self):
        if not self.is_running:

            password, ok = QInputDialog.getText(
                self, "Пароль", "Введите пароль для запуска:", QLineEdit.Password
            )
            if not ok or password != "1234":
                QMessageBox.warning(self, "Ошибка", "Неверный пароль!")
                return
            self.is_running = True
            self.start_btn.setText("Остановить")
            self.countdown_timer.start(1000)  
            self.simulation_timer.start(5000)  
        else:

            password, ok = QInputDialog.getText(
                self, "Пароль", "Введите пароль для остановки:", QLineEdit.Password
            )
            if not ok or password != "1234":
                QMessageBox.warning(self, "Ошибка", "Неверный пароль!")
                return
            self.is_running = False
            self.start_btn.setText("Запустить")
            self.countdown_timer.stop()
            self.simulation_timer.stop()

    def update_countdown(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            hours = self.remaining_time // 3600
            minutes = (self.remaining_time % 3600) // 60
            seconds = self.remaining_time % 60
            self.timer_label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            self.progress_bar.setValue(self.remaining_time)
        else:
            self.countdown_timer.stop()
            self.simulation_timer.stop()
            self.close()

    def update_graph(self):
        self.ax.clear()

        now = datetime.now()
        hours = [(now - timedelta(hours=i)).strftime("%H:00") for i in range(24)]
        hours.reverse()
        enters = [0] * 24
        exits = [0] * 24

        for event in self.history:
            try:
                event_time = datetime.strptime(event["time"], "%d.%m.%Y %H:%M:%S")
                hour_diff = int((now - event_time).total_seconds() / 3600)
                if 0 <= hour_diff < 24:
                    if event["action"] == "вход":
                        enters[hour_diff] += 1
                    else:
                        exits[hour_diff] += 1
            except:
                continue

        self.ax.plot(hours, enters, label="Входы", color="#27ae60", marker="o")
        self.ax.plot(hours, exits, label="Выходы", color="#e74c3c", marker="o")
        self.ax.set_title("Активность за последние 24 часа", color="#2c3e50")
        self.ax.set_xlabel("Время", color="#2c3e50")
        self.ax.set_ylabel("Количество", color="#2c3e50")
        self.ax.legend()
        self.ax.grid(True, linestyle="--", alpha=0.7)
        self.canvas.figure.tight_layout()
        self.canvas.draw()
