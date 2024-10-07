import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QFrame
from PySide6.QtCore import Qt
from home import HomePage as Page1
from text_enc_dec import Txt_enc_Dec as Page2
from file_enc_dec import FileEncryptionWindow as Page3
from steganography import SteganographyPage as Page4
from password_manager import PasswordManager as Page5
from settings import SettingsPage as Page6
from themesignal import emitter
from PySide6.QtGui import QIcon

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.theme = "classic"
        self.setup_ui()
        self.applyTheme()
        emitter.theme_signal.connect(self.changeTheme)

    def applyTheme(self):
        stylesheet_file = "stylesheets/master_page1_style_classic.qss"  # Use theme-specific stylesheets
        with open(stylesheet_file, "r") as f:
            stylesheet = f.read()
            self.setStyleSheet(stylesheet)
    def changeTheme(self, theme):
        self.hide()
        self.theme = theme
        print(self.theme)
        print(f"received signal: {theme}")
        stylesheet_file = f"stylesheets/master_page1_style_{theme}.qss"
        with open(stylesheet_file, "r") as f:
            stylesheet = f.read()
            self.setStyleSheet(stylesheet)
        self.show()

    def setup_ui(self):
        self.setWindowTitle("SecureCipher")
        window_icon = QIcon("resources/logo_small.png")
        self.setWindowIcon(window_icon)
        self.stack_widget = QStackedWidget(self)

        # Create instances of each page
        page1 = Page1()
        page2 = Page2()
        page3 = Page3()
        page4 = Page4()
        page5 = Page5()
        page6 = Page6()

        # Add pages to the stack widget
        self.stack_widget.addWidget(page1)
        self.stack_widget.addWidget(page2)
        self.stack_widget.addWidget(page3)
        self.stack_widget.addWidget(page4)
        self.stack_widget.addWidget(page5)
        self.stack_widget.addWidget(page6)

        # Create buttons for each page

        self.button_page1 = QPushButton("Home", self)
        self.button_page1.setMinimumHeight(40)
        self.button_page1.setCheckable(True)
        self.button_page1.setChecked(True)
        self.button_page1.clicked.connect(lambda: self.button_clicked(self.button_page1,0))
        self.button_page1.setCursor(Qt.CursorShape.PointingHandCursor)

        self.button_page2 = QPushButton("Text Encryption/Decryption", self)
        self.button_page2.setMinimumHeight(40)
        self.button_page2.setCheckable(True)
        self.button_page2.clicked.connect(lambda: self.button_clicked(self.button_page2,1))
        self.button_page2.setCursor(Qt.CursorShape.PointingHandCursor)

        self.button_page3 = QPushButton("File Encryption/Decryption", self)
        self.button_page3.setMinimumHeight(40)
        self.button_page3.setCheckable(True)
        self.button_page3.clicked.connect(lambda: self.button_clicked(self.button_page3,2))
        self.button_page3.setCursor(Qt.CursorShape.PointingHandCursor)

        self.button_page4 = QPushButton("Steganography", self)
        self.button_page4.setMinimumHeight(40)
        self.button_page4.setCheckable(True)
        self.button_page4.clicked.connect(lambda: self.button_clicked(self.button_page4,3))
        self.button_page4.setCursor(Qt.CursorShape.PointingHandCursor)

        self.button_page5 = QPushButton("Password Manager", self)
        self.button_page5.setMinimumHeight(40)
        self.button_page5.setCheckable(True)
        self.button_page5.clicked.connect(lambda: self.button_clicked(self.button_page5,4))
        self.button_page5.setCursor(Qt.CursorShape.PointingHandCursor)

        self.button_page6 = QPushButton("Settings", self)
        self.button_page6.setMinimumHeight(40)
        self.button_page6.setCheckable(True)
        self.button_page6.clicked.connect(lambda: self.button_clicked(self.button_page6,5))
        self.button_page6.setCursor(Qt.CursorShape.PointingHandCursor)

        # Create a frame for the buttons layout
        button_frame = QFrame()
        button_frame.setFixedHeight(50)
        screen_width = QApplication.primaryScreen().geometry().width()
        frame_width = int(0.90 * screen_width)
        button_frame.setFixedWidth(frame_width)
        button_frame.setContentsMargins(10, 0, 10, 0)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout(button_frame)
        button_layout.addWidget(self.button_page1)
        button_layout.addWidget(self.button_page2)
        button_layout.addWidget(self.button_page3)
        button_layout.addWidget(self.button_page4)
        button_layout.addWidget(self.button_page5)
        button_layout.addWidget(self.button_page6)
        button_layout.setSpacing(0)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        button_layout.setContentsMargins(20, 0, 20, 0)

        # Create a vertical layout for the main window
        main_layout = QVBoxLayout(self)
        main_layout.addSpacing(5)
        main_layout.addWidget(button_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addSpacing(5)
        main_layout.addWidget(self.stack_widget)

        # Setting object name for stylesheet
        button_frame.setObjectName("button_frame")
        self.button_page1.setObjectName("button_page1")
        self.button_page2.setObjectName("button_page2")
        self.button_page3.setObjectName("button_page3")
        self.button_page4.setObjectName("button_page4")
        self.button_page5.setObjectName("button_page5")
        self.button_page6.setObjectName("button_page6")

        # Show the initial page
        self.show_page(0)
        screen = QApplication.primaryScreen()
        screen_size = screen.availableSize()
        self.setGeometry(0, 0, screen_size.width(), screen_size.height())
        self.showMaximized()

        # Attribute to keep track of last clicked button
        self.last_clicked_button = None

    def show_page(self, index):
        self.stack_widget.setCurrentIndex(index)

    def button_clicked(self, button, index=None):
        if self.button_page1 != button and self.button_page1.isChecked():
            self.button_page1.setChecked(False)
        if self.last_clicked_button and self.last_clicked_button != button:
            self.last_clicked_button.setChecked(False)  # Uncheck the last clicked button
        self.last_clicked_button = button
        self.stack_widget.setCurrentIndex(index)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.showMaximized()
    sys.exit(app.exec())
