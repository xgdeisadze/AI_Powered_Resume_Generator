import sqlite3

from PySide6.QtCore import QRect
from PySide6.QtGui import QFont, QGuiApplication
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
)


class SelectUser(QWidget):
    def __init__(self, cursor: sqlite3.Cursor):
        super().__init__()
        self.cursor = cursor
        self.list_control = None
        self.user_data = []
        self.userID = None
        self.name = None
        self.email = None
        self.phone = None
        self.github = None
        self.other_link = None
        self.projects = None
        self.classes = None
        self.other = None
        self.setupWindow()

    def setupWindow(self):
        self.setWindowTitle("Select User Profile")
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)
        self.list_control = QListWidget()
        top_layout.addWidget(self.list_control)
        self.user_data = self.load_users()
        self.fill_user_info(self.user_data)
        user_data_panel = QVBoxLayout()
        self.fill_user_data_panel(user_data_panel)
        top_layout.addLayout(user_data_panel)
        self.list_control.currentItemChanged.connect(self.show_full_user_data)
        bottom_row = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.ok)
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.back)
        bottom_row.addWidget(ok_button)
        bottom_row.addWidget(back_button)
        main_layout.addLayout(bottom_row)
        self.setLayout(main_layout)
        self.set_size()

    def fill_user_data_panel(self, panel: QVBoxLayout):
        label_font = QFont("Arial", 12, QFont.Weight.Bold)
        user_id_label = QLabel("User ID:")
        user_id_label.setFont(label_font)
        panel.addWidget(user_id_label)
        self.userID = QLineEdit()
        panel.addWidget(self.userID)

        panel.addWidget(QLabel("E-Mail:"))
        self.email = QLineEdit()
        panel.addWidget(self.email)

        panel.addWidget(QLabel("Phone:"))
        self.phone = QTextEdit()
        panel.addWidget(self.phone)

        panel.addWidget(QLabel("Name:"))
        self.name = QLineEdit()
        panel.addWidget(self.name)

        panel.addWidget(QLabel("Github:"))
        self.github = QLineEdit()
        panel.addWidget(self.github)

        other_link = QLabel("Other Links:")
        panel.addWidget(other_link)
        self.other_link = QLineEdit()
        panel.addWidget(self.other_link)

        projects = QLabel("Projects:")
        panel.addWidget(projects)
        self.projects = QLineEdit()
        panel.addWidget(self.projects)

        classes = QLabel("Classes:")
        panel.addWidget(classes)
        self.classes = QLineEdit()
        panel.addWidget(self.classes)

        other = QLabel("Other:")
        panel.addWidget(other)
        self.other = QLineEdit()
        panel.addWidget(self.other)


    def load_users(self):
        self.cursor.execute("SELECT userID, email, phone, name, github, other_link, projects, classes, other FROM personal_info")
        return [{
             "userID": row[0],
             "email": row[1],
             "phone": row[2],
             "name": row[3],
             "github": row[4],
             "other_link": row[5],
             "projects": row[6],
             "classes": row[7],
             "other": row[8],}
        for row in self.cursor.fetchall()]


    def fill_user_info(self, user_data: list):
        for data in user_data:
            user_data_for_list = f"{data['name']} : {data['userID']}"
            item = QListWidgetItem(user_data_for_list, listview=self.list_control)
            item.setData(1, data["userID"])

    def set_size(self):
        screen = QGuiApplication.primaryScreen()
        available_geometry = screen.availableGeometry()
        width = available_geometry.width()
        height = available_geometry.height()
        self.setGeometry(
            QRect(width // 10, height // 10, width // 4, height // 2)
        )

    def show_full_user_data(self, current: QListWidgetItem, previous: QListWidgetItem):
        selected_data = current.data(1)
        data = get_complete_user_data(self.user_data, selected_data)
        self.userID.setText(data["userID"])
        self.email.setText(data["email"])
        self.phone.setText(data["phone"])
        self.name.setText(data["name"])
        self.github.setText(data["github"])
        self.other_link.setText(data["other_link"])
        self.projects.setText(data["projects"])
        self.classes.setText(data["classes"])
        self.other.setText(data["other"])

    def ok(self):
        self.cursor.execute("DELETE FROM selected_user;")
        current_item = self.list_control.currentItem()
        selected_data = current_item.data(1)
        data = get_complete_user_data(self.user_data, selected_data)
        data_to_insert = (
            data["userID"],
            data["email"],
            data["phone"],
            data["name"],
            data["github"],
            data["other_link"],
            data["projects"],
            data["classes"],
            data["other"]
        )
        insert_selected_user = """INSERT into selected_user(userID, email, phone, name, github, other_link, projects, classes, other)
         VALUES(?,?,?,?,?,?,?,?,?)"""
        self.cursor.execute(insert_selected_user, data_to_insert)
        self.close()


    def back(self):
        self.close()

def get_complete_user_data(user_list, user_id: str) -> dict:
    for user in user_list:
        if user["userID"] == user_id:
            return user