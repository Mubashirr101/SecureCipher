import sys
from PySide6.QtWidgets import QApplication, QMainWindow,QVBoxLayout, QGroupBox,QHBoxLayout, QLabel, QTextEdit
from themesignal import trigger_signal,emitter
from custom_button import CustomButton
from PySide6.QtCore import Qt
import webbrowser




class SettingsPage(QMainWindow):
    # Define a signal to emit the selected theme preference

    def __init__(self):
        super().__init__()
        print("SettingsPage init")
        self.theme = "classic"
        emitter.theme_signal.connect(self.changeTheme)
        self.initUI()
        self.applyTheme()


    def applyTheme(self):
        # print(f"Applying {theme} theme")
        stylesheet_file = "stylesheets/settings_style_classic.qss"  # Use theme-specific stylesheets
        with open(stylesheet_file, "r") as f:
            stylesheet = f.read()
            self.setStyleSheet(stylesheet)
    def changeTheme(self, theme):
        self.hide()
        self.theme = theme
        print(self.theme)
        print(f"received signal: {theme}")
        stylesheet_file = f"stylesheets/settings_style_{theme}.qss"
        with open(stylesheet_file, "r") as f:
            stylesheet = f.read()
            self.setStyleSheet(stylesheet)
        self.show()

    def initUI(self ):
        self.setWindowTitle("SecureCipher")
        # self.setGeometry(100, 100, 400, 300)
        # self.setStyleSheet("Background-color:#ECB365;")

        central_widget = QGroupBox()
        layout = QVBoxLayout()

        layout_1_1 = QHBoxLayout()
        # Theme Preferences
        theme_group = QGroupBox("")
        vertical_layout = QVBoxLayout()
        theme_label = QLabel("Choose a theme: ")
        # theme_group.setStyleSheet("Background-color:#04293A; border-radius:9; border:1 solid #0000; color:white;")
        theme_btn_box = QHBoxLayout()
        # Create buttons for each theme
        b1 = CustomButton("Classic",min_size=(100, 40),max_size=(100,40))

        b1.clicked.connect(lambda: trigger_signal("classic"))
        theme_btn_box.addWidget(b1)
        b2 = CustomButton("Light",min_size=(100,40),max_size=(100,40))

        b2.clicked.connect(lambda: trigger_signal("light"))
        theme_btn_box.addWidget(b2)
        vertical_layout.addWidget(theme_label)
        vertical_layout.addLayout(theme_btn_box)
        # b1.setStyleSheet(" background-color: #064663; color:white;border-radius:9; border:1 solid #0000;")
        # b2.setStyleSheet(" background-color: #064663 ; color:white;border-radius:9; border:1 solid #0000;")

        # Contact the dev team
        contact_group = QGroupBox("Contact the dev team")
        contact_group.setStyleSheet(
            "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top ; padding: 15px;}")
        contact_btn_box = QHBoxLayout()
        twitter = CustomButton("Twitter",min_size=(100,40),max_size=(100,40))
        twitter.clicked.connect(lambda: webbrowser.open("https://twitter.com/skmubashirrr"))
        email = CustomButton("Mail", min_size=(100,40),max_size=(100,40))
        email.clicked.connect(lambda: webbrowser.open("mailto:?to=mubashirshaikh1666@gmail.com&subject=Feedback%20for%20SecureCipher&body="))
        contact_btn_box.addWidget(twitter)
        contact_btn_box.addWidget(email)
        contact_group_section_layout = QVBoxLayout()
        contact_label = QLabel("Your feedback is invaluable! Reach out to us directly through our Twitter account or mail us.")
        # contact_label_heigth = int(0.2 * contact_group.height())
        # contact_label_width = int(0.4 * contact_group.width())
        contact_label.setWordWrap(True)
        contact_group_section_layout.addWidget(contact_label)
        contact_group_section_layout.addLayout(contact_btn_box)
        contact_group.setLayout(contact_group_section_layout)

        # About Section
        about_group = QGroupBox()
        about_group_section_layout = QVBoxLayout()
        about_label = QLabel("About SecureCipher :")
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setHtml(
        '''
        Hey there! 👋 Thanks for checking out Secure Cipher! I'm <b>Mubashir Shaikh</b> ,the sole developer behind this project. <br>
        As a cybersecurity enthusiast, I wanted to create a tool that prioritizes user privacy and security.  <br>
        With Secure Cipher, you can encrypt and decrypt text/files, hide messages using steganography, and manage your passwords securely. <br>
        <br>
        Additionally, one of my primary goals in developing Secure Cipher was to make powerful encryption, steganography techniques and an in-built password manager accessible to a wider audience.
        While many similar tools are command-line-based and predominantly designed for Linux users, I recognized the need for a user-friendly GUI application tailored to Windows users who may not be as comfortable with technical interfaces.<br><br>
        With Secure Cipher, I aim to bridge the gap between robust security features and user-friendly design, ensuring that even less tech-savvy individuals can confidently protect their sensitive information. <br>
        <br>
        Happy encrypting! 🔒 <br>
       '''
        )
        about_group_section_layout.addWidget(about_label)
        about_group_section_layout.addWidget(about_text)
        about_group.setLayout(about_group_section_layout)
        about_group_section_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)






        #sizing and positioning
        window_width = QApplication.primaryScreen().size().width()
        window_height = QApplication.primaryScreen().size().height()
        frame_Width = int(0.4 * window_width)
        frame_Height = int(0.35 * window_height)
        theme_group.setFixedSize(frame_Width, frame_Height)
        contact_group.setFixedSize(frame_Width, frame_Height)
        about_grp_width = int(0.8 * window_width)
        about_group.setFixedSize(about_grp_width, frame_Height)

        contact_label.setFixedSize(int(0.7 * contact_group.width()), int(0.5 * contact_group.height()))
        contact_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        contact_group_section_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        theme_label.setFixedSize(int(0.7 * theme_group.width()), int(0.5 * theme_group.height()))
        theme_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        theme_btn_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)










        #setting objectnames for the stylesheet
        theme_group.setObjectName("theme_group")
        b1.setObjectName("b1")
        b2.setObjectName("b2")
        central_widget.setObjectName("central_widget")
        contact_group.setObjectName("contact_group")
        twitter.setObjectName("twitter")
        email.setObjectName("email")
        contact_label.setObjectName("contact_label")
        about_group.setObjectName("about_group")
        about_label.setObjectName("about_label")
        about_text.setObjectName("about_text")
        theme_label.setObjectName("theme_label")





        theme_group.setLayout(vertical_layout)
        layout_1_1.addWidget(theme_group)
        layout_1_1.addWidget(contact_group)
        layout.addLayout(layout_1_1)
        layout.addWidget(about_group)
        layout.setAlignment(Qt.AlignCenter)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    settings_page = SettingsPage()
    settings_page.show()
    sys.exit(app.exec())
