import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QFrame,QHBoxLayout,QMessageBox
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from cryptography.fernet import Fernet, InvalidToken
from custom_button import CustomButton , CustomHoverButton
from ui_shadow import create_drop_shadow
from themesignal import emitter


class FileEncryptionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print("FileEncryptionWindow init")
        self.theme = "classic"
        self.initUI()
        self.applyTheme()
        emitter.theme_signal.connect(self.changeTheme)


    def applyTheme(self):
        # print(f"Applying {theme} theme")
        stylesheet_file = "stylesheets/file_enc_dec_style_classic.qss"  # Use theme-specific stylesheets
        with open(stylesheet_file, "r") as f:
            stylesheet = f.read()
            self.setStyleSheet(stylesheet)

    def changeTheme(self, theme):
        self.hide()
        self.theme = theme
        print(self.theme)
        print(f"received signal: {theme}")
        stylesheet_file = f"stylesheets/file_enc_dec_style_{theme}.qss"
        with open(stylesheet_file, "r") as f:
            stylesheet = f.read()
            self.setStyleSheet(stylesheet)
        self.show()

    def initUI(self):
        self.setWindowTitle("File Encryption/Decryption")
        self.setStyleSheet("Background-color:#ECB365;")
        # Create main widget and layouts
        self.main_widget = QWidget(self)
        self.layout1 = QVBoxLayout(self.main_widget)
        self.layout2 = QHBoxLayout()
        self.layout3 = QVBoxLayout()

        # Key Input
        self.keyword_entry_frame = QFrame()
        self.keyword_entry_frame.setFixedHeight(80)
        self.keyword_entry_frame.setFixedWidth(400)
        self.keyword_entry_frame.setLayout(QHBoxLayout())
        self.key_label = QLabel(" Key: ",self.keyword_entry_frame)
        self.key_input = QLineEdit(self.keyword_entry_frame,placeholderText="Enter the Key")
        self.keyword_entry_frame.layout().addWidget(self.key_label)
        self.keyword_entry_frame.layout().addWidget(self.key_input)
        self.layout2.addWidget(self.keyword_entry_frame)
        self.layout2.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # File Selection Area
        self.file_selection_frame = QFrame()

        self.file_selection_frame.setLayout(QVBoxLayout())
        self.file_label = QLabel("Select File:",self.file_selection_frame)
        self.file_label.setFixedHeight(20)
        self.file_path_label = QLabel("",self.file_selection_frame)
        self.file_path_label.setWordWrap(True)
        self.file_path_label.setFixedHeight(50)
        self.file_selection_frame.layout().addWidget(self.file_label)
        self.file_selection_frame.layout().addWidget(self.file_path_label)
        # Designated Drop Area
        self.drop_area = QFrame(self)

        self.drop_area.setGeometry(QRect())  # Set the geometry for the designated drop area
        self.drop_area.setFrameShape(QFrame.Box)
        self.drop_area.setAcceptDrops(True)
        self.drop_area.setLayout(QVBoxLayout())
        self.droplabel = QLabel("Drop File Here")
        hlayout_label = QHBoxLayout()
        hlayout_label.addWidget(self.droplabel)
        hlayout_label.setAlignment(Qt.AlignHCenter)
        self.drop_area.layout().addLayout(hlayout_label)
        self.file_button = CustomHoverButton("Browse",min_size=(85,25),max_size=(85,25))
        self.file_button.setFixedHeight(25)
        self.file_button.setFixedWidth(85)
        self.file_button.clicked.connect(self.select_file)
        hlayout_button = QHBoxLayout()
        hlayout_button.addWidget(self.file_button)
        hlayout_button.setAlignment(Qt.AlignHCenter)
        self.drop_area.layout().addLayout(hlayout_button)
        self.file_selection_frame.layout().addWidget(self.drop_area)
        self.layout3.addWidget(self.file_selection_frame)
        self.layout3.setContentsMargins(0,30,0,0)

        #3 BUTTONS
        # Generate Key Button
        self.layout4 = QHBoxLayout()
        self.generate_key_button = CustomButton("Generate Key",min_size=(100,75),max_size=(100,75))
        self.generate_key_button.setFixedHeight(75)
        self.generate_key_button.clicked.connect(self.generate_key)
        self.layout4.addWidget(self.generate_key_button)
        # Encrypt Button
        self.encrypt_button = CustomButton("Encrypt",min_size=(100,75),max_size=(100,75))
        self.encrypt_button.clicked.connect(self.encrypt_file)
        self.layout4.addWidget(self.encrypt_button)
        # Decrypt Button
        self.decrypt_button = CustomButton("Decrypt",min_size=(100,75),max_size=(100,75))
        self.decrypt_button.clicked.connect(self.decrypt_file)
        self.layout4.addWidget(self.decrypt_button)
        self.layout4.setContentsMargins(50,0,0,0)
        self.layout2.addLayout(self.layout4)
        self.layout2.setContentsMargins(250,30,250,10)
        self.layout3.setContentsMargins(250,25,250,60)

        self.layout1.addLayout(self.layout2)
        self.layout1.addLayout(self.layout3)

        #dropshadow
        create_drop_shadow(self.file_selection_frame)
        create_drop_shadow(self.keyword_entry_frame)


        #setting object name for stylesheet
        self.keyword_entry_frame.setObjectName("keyword_entry_frame")
        self.key_input.setObjectName("key_input")
        self.key_label.setObjectName("key_label")
        self.file_selection_frame.setObjectName("file_selection_frame")
        self.file_label.setObjectName("file_label")
        self.file_path_label.setObjectName("file_path_label")
        self.drop_area.setObjectName("drop_area")
        self.droplabel.setObjectName("drop_label")
        self.file_button.setObjectName("file_button")
        self.generate_key_button.setObjectName("generate_key_button")
        self.encrypt_button.setObjectName("encrypt_button")
        self.decrypt_button.setObjectName("decrypt_button")



        self.setCentralWidget(self.main_widget)


    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select File")
        self.file_path_label.setText(file_path)

    def generate_key(self):
        key = Fernet.generate_key().decode()
        self.key_input.setText(key)

    def encrypt_file(self):
        file_path = self.file_path_label.text()
        key = self.key_input.text()

        try:
            with open(file_path, 'rb') as file:
                plaintext = file.read()

            f = Fernet(key)
            ciphertext = f.encrypt(plaintext)

            encrypted_file_path = file_path + '.encrypted'
            with open(encrypted_file_path, 'wb') as file:
                file.write(ciphertext)
            os.remove(file_path)  # Delete the original file
            self.show_success_message("File Encrypted", "File encrypted successfully.")
        except Exception as e:
            self.show_error_message("Encryption failed", str(e))

    def decrypt_file(self):
        file_path = self.file_path_label.text()
        key = self.key_input.text()

        try:
            with open(file_path, 'rb') as file:
                ciphertext = file.read()

            f = Fernet(key)
            plaintext = f.decrypt(ciphertext)

            decrypted_file_path = os.path.splitext(file_path)[0]  # Remove the '.encrypted' extension
            with open(decrypted_file_path, 'wb') as file:
                file.write(plaintext)
            os.remove(file_path)  # Delete the encrypted file
            self.show_success_message("Decryption Successful", "File decrypted successfully.")
        except InvalidToken as e:
            self.show_error_message("Decryption failed",
                                    "Invalid Fernet key. Please make sure the correct key is used.")
        except Exception as e:
            self.show_error_message("Decryption failed", str(e))

    def dragEnterEvent(self, event: QDragEnterEvent):
        mime_data = event.mimeData()
        urls = mime_data.urls()

        if urls and urls[0].isLocalFile() and self.drop_area.geometry().contains(event.pos()):
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        mime_data = event.mimeData()
        urls = mime_data.urls()

        if urls and urls[0].isLocalFile() and self.drop_area.geometry().contains(event.pos()):
            file_path = urls[0].toLocalFile()
            self.file_path_label.setText(file_path)

    def show_error_message(self, title, message):
        error_message = QMessageBox(self)
        if self.theme == "classic":
            error_message.setStyleSheet("background-color: #04293A; color: white;border-radius:6px;")
        elif self.theme == "light":
            error_message.setStyleSheet("background-color: #507A94; color: white;border-radius:6px;")
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
                "   color:#FFFFFF"  # Change this color as needed
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
        error_message.setIcon(QMessageBox.Critical)
        error_message.setWindowTitle(title)

        # Extract only the part after "No such file or directory"
        error_prefix = "[Errno 2] "
        if message.startswith(error_prefix):
            formatted_message = f"Error: {message[len(error_prefix):]}"
        else:
            formatted_message = f"Error: {message}"

        error_message.setText(formatted_message)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(error_message.accept)
        ok_button.setStyleSheet(button_style)
        error_message.addButton(ok_button, QMessageBox.AcceptRole)
        error_message.exec()

    def show_success_message(self, title, message):
        success_message = QMessageBox(self)
        if self.theme == "classic":
            success_message.setStyleSheet("background-color: #04293A; color: white;border-radius:6px;")
        elif self.theme == "light":
            success_message.setStyleSheet("background-color: #507A94; color: white;border-radius:6px;")

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
                "   color:#FFFFFF"  # Change this color as needed
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
        success_message.setIcon(QMessageBox.Information)
        success_message.setWindowTitle(title)
        success_message.setText(message)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(success_message.accept)
        ok_button.setStyleSheet(button_style)
        success_message.addButton(ok_button, QMessageBox.AcceptRole)
        success_message.exec()


if __name__ == "__main__":
    app = QApplication([])
    window = FileEncryptionWindow()
    window.show()
    app.exec()
