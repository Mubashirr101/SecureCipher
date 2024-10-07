import sys
from PySide6.QtWidgets import QApplication, QPushButton, QFileDialog, QMessageBox
from Crypto.PublicKey import RSA
from themesignal import emitter

class RSAKeyGenerator():
    def __init__(self):
        super().__init__()
        self.theme = "classic"
        emitter.theme_signal.connect(self.changeTheme)




    def changeTheme(self, theme):
        self.theme = theme

    def generate_keys(self):

        self.msgbox = QMessageBox()
        self.msgbox.setStyleSheet("background-color: #064663; color: #FFFFFF;border-radius:6px;")
        if self.theme == "light":
            self.msgbox.setStyleSheet("background-color: #FFFFFF; color: #000000;border-radius:6px;")
        select_btn = QPushButton("Select")
        select_btn.clicked.connect(self.msgbox.accept)
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
        if self.theme == "light":
            button_style = ("QPushButton {"
                            "   color: #000000;"
                            "   background-color: #FFFFFF;"  # Change this color as needed
                            "   border: 1px solid #000000;"
                            "   padding: 5px;"
                            "   min-width: 70px;"
                            "   min-height: 25px;"
                            "   margin-right: 5px;"
                            "}"
                            "QPushButton:hover {"
                            "   background-color: #000000;"
                            "   color: #FFFFFF;"  # Change this color as needed
                            "}")
        self.msgbox.setWindowTitle("RSA Key Generator")
        self.msgbox.setText("RSA keys generated successfully and saved.")
        select_btn.setStyleSheet(button_style)
        self.msgbox.addButton(select_btn, QMessageBox.AcceptRole)

        directory = QFileDialog.getExistingDirectory(self, "Select Directory to Save Keys")
        if directory:
            key = RSA.generate(2048)
            private_key = key.export_key()
            public_key = key.publickey().export_key()

            with open(f"{directory}/private_key.pem", "wb") as private_key_file:
                private_key_file.write(private_key)

            with open(f"{directory}/public_key.pem", "wb") as public_key_file:
                public_key_file.write(public_key)

            self.msgbox.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RSAKeyGenerator()
    window.show()
    sys.exit(app.exec())
