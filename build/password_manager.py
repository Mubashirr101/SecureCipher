import sys
import cryptography
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QFrame,
    QListView,
    QMessageBox,
    QSpacerItem,
    QSizePolicy,
    QLayout,
    QSplitter,
)
from PySide6.QtCore import Qt, QStringListModel
import sqlite3
import hashlib
from cryptography.fernet import Fernet
import os
from PySide6.QtGui import QIcon
from PySide6 import QtCore
from custom_button import CustomButton, CustomHoverButton
from themesignal import emitter
from ui_shadow import create_drop_shadow



class PasswordManager(QMainWindow):
    def __init__(self):
        print("PasswordManager init")
        super().__init__()
        self.theme = "classic"
        emitter.theme_signal.connect(self.changeTheme)
        self.initUI()




    def changeTheme(self, theme):

        self.theme = theme
        self.stylsheetset_1()
        self.stylsheetset_2()
        # self.show()


    def initUI(self):

        # Initialize UI elements
        self.setWindowTitle("Password Manager")
        # self.setGeometry(100, 100, 800, 500)
        # self.setStyleSheet("Background-color:#ECB365;")
        self.pass_entry_buttons_frame = QFrame()

        # Authentication widgets
        self.auth_label = QLabel("Login/Signup")
        self.login_username_label = QLabel("Username: ")
        self.login_username_input = QLineEdit()
        # self.login_username_input.setStyleSheet(
        #     "color:white; background-color:#064663;"
        # )
        self.login_password_label = QLabel("Password: ")
        self.login_password_input = QLineEdit()
        # self.login_password_input.setStyleSheet(
        #     "color:white; background-color:#064663;"
        # )
        self.login_password_input.setEchoMode(QLineEdit.Password)
        self.login_button = CustomHoverButton("Login", min_size=(80, 30), max_size=(80, 30))
        self.signup_button = CustomHoverButton("Signup", min_size=(80, 30), max_size=(80, 30))

        # Password manager widgets


        self.auth_frame = QFrame()
        # self.auth_frame.setStyleSheet("color:#0000000;background-color: #507A94; border:2px solid #000000; border-radius:9px;")
        self.frame0 = QFrame()
        self.frame1 = QFrame()
        self.frame2 = QFrame()
        self.frame3 = QFrame()

        self.title_label = QLabel("Credentials: ")
        # self.title_label.setStyleSheet("color:white;")
        self.title_label.setMaximumHeight(25)
        self.website_input_label = QLabel("Website Name: ")
        self.website_input_label.setMinimumWidth(100)
        self.website_input = QLineEdit()
        self.website_input.setMinimumHeight(25)
        # self.website_input.setStyleSheet("color:black; background-color:white;")
        self.username_entry_label = QLabel("Username: ")
        self.username_entry_label.setMinimumWidth(100)
        self.username_entry = QLineEdit()
        self.username_entry.setMinimumHeight(25)
        # self.username_entry.setStyleSheet("color:black; background-color:white;")
        self.password_entry_label = QLabel("Password: ")
        self.password_entry_label.setMinimumWidth(100)
        self.password_entry = QLineEdit(self.pass_entry_buttons_frame)
        self.password_entry.setMinimumHeight(25)
        # self.password_entry.setStyleSheet("color:black; background-color:white;")
        self.password_entry.setEchoMode(QLineEdit.Password)
        # Set read-only initially
        self.website_input.setReadOnly(True)
        self.username_entry.setReadOnly(True)
        self.password_entry.setReadOnly(True)

        # Logout button
        self.logout_button = CustomButton("Logout",min_size=(130,40),max_size=(130,40))
        # self.logout_button.setStyleSheet(
        #     "color:white; background-color:#FF5733;border-radius:6px;"
        # )
        self.logout_button.setMaximumHeight(40)
        self.logout_button.setMaximumWidth(130)

        # copy password button
        self.copy_password_button = CustomHoverButton(self.pass_entry_buttons_frame,min_size=(30,25),max_size=(30,25))
        # self.copy_password_button.setStyleSheet("color:white; background-color:#064663;" )
        self.copy_password_button.setIcon(QIcon("resources/copy.png"))
        self.copy_password_button.setIconSize(QtCore.QSize(18, 18))
        # self.copy_password_button.setMinimumHeight(22)
        # self.copy_password_button.setMaximumWidth(250)

        #pass strength meter
        self.password_strength_label = QLabel("Password Strength: ")
        self.password_strength_value_label = QLabel()
        self.password_strength_value_label.setMinimumWidth(100)

        #show/hide password button
        self.show_password_button = CustomHoverButton(self.pass_entry_buttons_frame,min_size=(30,25),max_size=(30,25))
        self.show_password_button.setIcon(QIcon("resources/view.png"))
        self.show_password_button.setIconSize(QtCore.QSize(18, 18))
        self.show_password_button.setCheckable(True)
        self.update_show_pass_button_icon(False)  # Set initial icon

        self.website_list = QListView()
        # self.website_list.setStyleSheet("color:white; background-color:#064663;")
        self.website_list_model = QStringListModel()  # Add this line to create a model
        self.website_list.setModel(
            self.website_list_model
        )  # Set the model for the QListView
        self.edit_button = CustomButton("Edit",min_size=(130,40),max_size=(130,40))
        # self.edit_button.setStyleSheet("color:white; background-color:#04293A;")
        self.edit_button.setMaximumHeight(40)
        self.edit_button.setMaximumWidth(130)

        self.save_button = CustomButton("Save",min_size=(130,40),max_size=(130,40))
        # self.save_button.setStyleSheet("color:white; background-color:#04293A;")
        self.save_button.setMaximumHeight(40)
        self.save_button.setMaximumWidth(130)
        self.add_new_button = CustomButton("Add New")
        # self.add_new_button.setStyleSheet("color:white; background-color:#04293A;")
        self.add_new_button.setMaximumHeight(40)
        self.add_new_button.setMaximumWidth(130)
        self.delete_button = CustomButton("Delete",min_size=(130,40),max_size=(130,40))
        # self.delete_button.setStyleSheet("color:white; background-color:#FF5733;")  # You can customize the color
        self.delete_button.setMaximumHeight(40)
        self.delete_button.setMaximumWidth(130)

        # spacers for the buttons
        self.spacer1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.spacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.spacer3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.spacer4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.spacer5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Layouts
        self.main_layout = QVBoxLayout()
        self.auth_layout = QVBoxLayout()
        self.vault_layout = QHBoxLayout()
        self.splitter = QSplitter()

        # Set up authentication frame
        self.setup_auth_layout()

        # Set up password manager frame
        self.setup_vault_layout()

        # Set main layout
        self.main_layout.addLayout(self.auth_layout)
        self.main_layout.addLayout(self.vault_layout)

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

        # Connect signals and slots
        self.login_button.clicked.connect(self.authenticate_user)
        self.signup_button.clicked.connect(self.signup_user)
        self.edit_button.clicked.connect(self.enable_edit_mode)
        self.save_button.clicked.connect(self.save_changes)
        self.add_new_button.clicked.connect(self.add_new_entry)
        self.delete_button.clicked.connect(self.delete_entry)
        self.website_list.clicked.connect(self.load_entry)
        self.logout_button.clicked.connect(self.logout)
        self.copy_password_button.clicked.connect(self.copy_password)
        self.show_password_button.clicked.connect(self.toggle_password_visibility)
        self.password_entry.textChanged.connect(self.update_password_strength)






        # Database initialization
        self.db_connection = sqlite3.connect("password_manager.db")
        self.create_tables()

        # Load the encryption key
        self.key = self.load_key()

    def update_password_strength(self, text):
        print("Text:", text)
        strength = self.calculate_password_strength(text)
        self.password_strength_value_label.setText(strength)

    def calculate_password_strength(self,password):
        score = 0
        length = len(password)

        if any(char.isdigit() for char in password):
            score += 1
        if any(char.islower() for char in password):
            score += 1
        if any(char.isupper() for char in password):
            score += 1
        if any(char in "!@#$%^&*()_+-=[]{};:'\|,.<>?/~`" for char in password):
            score += 1
        if length >= 8:
            score += 1

        if score < 2:
            return "Weak"
        elif score < 4:
            return "Medium"
        else:
            return "Strong"

    def toggle_password_visibility(self, checked):
        if checked:
            self.password_entry.setEchoMode(QLineEdit.Normal)
        else:
            self.password_entry.setEchoMode(QLineEdit.Password)
        self.update_show_pass_button_icon(checked)

    def update_show_pass_button_icon(self, checked):
        icon_name = "hide.png" if checked else "view.png"
        self.show_password_button.setIcon(QIcon(f"resources/{icon_name}"))

    def stylsheetset_1(self):
        if self.theme == "classic":
            self.setStyleSheet("Background-color:#ECB365;")
            self.auth_frame.setStyleSheet("color:white;background-color: #04293A; border:1px solid #04293A; border-radius:6px;")
            self.auth_label.setStyleSheet("color:white; border:1px solid #04293A; border-radius:9px;")
            self.login_username_label.setStyleSheet("color:white;background-color:#04293A;border:1px solid #04293A; border-radius:9px;")
            self.login_username_input.setStyleSheet( "color:white; background-color:#064663;border:1px solid #04293A; border-radius:10px;padding:5px;")
            self.login_password_label.setStyleSheet("color:white;background-color:#04293A;border:1px solid #04293A; border-radius:9px;")
            self.login_password_input.setStyleSheet( "color:white; background-color:#064663;border:1px solid #04293A; border-radius:10px;padding:5px;")
            self.login_button.setStyleSheet("color:white; background-color:#064663;border-radius:6px;border:1px solid #064663;")
            self.signup_button.setStyleSheet("color:white; background-color:#064663;border-radius:6px;border:1px solid #064663;")

        elif self.theme == "light":
            self.setStyleSheet("Background-color:#FFFFFF;")
            self.auth_frame.setStyleSheet("background-color:#507A94; border:2px solid #000000; border-radius:9px;color:#FFFFFF;")
            self.auth_label.setStyleSheet("color:white; border:2px solid #507A94; border-radius:9px;")
            self.login_username_label.setStyleSheet("color:white;border:1px solid #507A94; border-radius:9px;")
            self.login_password_label.setStyleSheet("color:white;border:1px solid #507A94; border-radius:9px;")
            self.login_username_input.setStyleSheet( "color:#000000; background-color:#FFFFFF;border:1px solid #000000; border-radius:9px;padding:5px;")
            self.login_password_input.setStyleSheet("color:#000000; background-color:#FFFFFF;border:1px solid #000000; border-radius:9px;padding:5px;")
            self.login_button.setStyleSheet("color:white; background-color:#324C5C;border-radius:6px;border:1px solid #000000;")
            self.signup_button.setStyleSheet("color:white; background-color:#324C5C;border-radius:6px;border:1px solid #000000;")



    def stylsheetset_2(self):
        if self.theme == "classic":
            self.vault_label.setStyleSheet("color:white;border:1px solid #04293A; border-radius:9px;")
            self.row4_layout_frame.setStyleSheet(
                "color:white;background-color: #064663; border:1px solid #064663; border-radius:6px;")
            self.website_input_label.setStyleSheet("color:white;border:1px solid #064663; border-radius:9px;")
            self.username_entry_label.setStyleSheet("color:white;border:1px solid #064663; border-radius:9px;")
            self.password_entry_label.setStyleSheet("color:white;border:1px solid #064663; border-radius:9px;")
            self.pass_entry_buttons_frame.setStyleSheet(
                "background-color:#FFFFFF;border:1px solid #000000; border-radius:9px;")
            self.title_label.setStyleSheet("color:white;")
            self.website_input.setStyleSheet("color:black; background-color:white;")
            self.username_entry.setStyleSheet("color:black; background-color:white;")
            self.password_entry.setStyleSheet("color:black; background-color:white;border:1px solid #FFFFFF; border-radius:9px;")
            self.logout_button.setStyleSheet("color:white; background-color:#FF5733;border-radius:6px;")
            self.copy_password_button.setStyleSheet(
                "QPushButton {color:white; background-color:#FFFFFF;border:0px solid #000000;}"
                "QPushButton:hover { color: #000000; background-color: #FFFFFF; border: 1px solid #000000; }")
            self.show_password_button.setStyleSheet(
                "QPushButton {color:white; background-color:#FFFFFF;border:0px solid #000000;}"
                "QPushButton:hover { color: #000000; background-color: #FFFFFF; border: 1px solid #000000; }")
            self.website_list.setStyleSheet("color:white; background-color:#064663;")
            self.edit_button.setStyleSheet("color:white; background-color:#04293A;")
            self.save_button.setStyleSheet("color:white; background-color:#04293A;")
            self.add_new_button.setStyleSheet("color:white; background-color:#04293A;")
            self.delete_button.setStyleSheet("color:white; background-color:#FF5733;")  # You can customize the color
            self.frame0.setStyleSheet("color:white;background-color: #04293A; border:10px solid #ffff; border-radius:6px;")
            self.frame1.setStyleSheet("color:white;background-color:#064663; border:10px solid #ffff; border-radius:6px;")
            self.frame2.setStyleSheet("color:white;background-color: #04293A; border:1px solid #04293A; border-radius:6px;")
            self.splitter.setStyleSheet("QSplitter::handle {background-color: #ECB365;border: 3px solid #ECB365;border-radius:9px}")
        elif self.theme == "light":
            self.frame0.setStyleSheet("color:white;background-color: #507A94; border:3px solid #000000; border-radius:9px;")
            self.frame1.setStyleSheet("color:white;background-color:#507A94; border:1px solid #507A94; border-radius:6px;")
            self.frame2.setStyleSheet("color:white;background-color: #507A94; border:2px solid #000000; border-radius:9px;")
            self.vault_label.setStyleSheet("color:white;border:1px solid #507A94; border-radius:9px;")
            self.row4_layout_frame.setStyleSheet("color:white;background-color: #507A94; border:1px solid #507A94; border-radius:6px;")
            self.splitter.setStyleSheet("QSplitter::handle {background-color: #FFFFFF;border: 3px solid #FFFFFF;border-radius:9px}")
            self.title_label.setStyleSheet("color:white;border:1px solid #507A94; border-radius:9px;")
            self.website_input.setStyleSheet("color:black; background-color:white;border:1px solid #000000; border-radius:9px;padding:5px; ")
            self.website_input_label.setStyleSheet("color:white;border:1px solid #507A94; border-radius:9px;")
            self.username_entry_label.setStyleSheet("color:white;border:1px solid #507A94; border-radius:9px;")
            self.username_entry.setStyleSheet("color:black; background-color:white;border:1px solid #000000; border-radius:9px;padding:5px;")
            self.password_entry_label.setStyleSheet("color:white;border:1px solid #507A94; border-radius:9px;")
            self.password_entry.setStyleSheet("color:black; background-color:white;border:1px solid #FFFFFF; border-radius:9px;")
            self.pass_entry_buttons_frame.setStyleSheet("background-color:#FFFFFF;border:1px solid #000000; border-radius:9px;")
            self.copy_password_button.setStyleSheet(
                "QPushButton {color:white; background-color:#FFFFFF;border:0px solid #000000;}"
                "QPushButton:hover { color: #000000; background-color: #FFFFFF; border: 1px solid #000000; }")
            self.show_password_button.setStyleSheet(
                "QPushButton {color:white; background-color:#FFFFFF;border:0px solid #000000;}"
                "QPushButton:hover { color: #000000; background-color: #FFFFFF; border: 1px solid #000000; }")
            self.website_list.setStyleSheet("color:#000000; background-color:#FFFFFF;border:1px solid #000000; border-radius:9px;padding:5px;")
            self.edit_button.setStyleSheet("color:white; background-color:#324C5C;border:1px solid #000000; border-radius:9px;padding:5px;")
            self.save_button.setStyleSheet("color:white; background-color:#324C5C;border:1px solid #000000; border-radius:9px;padding:5px;")
            self.add_new_button.setStyleSheet("color:white; background-color:#324C5C;border:1px solid #000000; border-radius:9px;padding:5px;")
            self.delete_button.setStyleSheet("color:white; background-color:#FF5733;border:1px solid #000000;border-radius:9px;")
            self.logout_button.setStyleSheet("color:white; background-color:#FF5733;border:1px solid #000000;border-radius:9px;")




    def setup_auth_layout(self):
        # Create a frame for authentication widgets
        self.stylsheetset_1()
        self.auth_frame.setFixedHeight(250)
        self.auth_frame.setFixedWidth(300)


        self.auth_layout.addWidget(self.auth_frame)

        # Use QVBoxLayout for the frame
        auth_frame_layout = QVBoxLayout(self.auth_frame)

        auth_frame_layout.addWidget(self.auth_label)
        auth_frame_layout.addWidget(self.login_username_label)
        auth_frame_layout.addWidget(self.login_username_input)
        auth_frame_layout.addWidget(self.login_password_label)
        auth_frame_layout.addWidget(self.login_password_input)
        auth_frame_buttons_layout = QHBoxLayout(self.auth_frame)
        auth_frame_buttons_layout.addWidget(self.login_button)
        auth_frame_buttons_layout.addWidget(self.signup_button)
        auth_frame_buttons_layout.setContentsMargins(0, 20, 0, 5)
        auth_frame_layout.addLayout(auth_frame_buttons_layout)

        # Align the frame within the main layout
        self.auth_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        create_drop_shadow(self.auth_frame)

    def setup_vault_layout(self):
        # Create self.frame3 to wrap frame1 and frame2
        # Frame 1
        frame0_layout = QVBoxLayout()
        frame0_layout.addWidget(self.title_label)
        # frame0.setStyleSheet( "color:white;background-color: #04293A; border:10px solid #ffff; border-radius:6px;")
        # frame1.setStyleSheet( "color:white;background-color:#064663; border:10px solid #ffff; border-radius:6px;")
        # Vertical layout for frame1
        layout1 = QVBoxLayout()
        # Row 1: Website input
        row1_layout = QHBoxLayout()
        row1_layout.addWidget(self.website_input_label)
        row1_layout.addWidget(self.website_input)
        layout1.addLayout(row1_layout)
        # Row 2: Username entry
        row2_layout = QHBoxLayout()
        row2_layout.addWidget(self.username_entry_label)
        row2_layout.addWidget(self.username_entry)
        layout1.addLayout(row2_layout)
        # Row 3: Password entry
        row3_layout = QHBoxLayout()
        row3_layout.addWidget(self.password_entry_label)

        self.pass_entry_buttons_frame.setFixedHeight(40)

        pass_entry_buttons_frame_layout = QHBoxLayout(self.pass_entry_buttons_frame)
        pass_entry_buttons_frame_layout.addWidget(self.password_entry)
        pass_entry_buttons_frame_layout.addWidget(self.show_password_button)
        pass_entry_buttons_frame_layout.addWidget(self.copy_password_button)
        pass_entry_buttons_frame_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        pass_entry_buttons_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.pass_entry_buttons_frame.setLayout(pass_entry_buttons_frame_layout)
        row3_layout.addWidget(self.pass_entry_buttons_frame)
        layout1.addLayout(row3_layout)

        row_pass_strenth = QHBoxLayout()
        row_pass_strenth.addWidget(self.password_strength_label)
        row_pass_strenth.addWidget(self.password_strength_value_label)
        row_pass_strenth.setAlignment(Qt.AlignmentFlag.AlignCenter)
        row_pass_strenth.setContentsMargins(0, 0, 0, 0)
        layout1.addLayout(row_pass_strenth)
        # Row 4: Buttons
        self.row4_layout_frame = QFrame()
        self.row4_layout_frame.setMaximumWidth(900)
        self.row4_layout_frame.setMaximumHeight(70)
        row4_layout = QHBoxLayout(self.row4_layout_frame)
        row4_layout.setSizeConstraint(QLayout.SetMinimumSize)
        row4_layout.addItem(self.spacer1)
        row4_layout.addWidget(self.edit_button)
        row4_layout.addItem(self.spacer2)
        row4_layout.addWidget(self.save_button)
        row4_layout.addItem(self.spacer3)
        row4_layout.addWidget(self.add_new_button)
        row4_layout.addItem(self.spacer4)
        row4_layout.addWidget(self.delete_button)
        row4_layout.addItem(self.spacer5)

        layout1.addWidget(self.row4_layout_frame)
        layout1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame1.setLayout(layout1)
        frame0_layout.addWidget(self.frame1)
        self.frame0.setLayout(frame0_layout)
        self.frame0.setMaximumHeight(350)
        self.frame0.setMaximumWidth(650)

        # Frame 2
        layout2 = QVBoxLayout()
        self.vault_label = QLabel("Password Vault")
        layout2.addWidget(self.vault_label)
        layout2.addWidget(self.website_list)
        self.frame2.setLayout(layout2)
        # frame2.setStyleSheet("color:white;background-color: #04293A; border:1px solid #04293A; border-radius:6px;" )

        # Create a layout for self.frame3
        layout3 = QHBoxLayout(self.frame3)
        logoutbtn_cred_edit_frame = QFrame()
        logoutbtn_cred_edit_layout = QVBoxLayout(logoutbtn_cred_edit_frame)
        logoutbtn_cred_edit_layout.addWidget(self.frame0)
        logoutbtn_cred_edit_layout.addWidget(self.logout_button)

        self.splitter.addWidget(logoutbtn_cred_edit_frame)
        create_drop_shadow(self.frame2)
        self.splitter.addWidget(self.frame2)
        # splitter.setStyleSheet("QSplitter::handle {background-color: white;border: 1px solid grey;borgder-radius:6px}")
        layout3.addWidget(self.splitter)

        self.stylsheetset_2()



        ##QMessage Box
        self.copy_password_message = QMessageBox()

        # Set up Vault layout

        self.vault_layout.addWidget(self.frame3)
        create_drop_shadow(self.frame0)

        self.frame3.hide()


    def authenticate_user(self):
        self.username = self.login_username_input.text()
        password = self.hash_password(self.login_password_input.text())

        message_box = QMessageBox(self)
        if self.theme == "classic":
            message_box.setStyleSheet("background-color: #04293A; color: white;border-radius:6px;")
        elif self.theme == "light":
            message_box.setStyleSheet("background-color: #507A94; color: white;border-radius:6px;")

        # Create a custom QPushButton stylesheet

        if self.theme == "classic":
            button_style = (
                "QPushButton {"
                "   color: white;"
                "   background-color: #064663;"  # Change this color as needed
                "   border: 1px solid #ffff;"
                "   padding: 5px;"
                "   min-width: 70px;"
                "   min-height: 25px;"
                "   margin-right: 5px;"
                "}"
                "QPushButton:hover {"
                "   background-color: #2980b9;"
                "   color:#FFFFFF"# Change this color as needed
                "}"
            )
        elif self.theme == "light":
            button_style = (
                "QPushButton {"
                "   color: #000000;"
                "   background-color: #FFFFFF;"  # Change this color as needed
                "   border: 1px solid #324C5C;"
                "   padding: 5px;"
                "   min-width: 70px;"
                "   min-height: 25px;"
                "   margin-right: 5px;"
                "}"
                "QPushButton:hover {"
                "   background-color: #324C5C;"
                "   color: #FFFFFF "
                "}"
            )

        # Authenticate user
        cursor = self.db_connection.cursor()
        cursor.execute(
            "SELECT * FROM user_table WHERE username=? AND password=?",
            (self.username, password),
        )
        user = cursor.fetchone()

        if user:
            self.show_vault()
        else:
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Authentication Failed")
            message_box.setText("Authentication Failed, Invalid username or password")
            ok_button = QPushButton("OK")
            ok_button.clicked.connect(message_box.accept)
            ok_button.setStyleSheet(button_style)
            message_box.addButton(ok_button, QMessageBox.AcceptRole)
            message_box.exec()

    def signup_user(self):
        username = self.login_username_input.text()
        password = self.hash_password(self.login_password_input.text())
        signup_message_box = QMessageBox(self)
        if self.theme == "classic":
            signup_message_box.setStyleSheet("background-color: #04293A; color: white;border-radius:6px;")
        elif self.theme == "light":
            signup_message_box.setStyleSheet("background-color: #507A94; color: white;border-radius:6px;")

        # Create a custom QPushButton stylesheet

        if self.theme == "classic":
            signup_button_style = (
                "QPushButton {"
                "   color: white;"
                "   background-color: #064663;"  # Change this color as needed
                "   border: 1px solid #ffff;"
                "   padding: 5px;"
                "   min-width: 70px;"
                "   min-height: 25px;"
                "   margin-right: 5px;"
                "}"
                "QPushButton:hover {"
                "   background-color: #2980b9;"
                "   color:#FFFFFF"  # Change this color as needed
                "}"
            )
        elif self.theme == "light":
            signup_button_style = (
                "QPushButton {"
                "   color: #000000;"
                "   background-color: #FFFFFF;"  # Change this color as needed
                "   border: 1px solid #324C5C;"
                "   padding: 5px;"
                "   min-width: 70px;"
                "   min-height: 25px;"
                "   margin-right: 5px;"
                "}"
                "QPushButton:hover {"
                "   background-color: #324C5C;"
                "   color: #FFFFFF "
                "}"
            )




        # Signup logic
        cursor = self.db_connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO user_table (username, password) VALUES (?, ?)",
                (username, password),
            )
            signup_message_box.setIcon(QMessageBox.Information)
            signup_message_box.setWindowTitle("SignUp Successful")
            signup_message_box.setText(f"New account: {username} added successfully")
            signupok_button = QPushButton("OK")
            signupok_button.clicked.connect(signup_message_box.accept)
            signupok_button.setStyleSheet(signup_button_style)
            signup_message_box.addButton(signupok_button, QMessageBox.AcceptRole)
            signup_message_box.exec()

        except Exception as e:
            # Handle any exceptions here
            print("Error:", e)
            return  # Exit the method if an error occurs



    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def show_vault(self):
        # Hide the authentication frame
        self.auth_frame.hide()
        self.frame3.show()

        # Clear authentication input fields
        self.login_username_input.clear()
        self.login_password_input.clear()

        # Load website list
        self.update_website_list()

    def create_tables(self):
        cursor = self.db_connection.cursor()

        # Create user_table
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS user_table (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)"
        )

        # Create vault_table
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS vault_table (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, website TEXT, username TEXT, password TEXT)"
        )

        self.db_connection.commit()

    def add_new_entry(self):
        # Clear the line edits for a fresh entry
        self.website_input.clear()
        self.username_entry.clear()
        self.password_entry.clear()

        # Enable editing for a new entry
        self.website_input.setReadOnly(False)
        self.username_entry.setReadOnly(False)
        self.password_entry.setReadOnly(False)

        # Optionally, you can set focus to the website_input for convenience
        self.website_input.setFocus()

    def load_entry(self, index):
        # Load the selected entry details
        selected_website = self.website_list.model().data(index)
        user_id = self.get_authenticated_user_id()

        cursor = self.db_connection.cursor()
        cursor.execute(
            "SELECT * FROM vault_table WHERE user_id=? AND website=?",
            (user_id, selected_website),
        )
        entry = cursor.fetchone()

        if entry:
            self.website_input.setText(entry[2])
            self.username_entry.setText(entry[3])
            decrypted_password = self.decrypt_password(entry[4])
            self.password_entry.setText(decrypted_password)

    def update_website_list(self):
        # Update the website list
        user_id = self.get_authenticated_user_id()
        print("User ID:", user_id)

        cursor = self.db_connection.cursor()
        cursor.execute("SELECT website FROM vault_table WHERE user_id=?", (user_id,))
        websites = [entry[0] for entry in cursor.fetchall()]
        print("Websites:", websites)
        model = self.website_list.model()
        model.setStringList(websites)

    def get_authenticated_user_id(self):
        # Get the ID of the authenticated user
        username = self.username

        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id FROM user_table WHERE username=?", (username,))
        result = cursor.fetchone()
        print("Result:", result)

        if result is not None:
            user_id = result[0]
            return user_id
        else:
            # Handle the case where the user is not found
            # You might want to show an error message or take appropriate action
            return None

    def enable_edit_mode(self):
        # Enable editing of the credentials
        self.website_input.setReadOnly(False)
        self.username_entry.setReadOnly(False)
        self.password_entry.setReadOnly(False)

    def save_changes(self):
        # Save the changes made to the credentials
        website = self.website_input.text()
        username = self.username_entry.text()
        password = self.encrypt_password(self.password_entry.text())
        # Get the user ID from the authenticated user
        user_id = self.get_authenticated_user_id()
        cursor = self.db_connection.cursor()
        # Check if the entry already exists
        cursor.execute(
            "SELECT * FROM vault_table WHERE user_id=? AND website=?",
            (user_id, website),
        )
        existing_entry = cursor.fetchone()

        if existing_entry:
            # Entry exists, update it
            cursor.execute(
                "UPDATE vault_table SET username=?, password=? WHERE user_id=? AND website=?",
                (username, password, user_id, website),
            )
        else:
            # Entry doesn't exist, insert a new one
            cursor.execute(
                "INSERT INTO vault_table (user_id, website, username, password) VALUES (?, ?, ?, ?)",
                (user_id, website, username, password),
            )

        self.db_connection.commit()
        # Update the website list
        self.update_website_list()
        # Disable editing after saving changes
        self.website_input.setReadOnly(True)
        self.username_entry.setReadOnly(True)
        self.password_entry.setReadOnly(True)

    def delete_entry(self):
        selected_index = self.website_list.selectedIndexes()
        if not selected_index:
            return

        selected_website = self.website_list.model().data(selected_index[0])
        user_id = self.get_authenticated_user_id()

        cursor = self.db_connection.cursor()
        cursor.execute(
            "DELETE FROM vault_table WHERE user_id=? AND website=?",
            (user_id, selected_website),
        )
        self.db_connection.commit()

        # Update the website list after deletion
        self.update_website_list()

        # Clear the input fields after deletion
        self.website_input.clear()
        self.username_entry.clear()
        self.password_entry.clear()

    def logout(self):
        # Show the authentication frame and hide the vault frame
        self.frame3.hide()
        self.auth_frame.show()

        # Clear any existing user information
        self.login_username_input.clear()
        self.login_password_input.clear()

        # Optionally, clear the website list and entry details
        self.website_list.model().setStringList([])
        self.website_input.clear()
        self.username_entry.clear()
        self.password_entry.clear()


        # Disable editing for a new entry
        self.website_input.setReadOnly(True)
        self.username_entry.setReadOnly(True)
        self.password_entry.setReadOnly(True)

    def load_key(self):
        """
        Loads the key from the current directory named `secret.key`
        """
        key_path = "secret.key"
        if not os.path.exists(key_path):
            self.generate_key()
        key = open(key_path, "rb").read()
        print(f"Loaded Key: {key}")
        return key

    def generate_key(self):
        """
        Generates a key and saves it into a file
        """
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
        self.key = key  # Set the key attribute

    def encrypt_password(self, password):
        """
        Encrypts the password
        """
        key = self.load_key()
        encoded_message = password.encode()
        f = Fernet(key)
        encrypted_message = f.encrypt(encoded_message)

        return encrypted_message

    def decrypt_password(self, encrypted_password):
        try:
            # Print the encrypted password for debugging
            print("Encrypted Password:", encrypted_password)

            # Decrypt the password
            f = Fernet(self.load_key())
            decrypted_message = f.decrypt(encrypted_password)
            return decrypted_message.decode()
        except cryptography.fernet.InvalidToken as e:
            print("Error during password decryption:", e)
            return None

    def copy_password(self):
        decrypted_password = self.password_entry.text()

        # Create a custom QMessageBox
        message_box = QMessageBox(self)
        message_box.setStyleSheet("background-color: #064663; color: white;border-radius:6px;")

        # Create a custom QPushButton stylesheet
        button_style = (
            "QPushButton {"
            "   color: white;"
            "   background-color: #04293A;"  # Change this color as needed
            "   border: 1px solid #ffff;"
            "   padding: 5px;"
            "   min-width: 70px;"
            "   min-height: 25px;"
            "   margin-right: 5px;"
            "}"
            "QPushButton:hover {"
            "   background-color: #2980b9;"  # Change this color as needed
            "}"
        )


        if decrypted_password:
            clipboard = QApplication.clipboard()
            clipboard.setText(decrypted_password)

            message_box.setIcon(QMessageBox.Information)
            message_box.setWindowTitle("Password Copied")
            message_box.setText("Password copied to clipboard.")

            # Add a custom OK button with the stylesheet
            ok_button = QPushButton("OK")
            ok_button.clicked.connect(message_box.accept)
            ok_button.setStyleSheet(button_style)
            message_box.addButton(ok_button, QMessageBox.AcceptRole)
        else:
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("No Password")
            message_box.setText("No password to copy.")

            # Add a custom OK button with the stylesheet
            ok_button = QPushButton("OK")
            ok_button.clicked.connect(message_box.accept)
            ok_button.setStyleSheet(button_style)
            message_box.addButton(ok_button, QMessageBox.AcceptRole)

        # Show the custom QMessageBox
        message_box.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordManager()
    window.show()
    sys.exit(app.exec())
