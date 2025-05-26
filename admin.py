from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QLineEdit,
    QDialog,
    QFormLayout,
    QDialogButtonBox,
    QMessageBox,
    QFrame,
    QHeaderView,
    QTabWidget,
    QScrollArea,
    QComboBox,
    QDateEdit,
    QFileDialog,
    QGridLayout,
    QSpinBox,
    QAbstractItemView,
)
from PyQt5.QtCore import Qt, QDate, QDateTime, QTimer
from PyQt5.QtGui import QBrush, QColor, QIcon, QPixmap
import random
import os
import json
import uuid

EMPLOYEES_FILE = "employees.json"
REQUESTS_FILE = "requests.json"

STATUS_TRANSLATIONS = {
    "pending": "В процессе",
    "approved": "Одобрена",
    "rejected": "Отклонена",
}


class AddEmployeeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить сотрудника")
        self.setMinimumSize(400, 850)
        self.setStyleSheet(
            """
            QDialog {
                background: #F4F5F7;
                font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
            }
        """
        )
        card = QFrame()
        card.setStyleSheet(
            """
            background: #fff;
            border-radius: 32px;
            box-shadow: 0 8px 32px #b0b0b033;
            margin: 0 0 0 0;
            """
        )
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 60, 0, 0)
        main_layout.addWidget(card, alignment=Qt.AlignCenter)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(36, 32, 36, 32)
        card_layout.setSpacing(28)
        card.setMinimumWidth(340)
        card.setMaximumWidth(520)
        title = QLabel("Добавить сотрудника")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            "font-size:clamp(22px,3vw,32px);font-weight:900;color:#FF9800;letter-spacing:1px;margin-bottom:10px;"
        )
        card_layout.addWidget(title)
        self.photo_path = ""
        self.photo_label = QLabel()
        self.photo_label.setMinimumSize(90, 90)
        self.photo_label.setMaximumSize(160, 160)
        self.photo_label.setStyleSheet(
            "background:#f8fafc;border:3px solid #E0E6ED;border-radius:80px;box-shadow:0 2px 8px #bbb2;"
        )
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setText("Фото")
        card_layout.addWidget(self.photo_label, alignment=Qt.AlignHCenter)
        self.photo_btn = QPushButton("Загрузить фото")
        self.photo_btn.setStyleSheet(
            "font-size:15px;padding:10px 32px;border-radius:16px;background:#FF9800;color:#fff;font-weight:700;margin-top:10px;"
        )
        self.photo_btn.setCursor(Qt.PointingHandCursor)
        self.photo_btn.clicked.connect(self.load_photo)
        card_layout.addWidget(self.photo_btn, alignment=Qt.AlignHCenter)
        self.first_name = self._modern_field("Имя")
        card_layout.addWidget(self._modern_labeled_field("Имя", self.first_name))
        self.last_name = self._modern_field("Фамилия")
        card_layout.addWidget(self._modern_labeled_field("Фамилия", self.last_name))
        self.emp_id = self._modern_field("ID", readonly=True)
        self.emp_id.setText(str(random.randint(100, 999)))
        card_layout.addWidget(self._modern_labeled_field("ID", self.emp_id))
        self.phone = self._modern_field("Телефон")
        self.phone.setInputMask("+7 (000) 000-00-00;_")
        card_layout.addWidget(self._modern_labeled_field("Телефон", self.phone))
        card_layout.addSpacing(10)
        btns = QHBoxLayout()
        btns.setSpacing(18)
        ok_btn = QPushButton("Добавить")
        ok_btn.setStyleSheet(
            "QPushButton {background:#7BA89F;color:white;font-size:18px;padding:14px 0;border-radius:16px;font-weight:700;} QPushButton:hover {background:#5e8e7e;}"
        )
        ok_btn.setCursor(Qt.PointingHandCursor)
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Отмена")
        cancel_btn.setStyleSheet(
            "QPushButton {background:#eee;font-size:18px;padding:14px 0;border-radius:16px;} QPushButton:hover {background:#e0e0e0;}"
        )
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        ok_btn.setMinimumWidth(0)
        cancel_btn.setMinimumWidth(0)
        ok_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        cancel_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btns.addWidget(ok_btn)
        btns.addWidget(cancel_btn)
        card_layout.addLayout(btns)

    def _modern_field(self, placeholder, readonly=False):
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setStyleSheet(
            """
            QLineEdit {
                padding: 10px 14px;
                font-size: 17px;
                border-radius: 12px;
                border: 2px solid #E0E6ED;
                background: #f8fafc;
                margin-top: 2px;
                margin-bottom: 2px;
                min-height: 28px;
                min-width: 260px;
                max-width: 600px;
            }
            QLineEdit:focus {
                border: 2px solid #FF9800;
                background: #fffbe7;
            }
            QLineEdit[readOnly=\"true\"] {
                background: #f5f5f5;
                color: #888;
            }
            """
        )
        field.setReadOnly(readonly)
        field.setMinimumWidth(260)
        field.setMaximumWidth(600)
        field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        return field

    def _modern_labeled_field(self, label, field):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setSpacing(2)
        v.setContentsMargins(0, 0, 0, 0)
        l = QLabel(label)
        l.setStyleSheet(
            "font-size:14px;color:#7BA89F;font-weight:600;margin-bottom:2px;margin-left:2px;"
        )
        v.addWidget(l)
        v.addWidget(field)
        return w

    def load_photo(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Выберите фото", "", "Изображения (*.png *.jpg *.jpeg)"
        )
        if file_name:
            self.photo_path = file_name
            pixmap = QPixmap(file_name).scaled(
                self.photo_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.photo_label.setPixmap(pixmap)
            self.photo_label.setText("")
        else:
            self.photo_label.setText("Фото")
            self.photo_label.setPixmap(QPixmap())
            self.photo_path = ""

    def get_data(self):
        return (
            self.first_name.text(),
            self.last_name.text(),
            self.emp_id.text(),
            self.phone.text(),
            self.photo_path,
        )


class AdminRequestDialog(QDialog):
    def __init__(self, request_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Просмотр заявки")
        self.setMinimumSize(900, 800)
        self.request_data = request_data
        self.is_editable = request_data.get("status", "") == "pending"

        self.setStyleSheet(
            """
            QDialog {
                background: #F4F5F7;
                font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
            }
            QLabel[section-title] {
                font-size: 22px;
                font-weight: bold;
                color: #FF9800;
                margin-bottom: 18px;
            }
            QFrame[block="true"] {
                background: #fff;
                border-radius: 18px;
                border: 1.5px solid #E0E6ED;
                box-shadow: 0 4px 24px #bbb3;
                margin-bottom: 28px;
            }
            QLabel[key] {
                color: #888;
                font-size: 15px;
                font-weight: 500;
            }
            QLabel[value] {
                color: #222;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton {
                font-size: 18px;
                padding: 12px 36px;
                border-radius: 12px;
                font-weight: bold;
                background: #FF9800;
                color: white;
                margin: 18px 0 0 0;
            }
            QPushButton:hover {
                background: #e67c00;
            }
        """
        )

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(0)
        top_panel = QHBoxLayout()
        req_id = request_data.get("id", "-")
        status = request_data.get("status", "pending")
        status_text = STATUS_TRANSLATIONS.get(status, "Неизвестно")
        status_color = (
            "#4CAF50"
            if status == "approved"
            else ("#f44336" if status == "rejected" else "#FF9800")
        )
        title = QLabel(f"Заявка №{req_id}")
        title.setStyleSheet(
            "font-size: 32px; font-weight: bold; color: #FF9800; margin-right: 24px;"
        )
        top_panel.addWidget(title)
        status_badge = QLabel(
            f"<span style='background:{status_color};color:#fff;padding:8px 24px;border-radius:16px;font-size:18px;font-weight:bold;'>{status_text}</span>"
        )
        top_panel.addWidget(status_badge)
        top_panel.addStretch()
        main_layout.addLayout(top_panel)
        main_layout.addSpacing(18)
        info_block = QFrame()
        info_block.setProperty("block", True)
        info_layout = QGridLayout(info_block)
        info_layout.setContentsMargins(32, 24, 32, 24)
        info_layout.setHorizontalSpacing(32)
        info_layout.setVerticalSpacing(10)
        info_block.setMinimumHeight(90)
        info_layout.addWidget(self._key_label("Тип заявки:"), 0, 0)
        info_layout.addWidget(
            self._value_label(
                "Индивидуальная"
                if request_data.get("type") == "individual"
                else "Групповая"
            ),
            0,
            1,
        )
        info_layout.addWidget(self._key_label("Дата создания:"), 0, 2)
        info_layout.addWidget(
            self._value_label(request_data.get("created_at", "-")), 0, 3
        )
        info_layout.addWidget(self._key_label("Действует с:"), 1, 0)
        info_layout.addWidget(
            self._value_label(request_data.get("date_from", "-")), 1, 1
        )
        info_layout.addWidget(self._key_label("Действует по:"), 1, 2)
        info_layout.addWidget(self._value_label(request_data.get("date_to", "-")), 1, 3)
        main_layout.addWidget(info_block)
        host_block = QFrame()
        host_block.setProperty("block", True)
        host_layout = QGridLayout(host_block)
        host_layout.setContentsMargins(32, 24, 32, 24)
        host_layout.setHorizontalSpacing(32)
        host_layout.setVerticalSpacing(10)
        host_block.setMinimumHeight(70)
        host_layout.addWidget(self._key_label("Подразделение:"), 0, 0)
        host_layout.addWidget(
            self._value_label(request_data.get("department", "-")), 0, 1
        )
        host_layout.addWidget(self._key_label("ФИО принимающей стороны:"), 0, 2)
        host_layout.addWidget(
            self._value_label(request_data.get("host_fio", "-")), 0, 3
        )
        main_layout.addWidget(host_block)
        if request_data.get("type") == "individual":
            guest_block = QFrame()
            guest_block.setProperty("block", True)
            guest_layout = QGridLayout(guest_block)
            guest_layout.setContentsMargins(32, 24, 32, 24)
            guest_layout.setHorizontalSpacing(32)
            guest_layout.setVerticalSpacing(10)
            guest_block.setMinimumHeight(120)
            fio = f"{request_data.get('last_name', '')} {request_data.get('first_name', '')} {request_data.get('middle_name', '')}".strip()
            guest_layout.addWidget(self._key_label("ФИО:"), 0, 0)
            guest_layout.addWidget(self._value_label(fio), 0, 1)
            guest_layout.addWidget(self._key_label("Телефон:"), 0, 2)
            guest_layout.addWidget(
                self._value_label(request_data.get("phone", "-")), 0, 3
            )
            guest_layout.addWidget(self._key_label("Email:"), 1, 0)
            guest_layout.addWidget(
                self._value_label(request_data.get("email", "-")), 1, 1
            )
            guest_layout.addWidget(self._key_label("Организация:"), 1, 2)
            guest_layout.addWidget(
                self._value_label(request_data.get("org", "-")), 1, 3
            )
            guest_layout.addWidget(self._key_label("Дата рождения:"), 2, 0)
            guest_layout.addWidget(
                self._value_label(request_data.get("birth", "-")), 2, 1
            )
            guest_layout.addWidget(self._key_label("Паспорт:"), 2, 2)
            guest_layout.addWidget(
                self._value_label(
                    f"{request_data.get('series', '')} {request_data.get('number', '')}"
                ),
                2,
                3,
            )
            guest_layout.addWidget(self._key_label("Примечание:"), 3, 0)
            guest_layout.addWidget(
                self._value_label(request_data.get("note", "-")), 3, 1, 1, 3
            )
            main_layout.addWidget(guest_block)
        else:
            guests_block = QFrame()
            guests_block.setProperty("block", True)
            guests_layout = QVBoxLayout(guests_block)
            guests_title = QLabel(
                "<b style='color:#7BA89F;font-size:18px;'>Список гостей</b>"
            )
            guests_layout.addWidget(guests_title)
            table = QTableWidget()
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(
                ["ФИО", "Контакты", "Дата рождения", "Паспорт", "Примечание"]
            )
            table.setStyleSheet(
                "background: white; border-radius: 8px; font-size: 14px;"
            )
            table.verticalHeader().setVisible(False)
            table.setEditTriggers(QTableWidget.NoEditTriggers)
            visitors = request_data.get("visitors", [])
            table.setRowCount(len(visitors))
            for i, visitor in enumerate(visitors):
                table.setItem(i, 0, QTableWidgetItem(visitor.get("fio", "")))
                table.setItem(i, 1, QTableWidgetItem(visitor.get("contacts", "")))
                table.setItem(i, 2, QTableWidgetItem(visitor.get("birth", "")))
                table.setItem(i, 3, QTableWidgetItem(visitor.get("passport", "")))
                table.setItem(i, 4, QTableWidgetItem(visitor.get("note", "")))
            guests_layout.addWidget(table)
            main_layout.addWidget(guests_block)
        docs_block = QFrame()
        docs_block.setProperty("block", True)
        docs_layout = QHBoxLayout(docs_block)
        docs_layout.setContentsMargins(32, 18, 32, 18)
        docs_layout.setSpacing(18)
        docs_title = QLabel("Документ:")
        docs_title.setProperty("key", True)
        docs_layout.addWidget(docs_title)
        file_path = request_data.get("attached_file_path", "")
        if file_path and os.path.exists(file_path):
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                thumb = QLabel()
                thumb.setPixmap(
                    pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
                thumb.setStyleSheet(
                    "border:1.5px solid #E0E6ED;border-radius:8px;background:#fafbfc;"
                )
                thumb.setCursor(Qt.PointingHandCursor)

                def show_full_image():
                    dlg = QDialog(self)
                    dlg.setWindowTitle("Документ")
                    v = QVBoxLayout(dlg)
                    img = QLabel()
                    img.setPixmap(
                        pixmap.scaled(
                            600, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation
                        )
                    )
                    v.addWidget(img)
                    btn = QPushButton("Закрыть")
                    btn.clicked.connect(dlg.accept)
                    v.addWidget(btn, alignment=Qt.AlignCenter)
                    dlg.exec_()

                thumb.mousePressEvent = lambda e: show_full_image()
                docs_layout.addWidget(thumb)
            download_btn = QPushButton("Скачать документ")
            download_btn.setStyleSheet(
                "font-size:15px;padding:8px 18px;border-radius:8px;background:#7BA89F;color:white;font-weight:600;"
            )

            def download_file():
                from PyQt5.QtWidgets import QFileDialog

                save_path, _ = QFileDialog.getSaveFileName(
                    self, "Сохранить документ", os.path.basename(file_path)
                )
                if save_path:
                    import shutil

                    shutil.copy(file_path, save_path)

            download_btn.clicked.connect(download_file)
            docs_layout.addWidget(download_btn)
        else:
            docs_value = QLabel("Нет документа")
            docs_value.setProperty("value", True)
            docs_layout.addWidget(docs_value)
        main_layout.addWidget(docs_block)
        btns = QHBoxLayout()
        btns.addStretch()
        if self.is_editable:
            approve_btn = QPushButton("Одобрить")
            approve_btn.setStyleSheet(
                "background:#4CAF50;font-size:18px;padding:12px 36px;border-radius:12px;color:white;font-weight:bold;margin-right:18px;"
            )
            approve_btn.clicked.connect(self.approve_request)
            btns.addWidget(approve_btn)
            reject_btn = QPushButton("Отклонить")
            reject_btn.setStyleSheet(
                "background:#f44336;font-size:18px;padding:12px 36px;border-radius:12px;color:white;font-weight:bold;margin-right:18px;"
            )
            reject_btn.clicked.connect(self.reject_request)
            btns.addWidget(reject_btn)
        close_btn = QPushButton("Закрыть")
        close_btn.setStyleSheet(
            "background:#eee;font-size:18px;padding:12px 36px;border-radius:12px;color:#222;font-weight:bold;"
        )
        close_btn.clicked.connect(self.reject)
        btns.addWidget(close_btn)
        main_layout.addLayout(btns)

    def _key_label(self, text):
        l = QLabel(text)
        l.setProperty("key", True)
        return l

    def _value_label(self, text):
        l = QLabel(text)
        l.setProperty("value", True)
        return l

    def get_status_color(self, status):
        if status == "approved":
            return "green"
        elif status == "rejected":
            return "red"
        else:
            return "orange"

    def approve_request(self):
        self.request_data["status"] = "approved"
        self.accept()

    def reject_request(self):
        self.request_data["status"] = "rejected"
        self.accept()


class AdminPanel(QWidget):
    def __init__(self, fio):
        super().__init__()
        self.setWindowTitle("Админ панель")
        self.resize(1920, 1080)
        self.fio = fio
        self.employees = []  
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_employee_list)
        self.update_timer.start(5000)  

        self.init_ui()

    def load_employees(self):
        if os.path.exists(EMPLOYEES_FILE):
            try:
                with open(EMPLOYEES_FILE, "r", encoding="utf-8") as f:
                    self.employees = json.load(f)
            except Exception:
                self.employees = []
        else:
            self.employees = []

    def save_employees(self):
        with open(EMPLOYEES_FILE, "w", encoding="utf-8") as f:
            json.dump(self.employees, f, ensure_ascii=False, indent=2)

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        menu_widget = QWidget()
        menu_widget.setStyleSheet(
            """
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e0eafc, stop:1 #cfdef3);
            border-top-left-radius: 32px;
            border-bottom-left-radius: 32px;
            box-shadow: 6px 0 32px #b0b0b033;
            """
        )
        menu_layout = QVBoxLayout(menu_widget)
        menu_layout.setAlignment(Qt.AlignTop)
        menu_widget.setFixedWidth(320)
        avatar = QLabel()
        avatar.setPixmap(QPixmap(64, 64))
        avatar.setStyleSheet(
            "background:#fff;border-radius:32px;border:3px solid #7BA89F;margin-top:32px;margin-bottom:8px;"
        )
        avatar.setFixedSize(64, 64)
        menu_layout.addWidget(avatar, alignment=Qt.AlignHCenter)
        fio_lbl = QLabel(f"<b style='font-size:18px;color:#7BA89F;'>{self.fio}</b>")
        fio_lbl.setAlignment(Qt.AlignCenter)
        fio_lbl.setStyleSheet("margin-bottom:18px;")
        menu_layout.addWidget(fio_lbl)
        title = QLabel(
            "<span style='font-size:28px;font-weight:900;letter-spacing:2px;color:#FF9800;text-shadow:0 2px 8px #7BA89F;'>Админ</span>"
        )
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("margin-bottom: 18px; padding: 0 10px;")
        menu_layout.addWidget(title)
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color:#e0e6ed;margin:0 0 18px 0;")
        menu_layout.addWidget(sep)
        self.menu_buttons = {}
        btn_style = (
            "QPushButton {"
            "background: #fff; font-size: 17px; padding: 14px 0; margin-bottom: 18px; border-radius: 14px; border: none;"
            "box-shadow: 0 2px 8px #b0b0b022; color: #222; font-weight: 600; letter-spacing: 1px;"
            "transition: background 0.3s, color 0.3s;"
            "text-align: left; padding-left: 32px;"
            "}"
            "QPushButton:hover {"
            "background: #FF9800; color: #fff;"
            "}"
        )
        buttons = [
            ("Id сотрудников", lambda: self.show_employees(force_update=True), "👤"),
            ("Заявки", self.show_requests, "📄"),
            ("Гости", lambda: self.show_guests(), "🧑‍🤝‍🧑"),
            ("Реестр", lambda: self.show_placeholder("Реестр"), "📋"),
        ]
        for text, slot, icon in buttons:
            btn = QPushButton(f"{icon}   {text}")
            btn.setStyleSheet(btn_style)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(slot)
            menu_layout.addWidget(btn)
            self.menu_buttons[text] = btn
        menu_layout.addStretch()
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.HLine)
        sep2.setStyleSheet("color:#e0e6ed;margin:18px 0 0 0;")
        menu_layout.addWidget(sep2)
        version_lbl = QLabel("<span style='color:#bbb;font-size:13px;'>v1.0</span>")
        version_lbl.setAlignment(Qt.AlignCenter)
        version_lbl.setStyleSheet("margin-top:8px;margin-bottom:8px;")
        menu_layout.addWidget(version_lbl)
        logout_btn = QPushButton("Выйти")
        logout_btn.setStyleSheet(
            "background:#eee;font-size:15px;padding:8px 0;border-radius:10px;color:#888;font-weight:600;"
        )
        logout_btn.setCursor(Qt.PointingHandCursor)
        menu_layout.addWidget(logout_btn)
        self.work_area = QWidget()
        self.work_area.setStyleSheet(
            "background-color: #F4F5F7; border-top-right-radius: 18px; border-bottom-right-radius: 18px;"
        )
        self.work_layout = QVBoxLayout(self.work_area)
        self.work_layout.setContentsMargins(80, 60, 80, 60)
        self.show_employees()
        main_layout.addWidget(menu_widget)
        main_layout.addWidget(self.work_area)
        self.setLayout(main_layout)

    def show_placeholder(self, text):
        if text == "Реестр":
            self.show_registry()
        else:
            self.clear_work_area()
            label = QLabel(
                f"<span style='font-size:22px;color:#888;'>Раздел '{text}' в разработке</span>"
            )
            label.setAlignment(Qt.AlignCenter)
            self.work_layout.addWidget(label)

    def clear_work_area(self):
        while self.work_layout.count():
            item = self.work_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def show_employees(self, force_update=False):
        if (
            not force_update
            and hasattr(self, "work_layout")
            and self.work_layout.count() > 0
        ):
            current_widget = self.work_layout.itemAt(0).widget()
            if isinstance(current_widget, QTabWidget):
                self._update_employees_tables(current_widget)
                return
        self.load_employees()
        self.clear_work_area()

        add_btn = QPushButton("Добавить сотрудника")
        add_btn.setStyleSheet(
            "font-size:16px;padding:10px 28px;border-radius:14px;background:#FF9800;color:white;font-weight:700;margin-bottom:18px;"
        )
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(self.add_employee_dialog)
        self.work_layout.addWidget(add_btn, alignment=Qt.AlignLeft)

        tab_widget = QTabWidget()
        tab_widget.setStyleSheet(
            """
            QTabWidget::pane {
                border: 0;
                background-color: #F4F5F7;
                border-radius: 12px;
            }
            QTabBar::tab {
                background-color: #E0E0E0;
                color: #222;
                padding: 8px 18px 12px 18px;
                min-width: 100px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 1px;
                margin-bottom: 4px;
                font-size: 15px;
                font-weight: 500;
                text-align: center;
            }
            QTabBar::tab:selected {
                background-color: #F4F5F7;
                border-bottom: 2px solid #FF9800;
                margin-bottom: 0px;
            }
            QTabBar::tab:hover {
                background-color: #D3D4D6;
            }
            """
        )

        all_tab = QWidget()
        all_layout = QVBoxLayout(all_tab)
        all_table = self._create_employees_table(self.employees)
        all_layout.addWidget(all_table)
        tab_widget.addTab(all_tab, "Все")

        present_tab = QWidget()
        present_layout = QVBoxLayout(present_tab)
        present_emps = self._get_present_employees()
        present_table = self._create_employees_table(present_emps)
        present_layout.addWidget(present_table)
        tab_widget.addTab(present_tab, "На месте")

        absent_tab = QWidget()
        absent_layout = QVBoxLayout(absent_tab)
        absent_emps = self._get_absent_employees()
        absent_table = self._create_employees_table(absent_emps)
        absent_layout.addWidget(absent_table)
        tab_widget.addTab(absent_tab, "Отсутствуют")

        self.work_layout.addWidget(tab_widget)

    def _update_employees_tables(self, tab_widget):
        if not tab_widget or not isinstance(tab_widget, QTabWidget):
            return

        if (
            tab_widget.count() < 3
        ):  
            return

        try:
            all_tab = tab_widget.widget(0)
            if all_tab:
                all_table = all_tab.findChild(QTableWidget)
                if all_table:
                    self._update_table_content(all_table, self.employees)
            present_tab = tab_widget.widget(1)
            if present_tab:
                present_table = present_tab.findChild(QTableWidget)
                if present_table:
                    present_emps = self._get_present_employees()
                    self._update_table_content(present_table, present_emps)
            absent_tab = tab_widget.widget(2)
            if absent_tab:
                absent_table = absent_tab.findChild(QTableWidget)
                if absent_table:
                    absent_emps = self._get_absent_employees()
                    self._update_table_content(absent_table, absent_emps)
        except Exception as e:
            print(f"Error updating employee tables: {e}")
            self.show_employees(force_update=True)

    def _update_table_content(self, table, employees):
        table.setRowCount(len(employees))
        for row, emp in enumerate(employees):
            emp_id = emp.get("id", "")
            table.setItem(row, 0, QTableWidgetItem(emp_id))
            table.setItem(row, 1, QTableWidgetItem(emp.get("first_name", "")))
            table.setItem(row, 2, QTableWidgetItem(emp.get("last_name", "")))
            table.setItem(row, 3, QTableWidgetItem(emp.get("phone", "")))
            status = "на месте"
            color = QColor("#27ae60")
            if emp_id in self._get_employee_actions():
                last_action = self._get_employee_actions()[emp_id]
                if last_action.get("action") != "вход":
                    status = "отсутствует"
                    color = QColor("#e74c3c")

            status_item = QTableWidgetItem(status.capitalize())
            status_item.setForeground(QBrush(color))
            table.setItem(row, 4, status_item)

    def _get_employee_actions(self):
        history = []
        if os.path.exists("traffic_history.json"):
            try:
                with open("traffic_history.json", "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception as e:
                print(f"Error loading history: {e}")

        employee_history = [h for h in history if h.get("role") == "Сотрудник"]
        employee_actions = {}
        for action in sorted(
            employee_history, key=lambda x: x.get("time", ""), reverse=True
        ):
            emp_id = action.get("id")
            if emp_id and emp_id not in employee_actions:
                employee_actions[emp_id] = action
        return employee_actions

    def _get_present_employees(self):
        employee_actions = self._get_employee_actions()
        present_emps = []
        for e in self.employees:
            emp_id = e.get("id", "")
            last_action = employee_actions.get(emp_id)
            if not last_action or last_action.get("action") == "вход":
                present_emps.append(e)
        return present_emps

    def _get_absent_employees(self):
        employee_actions = self._get_employee_actions()
        absent_emps = []
        for e in self.employees:
            emp_id = e.get("id", "")
            last_action = employee_actions.get(emp_id)
            if last_action and last_action.get("action") == "выход":
                absent_emps.append(e)
        return absent_emps

    def update_employee_list(self):
        if hasattr(self, "work_layout") and self.work_layout.count() > 0:
            current_widget = self.work_layout.itemAt(0).widget()
            if isinstance(current_widget, QTabWidget):
                self._update_employees_tables(current_widget)

    def _create_employees_table(self, employees):
        from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton
        import json
        import os
        from PyQt5.QtGui import QBrush, QColor
        history = []
        if os.path.exists("traffic_history.json"):
            try:
                with open("traffic_history.json", "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception as e:
                print(f"Error loading history: {e}")
        employee_history = [h for h in history if h.get("role") == "Сотрудник"]
        employee_actions = {}
        for action in sorted(
            employee_history, key=lambda x: x.get("time", ""), reverse=True
        ):
            emp_id = action.get("id")
            if emp_id and emp_id not in employee_actions:
                employee_actions[emp_id] = action
        filtered_employees = [
            emp for emp in employees if emp.get("id")
        ]  

        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["ID", "Имя", "Фамилия", "Телефон", "Статус"])
        table.setStyleSheet(
            """
            QTableWidget {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                font-size: 15px;
                selection-background-color: #cee7e4;
                selection-color: #222;
            }
            QHeaderView::section {
                background-color: #7BA89F;
                color: white;
                padding: 8px;
                border: 1px solid #e0e0e0;
                font-weight: bold;
            }
            QHeaderView::section:first {
                border-top-left-radius: 10px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 10px;
            }
            QTableWidgetItem {
                padding: 5px;
            }
            """
        )
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setRowCount(len(filtered_employees))
        for row, emp in enumerate(filtered_employees):
            emp_id = emp.get("id", "")
            table.setItem(row, 0, QTableWidgetItem(emp_id))
            table.setItem(row, 1, QTableWidgetItem(emp.get("first_name", "")))
            table.setItem(row, 2, QTableWidgetItem(emp.get("last_name", "")))
            table.setItem(row, 3, QTableWidgetItem(emp.get("phone", "")))
            status = "на месте"
            color = QColor("#27ae60")
            if emp_id in employee_actions:
                last_action = employee_actions[emp_id]
                if last_action.get("action") == "вход":
                    status = "на месте"
                    color = QColor("#27ae60")
                else:
                    status = "отсутствует"
                    color = QColor("#e74c3c")
            status_item = QTableWidgetItem(status.capitalize())
            status_item.setForeground(QBrush(color))
            table.setItem(row, 4, status_item)
        return table

    def show_requests(self):
        self.clear_work_area()

        self.request_tabs = QTabWidget()
        self.request_tabs.setStyleSheet(
            """
            QTabWidget::pane {
                border: 0;
                background-color: #F4F5F7;
                border-bottom-right-radius: 18px;
                border-bottom-left-radius: 18px;
            }
            QTabBar::tab {
                background-color: #E0E0E0;
                color: #222;
                padding: 8px 18px 12px 18px;
                min-width: 100px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 1px;
                margin-bottom: 4px;
                font-size: 15px;
                font-weight: 500;
                text-align: center;
            }
            QTabBar::tab:selected {
                background-color: #F4F5F7;
                border-bottom: 2px solid #FF9800;
                margin-bottom: 0px;
            }
            QTabBar::tab:hover {
                background-color: #D3D4D6;
            }
        """
        )
        all_requests_tab = QWidget()
        all_requests_layout = QVBoxLayout(all_requests_tab)
        self.all_requests_table = self.create_requests_table()
        all_requests_layout.addWidget(self.all_requests_table)
        self.request_tabs.addTab(all_requests_tab, "Все")
        pending_requests_tab = QWidget()
        pending_requests_layout = QVBoxLayout(pending_requests_tab)
        self.pending_requests_table = self.create_requests_table()
        pending_requests_layout.addWidget(self.pending_requests_table)
        self.request_tabs.addTab(pending_requests_tab, "В процессе")
        approved_requests_tab = QWidget()
        approved_requests_layout = QVBoxLayout(approved_requests_tab)
        self.approved_requests_table = self.create_requests_table()
        approved_requests_layout.addWidget(self.approved_requests_table)
        self.request_tabs.addTab(approved_requests_tab, "Одобренные")
        rejected_requests_tab = QWidget()
        rejected_requests_layout = QVBoxLayout(rejected_requests_tab)
        self.rejected_requests_table = self.create_requests_table()
        rejected_requests_layout.addWidget(self.rejected_requests_table)
        self.request_tabs.addTab(rejected_requests_tab, "Отклоненные")

        self.work_layout.addWidget(self.request_tabs)
        self.update_requests_tables()

    def create_requests_table(self):
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(
            ["ID Заявки", "Тип", "Дата создания", "Статус", "Действие"]
        )
        table.setStyleSheet(
            """
            QTableWidget {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                font-size: 14px;
                selection-background-color: #cee7e4; /* Custom selection color */
                selection-color: #222;
            }
            QHeaderView::section {
                background-color: #7BA89F;
                color: white;
                padding: 8px;
                border: 1px solid #e0e0e0;
                font-weight: bold;
            }
            QHeaderView::section:first {
                border-top-left-radius: 8px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 8px;
            }
            QTableWidgetItem {
                padding: 5px;
            }
        """
        )
        table.verticalHeader().setVisible(False)
        table.setColumnWidth(0, 200)
        table.setColumnWidth(1, 100)
        table.setColumnWidth(2, 150)
        table.setColumnWidth(3, 120)
        table.setColumnWidth(4, 150)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.itemDoubleClicked.connect(self.view_request_details)

        return table

    def update_requests_tables(self):
        all_requests = self.load_requests()

        pending_requests = [
            req for req in all_requests if req.get("status", "") == "pending"
        ]
        approved_requests = [
            req for req in all_requests if req.get("status", "") == "approved"
        ]
        rejected_requests = [
            req for req in all_requests if req.get("status", "") == "rejected"
        ]

        self.populate_requests_table(self.all_requests_table, all_requests)
        self.populate_requests_table(self.pending_requests_table, pending_requests)
        self.populate_requests_table(self.approved_requests_table, approved_requests)
        self.populate_requests_table(self.rejected_requests_table, rejected_requests)

    def populate_requests_table(self, table, requests_list):
        table.setRowCount(len(requests_list))
        for row, req in enumerate(requests_list):
            table.setItem(row, 0, QTableWidgetItem(req.get("id", "")))
            table.setItem(
                row,
                1,
                QTableWidgetItem(
                    "Индивидуальная"
                    if req.get("type", "") == "individual"
                    else "Групповая"
                ),
            )
            table.setItem(row, 2, QTableWidgetItem(req.get("created_at", "Не указана")))

            status = req.get("status", "pending")
            status_item = QTableWidgetItem(
                STATUS_TRANSLATIONS.get(status, "Неизвестно")
            )
            status_item.setForeground(self.get_status_color_brush(status))
            table.setItem(row, 3, status_item)

            view_btn = QPushButton("Просмотреть")
            view_btn.setStyleSheet(
                "font-size:12px;padding:2px 6px;border-radius:6px;background:#7BA89F;color:white;"
            )
            view_btn.setProperty("request_id", req.get("id", ""))
            view_btn.clicked.connect(
                lambda _, req_id=req.get("id", ""): self.view_request_details_by_id(
                    req_id
                )
            )

            table.setCellWidget(row, 4, view_btn)

    def get_status_color_brush(self, status):
        if status == "approved":
            return QBrush(QColor("green"))
        elif status == "rejected":
            return QBrush(QColor("red"))
        else:
            return QBrush(QColor("orange"))

    def view_request_details(self, item):
        request_id = item.tableWidget().item(item.row(), 0).text()
        self.view_request_details_by_id(request_id)

    def view_request_details_by_id(self, request_id):
        print(f"[DEBUG] Attempting to view request details for ID: {request_id}")
        all_requests = self.load_requests()
        req = next((r for r in all_requests if r.get("id", "") == request_id), None)

        if req:
            print(f"[DEBUG] Found request: {req.get('id', '')}")
            dlg = AdminRequestDialog(req, self)
            print("[DEBUG] AdminRequestDialog created.")

            original_status = req.get("status")

            if dlg.exec_() == QDialog.Accepted:
                print("[DEBUG] AdminRequestDialog accepted.")
                new_status = dlg.request_data.get("status")
                if new_status != original_status:
                    for i in range(len(all_requests)):
                        if all_requests[i].get("id", "") == request_id:
                            all_requests[i]["status"] = new_status
                            break

                    self.save_requests(all_requests)
                    self.update_requests_tables()
                    QMessageBox.information(
                        self,
                        "Обновление статуса",
                        f"Статус заявки №{request_id} обновлен.",
                    )
            else:
                print("[DEBUG] AdminRequestDialog rejected/closed.")

        else:
            print(f"[DEBUG] Request with ID {request_id} not found.")
            QMessageBox.warning(self, "Ошибка", f"Заявка с ID {request_id} не найдена.")

    def load_requests(self):
        if os.path.exists(REQUESTS_FILE):
            try:
                with open(REQUESTS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for req in data:
                        if "id" not in req:
                            req["id"] = str(uuid.uuid4())
                        if "status" not in req:
                            req["status"] = "pending"
                        if "created_at" not in req:
                            req["created_at"] = QDateTime.currentDateTime().toString(
                                Qt.ISODate
                            )

                    print(f"[DEBUG] Loaded {len(data)} requests from {REQUESTS_FILE}")
                    return data
            except (json.JSONDecodeError, Exception) as e:
                print(f"[DEBUG] Error loading requests: {e}")
                QMessageBox.warning(
                    self, "Ошибка файла", f"Ошибка чтения {REQUESTS_FILE}: {e}"
                )
                return []
        else:
            print(f"[DEBUG] {REQUESTS_FILE} not found.")
            return []

    def save_requests(self, requests_list):
        try:
            with open(REQUESTS_FILE, "w", encoding="utf-8") as f:
                json.dump(requests_list, f, ensure_ascii=False, indent=2)
        except Exception as e:
            QMessageBox.warning(
                self, "Ошибка файла", f"Ошибка записи в {REQUESTS_FILE}: {e}"
            )

    def show_guests(self):
        from PyQt5.QtCore import QDate

        self.clear_work_area()
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet(
            """
            QTabWidget::pane {
                border: 0;
                background-color: #F4F5F7;
                border-radius: 12px;
            }
            QTabBar::tab {
                background-color: #E0E0E0;
                color: #222;
                padding: 8px 18px 12px 18px;
                min-width: 100px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 1px;
                margin-bottom: 4px;
                font-size: 15px;
                font-weight: 500;
                text-align: center;
            }
            QTabBar::tab:selected {
                background-color: #F4F5F7;
                border-bottom: 2px solid #FF9800;
                margin-bottom: 0px;
            }
            QTabBar::tab:hover {
                background-color: #D3D4D6;
            }
            """
        )
        active_tab = QWidget()
        active_layout = QVBoxLayout(active_tab)
        title1 = QLabel(
            "<span style='font-size:22px;font-weight:bold;color:#222;'>Действующие гости</span>"
        )
        title1.setAlignment(Qt.AlignCenter)
        active_layout.addWidget(title1)
        active_layout.addWidget(self._create_guests_table(history=False))
        history_tab = QWidget()
        history_layout = QVBoxLayout(history_tab)
        title2 = QLabel(
            "<span style='font-size:22px;font-weight:bold;color:#222;'>История гостей (пропуск истёк)</span>"
        )
        title2.setAlignment(Qt.AlignCenter)
        history_layout.addWidget(title2)
        history_layout.addWidget(self._create_guests_table(history=True))
        tab_widget.addTab(active_tab, "Действующие")
        tab_widget.addTab(history_tab, "История")
        self.work_layout.addWidget(tab_widget)

    def _create_guests_table(self, history=False):
        from PyQt5.QtCore import QDate

        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(
            ["ФИО гостя", "Тип заявки", "Действует с", "Действует по", "Инфо"]
        )
        table.setStyleSheet(
            """
            QTableWidget {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                font-size: 15px;
                selection-background-color: #cee7e4;
                selection-color: #222;
            }
            QHeaderView::section {
                background-color: #7BA89F;
                color: white;
                padding: 8px;
                border: 1px solid #e0e0e0;
                font-weight: bold;
            }
            QHeaderView::section:first {
                border-top-left-radius: 10px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 10px;
            }
            QTableWidgetItem {
                padding: 5px;
            }
            """
        )
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        guests = []
        today = QDate.currentDate().toString("yyyy-MM-dd")
        for req in self.load_requests():
            if req.get("status") != "approved":
                continue
            if req.get("type") == "individual":
                fio = f"{req.get('last_name', '')} {req.get('first_name', '')} {req.get('middle_name', '')}".strip()
                guest = {
                    "fio": fio,
                    "type": "Индивидуальная",
                    "date_from": req.get("date_from", ""),
                    "date_to": req.get("date_to", ""),
                    "full": req,
                }
                guests.append(guest)
            elif req.get("type") == "group":
                for visitor in req.get("visitors", []):
                    fio = visitor.get("fio", "")
                    guest = {
                        "fio": fio,
                        "type": "Групповая",
                        "date_from": req.get("date_from", ""),
                        "date_to": req.get("date_to", ""),
                        "full": {**req, **visitor},
                    }
                    guests.append(guest)
        if history:
            guests = [g for g in guests if g["date_to"] < today]
        else:
            guests = [g for g in guests if g["date_to"] >= today]
        table.setRowCount(len(guests))
        for row, guest in enumerate(guests):
            table.setItem(row, 0, QTableWidgetItem(guest["fio"]))
            table.setItem(row, 1, QTableWidgetItem(guest["type"]))
            table.setItem(row, 2, QTableWidgetItem(guest["date_from"]))
            table.setItem(row, 3, QTableWidgetItem(guest["date_to"]))
            info_btn = QPushButton("Подробнее")
            info_btn.setStyleSheet(
                "font-size:13px;padding:4px 12px;border-radius:8px;background:#7BA89F;color:white;"
            )
            info_btn.clicked.connect(lambda _, g=guest["full"]: self.show_guest_info(g))
            table.setCellWidget(row, 4, info_btn)
        return table

    def show_guest_info(self, guest):
        dlg = QDialog(self)
        dlg.setWindowTitle("Информация о госте")
        dlg.setMinimumWidth(500)
        layout = QVBoxLayout(dlg)
        title = QLabel(f"<b style='font-size:20px;'>Информация о госте</b>")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        info = ""
        for key, value in guest.items():
            if key in ("id", "status", "type", "created_at", "visitors", "full"):
                continue
            info += f"<b>{key}:</b> {value}<br>"
        info_lbl = QLabel(info)
        info_lbl.setTextFormat(Qt.RichText)
        info_lbl.setWordWrap(True)
        layout.addWidget(info_lbl)
        btns = QHBoxLayout()
        ok_btn = QPushButton("Закрыть")
        ok_btn.clicked.connect(dlg.accept)
        btns.addStretch()
        btns.addWidget(ok_btn)
        layout.addLayout(btns)
        dlg.exec_()

    def show_registry(self):
        self.clear_work_area()
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet(
            """
            QTabWidget::pane {
                border: 0;
                background-color: #F4F5F7;
                border-radius: 12px;
            }
            QTabBar::tab {
                background-color: #E0E0E0;
                color: #222;
                padding: 8px 18px 12px 18px;
                min-width: 100px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 1px;
                margin-bottom: 4px;
                font-size: 15px;
                font-weight: 500;
                text-align: center;
            }
            QTabBar::tab:selected {
                background-color: #F4F5F7;
                border-bottom: 2px solid #FF9800;
                margin-bottom: 0px;
            }
            QTabBar::tab:hover {
                background-color: #D3D4D6;
            }
        """
        )
        employees_tab = QWidget()
        employees_layout = QVBoxLayout(employees_tab)
        title = QLabel(
            "<span style='font-size:24px;font-weight:bold;color:#222;'>Реестр сотрудников</span>"
        )
        title.setAlignment(Qt.AlignCenter)
        employees_layout.addWidget(title)
        employees_table = QTableWidget()
        employees_table.setColumnCount(6)
        employees_table.setHorizontalHeaderLabels(
            ["ID", "ФИО", "Телефон", "Последнее действие", "Время", "Статус"]
        )
        employees_table.setStyleSheet(
            """
            QTableWidget {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                font-size: 15px;
                selection-background-color: #cee7e4;
                selection-color: #222;
            }
            QHeaderView::section {
                background-color: #7BA89F;
                color: white;
                padding: 8px;
                border: 1px solid #e0e0e0;
                font-weight: bold;
            }
            QHeaderView::section:first {
                border-top-left-radius: 10px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 10px;
            }
            QTableWidgetItem {
                padding: 5px;
            }
        """
        )
        employees_table.verticalHeader().setVisible(False)
        employees_table.setEditTriggers(QTableWidget.NoEditTriggers)
        history = []
        if os.path.exists("traffic_history.json"):
            try:
                with open("traffic_history.json", "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception as e:
                print(f"Error loading history: {e}")
        employee_history = [h for h in history if h.get("role") == "Сотрудник"]
        employee_history.sort(key=lambda x: x.get("time", ""), reverse=True)
        employee_actions = {}
        for action in employee_history:
            emp_id = action.get("id")
            if emp_id not in employee_actions:
                employee_actions[emp_id] = action
        employees_table.setRowCount(len(employee_actions))
        for row, (emp_id, action) in enumerate(employee_actions.items()):
            employee = next((e for e in self.employees if e.get("id") == emp_id), None)
            if employee:
                employees_table.setItem(row, 0, QTableWidgetItem(emp_id))
                employees_table.setItem(
                    row,
                    1,
                    QTableWidgetItem(
                        f"{employee.get('first_name', '')} {employee.get('last_name', '')}"
                    ),
                )
                employees_table.setItem(
                    row, 2, QTableWidgetItem(employee.get("phone", ""))
                )
                employees_table.setItem(
                    row, 3, QTableWidgetItem(action.get("action", "").capitalize())
                )
                employees_table.setItem(
                    row, 4, QTableWidgetItem(action.get("time", ""))
                )
                status = "На месте" if action.get("action") == "вход" else "Отсутствует"
                status_item = QTableWidgetItem(status)
                status_item.setForeground(
                    QBrush(QColor("#27ae60" if status == "На месте" else "#e74c3c"))
                )
                employees_table.setItem(row, 5, status_item)

        employees_layout.addWidget(employees_table)
        tab_widget.addTab(employees_tab, "Сотрудники")
        guests_tab = QWidget()
        guests_layout = QVBoxLayout(guests_tab)
        title = QLabel(
            "<span style='font-size:24px;font-weight:bold;color:#222;'>Реестр гостей</span>"
        )
        title.setAlignment(Qt.AlignCenter)
        guests_layout.addWidget(title)
        guests_table = QTableWidget()
        guests_table.setColumnCount(6)
        guests_table.setHorizontalHeaderLabels(
            ["ID", "ФИО", "Тип", "Последнее действие", "Время", "Статус"]
        )
        guests_table.setStyleSheet(
            """
            QTableWidget {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                font-size: 15px;
                selection-background-color: #cee7e4;
                selection-color: #222;
            }
            QHeaderView::section {
                background-color: #7BA89F;
                color: white;
                padding: 8px;
                border: 1px solid #e0e0e0;
                font-weight: bold;
            }
            QHeaderView::section:first {
                border-top-left-radius: 10px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 10px;
            }
            QTableWidgetItem {
                padding: 5px;
            }
        """
        )
        guests_table.verticalHeader().setVisible(False)
        guests_table.setEditTriggers(QTableWidget.NoEditTriggers)
        guest_history = [
            h for h in history if h.get("role") in ["Гость", "Группа гостей"]
        ]
        guest_history.sort(key=lambda x: x.get("time", ""), reverse=True)
        guest_actions = {}
        for action in guest_history:
            guest_id = action.get("id")
            if guest_id not in guest_actions:
                guest_actions[guest_id] = action
        guests_table.setRowCount(len(guest_actions))
        for row, (guest_id, action) in enumerate(guest_actions.items()):
            guests_table.setItem(row, 0, QTableWidgetItem(guest_id))
            guests_table.setItem(row, 1, QTableWidgetItem(action.get("name", "")))
            guests_table.setItem(row, 2, QTableWidgetItem(action.get("role", "")))
            guests_table.setItem(
                row, 3, QTableWidgetItem(action.get("action", "").capitalize())
            )
            guests_table.setItem(row, 4, QTableWidgetItem(action.get("time", "")))
            status = "На месте" if action.get("action") == "вход" else "Отсутствует"
            status_item = QTableWidgetItem(status)
            status_item.setForeground(
                QBrush(QColor("#27ae60" if status == "На месте" else "#e74c3c"))
            )
            guests_table.setItem(row, 5, status_item)

        guests_layout.addWidget(guests_table)
        tab_widget.addTab(guests_tab, "Гости")

        self.work_layout.addWidget(tab_widget)

    def add_employee_dialog(self):
        dlg = AddEmployeeDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            first_name, last_name, emp_id, phone, photo_path = dlg.get_data()
            if any(e.get("id") == emp_id for e in self.employees):
                QMessageBox.warning(
                    self, "Ошибка", f"Сотрудник с ID {emp_id} уже существует."
                )
                return
            new_emp = {
                "id": emp_id,
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone,
                "photo_path": photo_path,
            }
            self.employees.append(new_emp)
            self.save_employees()
            QMessageBox.information(self, "Успех", "Сотрудник успешно добавлен!")
            self.show_employees(force_update=True)
