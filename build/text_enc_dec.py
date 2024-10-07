import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QGroupBox,
    QHBoxLayout,
    QButtonGroup,
    QRadioButton,
    QFrame,
    QMessageBox,
    QFileDialog,
)
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from vignere_cipher_algo import vigenere_cipher
from rsa_encryptor import RSAEncryptor  # Import the RSAEncryptor class
from custom_button import CustomButton, CustomHoverButton
from ui_shadow import create_drop_shadow
from themesignal import emitter
from rsakeygenerator import RSAKeyGenerator
class Txt_enc_Dec(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Txt_enc_Dec init")
        self.theme = "classic"
        self.initUI()
        self.applyTheme()
        emitter.theme_signal.connect(self.changeTheme)



    def applyTheme(self):
        # print(f"Applying {theme} theme")
        stylesheet_file = "stylesheets/text_enc_dec_style_classic.qss"  # Use theme-specific stylesheets
        with open(stylesheet_file, "r") as f:
            stylesheet = f.read()
            self.setStyleSheet(stylesheet)
    def changeTheme(self, theme):
        self.hide()
        self.theme = theme
        self.reset_radio_btns()
        print(self.theme)
        print(f"received signal: {theme}")
        stylesheet_file = f"stylesheets/text_enc_dec_style_{theme}.qss"
        with open(stylesheet_file, "r") as f:
            stylesheet = f.read()
            self.setStyleSheet(stylesheet)
        self.show()


    def initUI(self):

        print(self.theme)

        self.setWindowTitle("Text Encryption / Decryption")


        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.rsa_encryptor = RSAEncryptor()  # Create an instance of the RSAEncryptor class
        layout_main = QVBoxLayout()
        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()
        layout5 = QHBoxLayout()




        frame_1_2 = QFrame()
        radio_grp_box = QGroupBox("Encryption Algorithm: ", frame_1_2)
        radio_grp_box.setStyleSheet(
            "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 5px; }")
        radio_grp_box.setFixedHeight(95)
        radio_grp_box.setFixedWidth(300)
        self.radio_btn_grp = QButtonGroup(self)
        self.radio_button1 = QRadioButton("Vigenère Cipher")
        self.radio_button2 = QRadioButton("AES")
        self.radio_button3 = QRadioButton("RSA")
        self.radio_button4 = QRadioButton("None")
        self.reset_button = CustomHoverButton("Reset", min_size=(60, 25), max_size=(60, 25))
        self.reset_button.clicked.connect(self.reset_radio_btns)

        self.radio_btn_grp.addButton(self.radio_button1)
        self.radio_btn_grp.addButton(self.radio_button2)
        self.radio_btn_grp.addButton(self.radio_button3)
        self.radio_btn_grp.addButton(self.radio_button4)
        self.radio_btn_grp.addButton(self.reset_button)

        rad_btn_grp_layout = QHBoxLayout()
        rad_btn_grp_layout.addWidget(self.radio_button1)
        rad_btn_grp_layout.addWidget(self.radio_button2)
        rad_btn_grp_layout.addWidget(self.radio_button3)
        rad_btn_grp_layout.addWidget(self.reset_button)
        radio_grp_box.setLayout(rad_btn_grp_layout)
        self.radio_button1.toggled.connect(self.update_ui_based_on_encryption)
        self.radio_button2.toggled.connect(self.update_ui_based_on_encryption)
        self.radio_button3.toggled.connect(self.update_ui_based_on_encryption)
        layout2.addWidget(radio_grp_box)


        if self.theme == "classic":
            print('theme in gen key button: ', self.theme)
            self.generate_key_button = CustomButton("Generate Key(s)", self, min_size=(120, 90), max_size=(120, 90))
        elif self.theme == "light":
            print('theme in gen key button: ', self.theme)
            self.generate_key_button = CustomButton("Generate Key(s)", self, min_size=(120, 90), max_size=(120, 90))

        self.generate_key_button.setFixedWidth(120)
        self.generate_key_button.setFixedHeight(90)
        self.generate_key_button.clicked.connect(self.generate_key)
        layout2.addWidget(self.generate_key_button)

        frame_1_1 = QFrame(central_widget)
        frame_1_1.setFixedWidth(300)
        self.keyword_label = QLabel("Key:", frame_1_1)
        self.keyword_entry = self.CustomLineEdit(frame_1_1, placeholderText=" Enter keyword ")
        self.keyword_entry.setFixedHeight(30)
        layout4 = QHBoxLayout(frame_1_1)
        layout4.addWidget(self.keyword_label)
        layout4.addWidget(self.keyword_entry)
        frame_1_1.setLayout(layout4)
        layout2.addWidget(frame_1_1)

        frame_1_1_2_rsa_keys = QFrame(central_widget)
        self.rsa_keys_label = QLabel("RSA Keys:", frame_1_1_2_rsa_keys)
        frame_1_1_2_rsa_keys_layout = QVBoxLayout()
        twobuttonslayout = QHBoxLayout()
        frame_1_1_2_rsa_keys_layout.addWidget(self.rsa_keys_label)
        twobuttonslayout = QHBoxLayout()
        frame_1_1_2_rsa_keys_layout.addWidget(self.rsa_keys_label)
        if self.theme == "classic":
            print('theme in priv key button: ', self.theme)
            self.browse_private_key_button = CustomHoverButton(
                " Private Key", min_size=(80, 25), max_size=(80, 25)
            )
        elif self.theme == "light":
            print('theme in priv key button: ', self.theme)
            self.browse_private_key_button = CustomHoverButton(
                " Private Key", min_size=(80, 25), max_size=(80, 25)
            )

        self.browse_private_key_button.clicked.connect(self.browse_private_key)
        self.browse_private_key_button.setFixedSize(
            80, 25)

        if self.theme == "classic":
            print('theme in pub key button: ', self.theme)
            self.browse_public_key_button = CustomHoverButton(
                " Public Key", min_size=(80, 25), max_size=(80, 25)
            )
        elif self.theme == "light":
            print('theme in pub key button: ', self.theme)
            self.browse_public_key_button = CustomHoverButton(
                " Public Key", min_size=(80, 25), max_size=(80, 25)
            )

        self.browse_public_key_button.setFixedSize(80, 25)
        self.browse_public_key_button.clicked.connect(self.browse_public_key)
        twobuttonslayout.addWidget(self.browse_private_key_button)
        twobuttonslayout.addWidget(self.browse_public_key_button)
        frame_1_1_2_rsa_keys_layout.addLayout(twobuttonslayout)
        frame_1_1_2_rsa_keys.setLayout(frame_1_1_2_rsa_keys_layout)
        frame_1_1_2_rsa_keys.setFixedWidth(200)
        frame_1_1_2_rsa_keys.setFixedHeight(95)
        layout2.addWidget(frame_1_1_2_rsa_keys)



        if self.theme == "classic":
            print('theme in enc button: ', self.theme)
            self.encode_button = CustomButton("Encode", self, min_size=(100, 90), max_size=(100, 90))
        elif self.theme == "light":
            print('theme in enc button: ', self.theme)
            self.encode_button = CustomButton("Encode", self, min_size=(100, 90), max_size=(100, 90))

        self.encode_button.setFixedWidth(100)
        self.encode_button.setFixedHeight(90)

        self.encode_button.clicked.connect(self.encode)
        layout2.addWidget(self.encode_button)


        if self.theme == "classic":
            print('theme in dec button: ', self.theme)
            self.decode_button = CustomButton("Decode", self, min_size=(100, 90), max_size=(100, 90))
        elif self.theme == "light":
            print('theme in dec button: ', self.theme)
            self.decode_button = CustomButton("Decode", self, min_size=(100, 90), max_size=(100, 90))

        self.decode_button.setFixedWidth(100)
        self.decode_button.setFixedHeight(90)
        self.decode_button.clicked.connect(self.decode)
        layout2.addWidget(self.decode_button)
        layout2.addLayout(layout5)
        layout2.setContentsMargins(70, 30, 70, 10)
        frame_2_1 = QFrame()
        self.plain_text_label = QLabel("Plain Text:", frame_2_1)
        self.plain_text_entry = QTextEdit(frame_2_1)
        layout6 = QVBoxLayout(frame_2_1)
        layout6.addWidget(self.plain_text_label)
        layout6.addWidget(self.plain_text_entry)
        frame_2_1.setLayout(layout6)
        layout3.addWidget(frame_2_1)
        layout3.setContentsMargins(70, 25, 70, 50)

        frame_2_2 = QFrame()
        self.encoded_text_label = QLabel("Encrypted Text:", frame_2_2)
        self.encoded_text_entry = QTextEdit(frame_2_2)

        layout7 = QVBoxLayout(frame_2_2)
        layout7.addWidget(self.encoded_text_label)
        layout7.addWidget(self.encoded_text_entry)
        frame_2_2.setLayout(layout7)
        layout3.addWidget(frame_2_2)

        create_drop_shadow(frame_1_1)
        create_drop_shadow(frame_1_1_2_rsa_keys)
        create_drop_shadow(frame_1_2)
        create_drop_shadow(frame_2_1)
        create_drop_shadow(frame_2_2)
        create_drop_shadow(radio_grp_box)

        self.keyword_entry.setObjectName("keyword_entry")
        self.keyword_label.setObjectName("keyword_label")
        frame_1_1.setObjectName("frame_1_1")
        frame_1_1_2_rsa_keys.setObjectName("frame_1_1_2_rsa_keys")
        self.rsa_keys_label.setObjectName("rsa_keys_label")
        self.browse_private_key_button.setObjectName("browse_private_key_button")
        self.browse_public_key_button.setObjectName("browse_public_key_button")
        self.generate_key_button.setObjectName("generate_key_button")
        self.encode_button.setObjectName("encode_button")
        self.decode_button.setObjectName("decode_button")
        self.plain_text_entry.setObjectName("plain_text_entry")
        self.plain_text_label.setObjectName("plain_text_label")
        self.encoded_text_entry.setObjectName("encoded_text_entry")
        self.encoded_text_label.setObjectName("encoded_text_label")
        frame_2_1.setObjectName("frame_2_1")
        frame_2_2.setObjectName("frame_2_2")
        radio_grp_box.setObjectName("radio_grp_box")
        self.radio_button1.setObjectName("radio_button_1")
        self.radio_button2.setObjectName("radio_button_2")
        self.radio_button3.setObjectName("radio_button_3")
        self.reset_button.setObjectName("reset_button")
        # self.title_label.setObjectName("title_label")


        layout1.addLayout(layout2)
        layout1.addLayout(layout3)
        # layout_main.addWidget(self.title_label)
        layout_main.addLayout(layout1)
        central_widget.setLayout(layout_main)

    def reset_radio_btns(self):
        self.radio_btn_grp.setExclusive(False)
        self.radio_button1.setChecked(False)
        self.radio_button2.setChecked(False)
        self.radio_button3.setChecked(False)
        self.radio_button4.setChecked(False)
        self.radio_btn_grp.setExclusive(True)
        self.keyword_entry.clear()
        self.encoded_text_entry.clear()
        self.plain_text_entry.clear()


    def update_ui_based_on_encryption(self):
        # Disable/enable keyword frame based on selected encryption
        if self.radio_button3.isChecked():  # If RSA is selected
            self.keyword_label.setEnabled(False)
            self.keyword_entry.setEnabled(False)
        else:
            self.keyword_label.setEnabled(True)
            self.keyword_entry.setEnabled(True)

        # Disable/enable RSA keys frame based on selected encryption
        if self.radio_button1.isChecked() or self.radio_button2.isChecked():  # If Vigenère or AES is selected
            self.rsa_keys_label.setEnabled(False)
            self.browse_private_key_button.setEnabled(False)
            self.browse_public_key_button.setEnabled(False)
        else:
            self.rsa_keys_label.setEnabled(True)
            self.browse_private_key_button.setEnabled(True)
            self.browse_public_key_button.setEnabled(True)

    def generate_key(self):
        try:
            if self.radio_button2.isChecked(): # AES encryption
                key = get_random_bytes(32)  # 32 bytes for a 256-bit key
                self.keyword_entry.setText(b64encode(key).decode())
            elif self.radio_button3.isChecked(): # RSA encryption
                RSAKeyGenerator.generate_keys(self=self)
        except Exception as e:
            self.show_error_message("Error generating key", str(e))

    def browse_private_key(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("PEM files (*.pem)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            if self.plain_text_entry.document().isEmpty():
                self.rsa_encryptor.set_decryption_clicked()
            self.rsa_encryptor.set_private_key_from_file(file_path)  # Set private key

    def browse_public_key(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("PEM files (*.pem)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            if self.plain_text_entry.document().isEmpty():
                self.rsa_encryptor.set_decryption_clicked()
            self.rsa_encryptor.set_public_key_from_file(file_path)  # Set public key

    def encode(self):
        try:
            if self.plain_text_entry.toPlainText() == "":
                self.show_error_message(" Error ", "Please enter the text to be encrypted")
                return
            else:
                if self.radio_button1.isChecked():  # Vigenere Cipher
                    key = self.keyword_entry.text()
                    plaintext = self.plain_text_entry.toPlainText()
                    encoded_txt = vigenere_cipher(plaintext, key, mode='encrypt')

                    self.encoded_text_entry.clear()
                    self.encoded_text_entry.setPlainText(encoded_txt)
                    self.plain_text_entry.clear()

                elif self.radio_button2.isChecked():  # AES encryption
                    key = b64decode(self.keyword_entry.text())
                    plaintext = self.plain_text_entry.toPlainText().encode('utf-8')

                    cipher = AES.new(key, AES.MODE_CBC)
                    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

                    self.encoded_text_entry.clear()
                    self.encoded_text_entry.setPlainText(b64encode(cipher.iv + ciphertext).decode())
                    self.plain_text_entry.clear()

                elif self.radio_button3.isChecked():  # RSA encryption
                    plaintext = self.plain_text_entry.toPlainText()
                    ciphertext, signature = self.rsa_encryptor.encrypt_and_sign(plaintext)

                    self.encoded_text_entry.clear()
                    self.encoded_text_entry.setPlainText(
                        f"Ciphertext: {b64encode(ciphertext).decode()}\nSignature: {b64encode(signature).decode()}")
                    self.plain_text_entry.clear()

                    pass
                else:
                    self.show_error_message(" Error ", "Please select an encryption algorithm")

        except ValueError as ve:
            self.show_error_message(" Error ", str(ve))

    def decode(self):
        try:
            if self.encoded_text_entry.toPlainText() == "":
                self.show_error_message(" Error ", "Please enter the text to be decrypted")
                return
            else:
                if self.radio_button1.isChecked():  # Vigenere Cipher
                    key = self.keyword_entry.text()
                    encoded_txt = self.encoded_text_entry.toPlainText()
                    decoded_txt = vigenere_cipher(encoded_txt, key, mode='decrypt')

                    self.plain_text_entry.clear()
                    self.plain_text_entry.setPlainText(decoded_txt)
                    self.encoded_text_entry.clear()

                elif self.radio_button2.isChecked():  # AES decryption
                    key = b64decode(self.keyword_entry.text())
                    encrypted_text = b64decode(self.encoded_text_entry.toPlainText())

                    iv = encrypted_text[:16]
                    ciphertext = encrypted_text[16:]

                    cipher = AES.new(key, AES.MODE_CBC, iv)
                    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

                    self.plain_text_entry.setPlainText(plaintext.decode('utf-8'))
                    self.encoded_text_entry.clear()

                elif self.radio_button3.isChecked():  # RSA decryption
                    self.rsa_encryptor.set_decryption_clicked()  # Set decryption button clicked
                    ciphertext_and_signature = self.encoded_text_entry.toPlainText().split('\n')
                    ciphertext = b64decode(ciphertext_and_signature[0].split(': ')[1])
                    signature = b64decode(ciphertext_and_signature[1].split(': ')[1])

                    decrypted_text = self.rsa_encryptor.verify_and_decrypt(ciphertext, signature)

                    self.plain_text_entry.setPlainText(decrypted_text)
                    self.encoded_text_entry.clear()
                else:
                    self.show_error_message(" Error ", "Please select an encryption algorithm")
        except ValueError as ve:
            self.show_error_message(" Error ", str(ve))

    def show_error_message(self, title, message):
        print(title, message)
        error_message = QMessageBox(self)
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(error_message.accept)
        error_message.setWindowTitle(title)
        error_message.setText(message)
        error_message.setIcon(QMessageBox.Critical)


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

        ok_button.setStyleSheet(button_style)
        error_message.addButton(ok_button, QMessageBox.AcceptRole)
        error_message.exec()

    class CustomLineEdit(QLineEdit):
        def __init__(self, parent=None, placeholderText=""):
            super().__init__(parent)
            self.theme = "classic"
            emitter.theme_signal.connect(self.changeTheme)
            self.setPlaceholderText(placeholderText)

        def changeTheme(self, theme):
            self.theme = theme

        def setEnabled(self, enabled):
            super().setEnabled(enabled)

            # Check if the parent widget is a QFrame
            parent_widget = self.parentWidget()
            if isinstance(parent_widget, QFrame):
                # Apply visual indication for disabled state
                if not enabled:
                    if self.theme == "classic":
                        parent_widget.setStyleSheet(
                            "QFrame { background-color: #3c5c6e; }")
                    elif self.theme == "light":
                        parent_widget.setStyleSheet(
                            "QFrame { background-color: #D6D6D6;color:737373;border: 1px solid #FFFFFF; }"
                            "QLabel {border:1px solid #D6D6D6 ; }")

                else:
                    parent_widget.setStyleSheet("")




if __name__ == "__main__":
    app = QApplication([])
    mainWindow = Txt_enc_Dec()
    mainWindow.show()
    sys.exit(app.exec())

