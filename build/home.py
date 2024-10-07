import sys
import os
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QFrame,
    QStackedWidget,
    QTextEdit,
    QPushButton

)
from PySide6.QtCore import Qt, QSize
from custom_button import CustomButton
from ui_shadow import create_drop_shadow
from PySide6.QtGui import QPixmap, QIcon
from themesignal import emitter


class HomePage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.theme = "classic"
        self.setup_ui()
        self.applyTheme()
        emitter.theme_signal.connect(self.changeTheme)

    def applyTheme(self):
        # Get the directory of the executable

        stylesheet_file = f"stylesheets/home_style_classic.qss"
        with open(stylesheet_file, "r") as f:
            stylesheet = f.read()
            self.setStyleSheet(stylesheet)

    def changeTheme(self, theme):
        self.hide()
        self.theme = theme
        stylesheet_file = f"stylesheets/home_style_{theme}.qss"
        with open(stylesheet_file, "r") as f:
            stylesheet = f.read()
            self.setStyleSheet(stylesheet)
        self.show()

    def setup_ui(self):

        print("settingupui")
        self.setWindowTitle("Home")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout_main = QVBoxLayout(central_widget)

        # navigation arrows
        self.left_arrow = QPushButton()
        self.left_arrow.setIcon(QIcon("resources/left_arrow.png"))
        self.left_arrow.setIconSize(QSize(40, 40))
        self.left_arrow.setFixedSize(50, 50)
        self.left_arrow.setCursor(Qt.PointingHandCursor)
        self.left_arrow.clicked.connect(lambda: self.show_previous_page())
        self.left_arrow.setEnabled(False)

        self.right_arrow = QPushButton()
        self.right_arrow.setIcon(QIcon("resources/right_arrow.png"))
        self.right_arrow.setIconSize(QSize(40, 40))
        self.right_arrow.setFixedSize(50, 50)
        self.right_arrow.setCursor(Qt.PointingHandCursor)
        self.right_arrow.clicked.connect(lambda: self.show_next_page())


        # stacked box 1
        self.stacked_box1 = QFrame()
        stacked_box1_layout = QHBoxLayout(self.stacked_box1)
        stacked_box1_layout.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("resources/logo.png") # logo designed by ** June Ketchum **
        logo_label = QLabel(self.stacked_box1)
        logo_label.setPixmap(pixmap)
        logo_label.setScaledContents(True)
        logo_label.setFixedSize(200, 200)

        para_layout = QVBoxLayout()
        description_label = QLabel("Welcome to Secure-Cipher")
        description_para = QLabel(
            "Secure-Cipher is a simple and easy to use application that provides a variety of encryption and decryption methods. It is designed to be user-friendly and secure. It provides a variety of encryption and decryption methods such as Vigenere Cipher, Text Encryption and Decryption, File Encryption and Decryption, Steganography and Password Manager. It also provides a settings page to customize the application according to user's preferences.")
        description_para.setWordWrap(True)


        para_layout.addWidget(description_label)
        para_layout.addWidget(description_para)

        stacked_box1_layout.addWidget(logo_label, stretch=1)
        stacked_box1_layout.addLayout(para_layout, stretch=1)

        # Create page 2
        page_frame2 = QFrame()
        page_layout2 = QVBoxLayout(page_frame2)
        page_layout2.setAlignment(Qt.AlignCenter)


        description_label2 = QLabel("Welcome to the tutorials page for Secure-Cipher!")
        description_label2.setAlignment(Qt.AlignCenter)

        description_para2 = QTextEdit()
        description_para2.setReadOnly(True)
        description_para2.setHtml('''
                <br>
               <b> Here, you'll find comprehensive guides on how to utilize every feature of our application. </b><br>
               <br> 
                Whether you're exploring encryption methods, decrypting files, or managing your passwords securely, <br>
                we've got you covered. <br>
                Whether you're a tech enthusiast or a cybersecurity novice, our guides will walk you through <br>
                the essentials of encryption and decryption. <br>
                <br>
                Each tutorial is designed to be clear and concise, guiding you through every step of the process. <br>
                Get ready to explore the world of encryption and decryption with <b><i>Secure-Cipher</i>, where security meets simplicity</b>.<br>
                <br>
                <b>Click</b> the arrow to continue and dive into the tutorials! >>
               '''
        )
        page_layout2.addWidget(description_label2)
        page_layout2.addWidget(description_para2)

        # create page 3
        page_frame3 = QFrame()
        page_layout3 = QVBoxLayout(page_frame3)
        page_layout3.setAlignment(Qt.AlignCenter)

        description_label3 = QLabel("Tutorial for Text Encryption/Decryption : ")
        description_para_text = ''' 
        1.  Select Encryption Algorithm :  
            - Choose one of the options: Vigenère Cipher, AES, RSA, or None.  
            - Click on the radio button next to the encryption algorithm you want to use.  
                                                 
        2.  Enter Key (if applicable) :  
            - If you selected Vigenère Cipher or AES, you'll need to enter a key.   
            - Type your key into the 'Key' input field provided.  
            - For RSA encryption, you won't need to enter a key here.  
                                                 
        3.  Generate Keys (if needed) :  
            - If you're using AES encryption, you can click the 'Generate Key(s)' button to generate a random key.  
            - For RSA encryption, you can also generate keys by clicking the 'Generate Key(s)' button.  
                                                 
        4.  Load RSA Keys (if applicable) :  
            - If you selected RSA encryption, you'll need to load RSA keys. 
            - Click on the 'Private Key' or 'Public Key' button to browse and select the corresponding key file.  
        
        5.  Enter Text :  
            - In the 'Plain Text' text area, type or paste the text you want to encrypt.  
            - Ensure that your text is entered correctly before proceeding.  
                                                 
        6.  Encrypt :  
            - After entering the text and setting up the encryption parameters, you can proceed with encryption.  
            - Click on the 'Encode' button to encrypt the entered text based on the selected algorithm and key.  
            - The encrypted text will appear in the 'Encrypted Text' text area.  
                                                 
        7.  Decrypt :  
            - If you want to decrypt previously encrypted text, ensure that you have the correct algorithm and key settings.  
            - Enter or paste the encrypted text into the 'Encrypted Text' text area.  
            - Click on the 'Decode' button to decrypt the encrypted text.  
            - The decrypted text will appear in the 'Plain Text' text area.  
                                                 
        8.  Reset : 
            - At any point, if you want to start over or clear all input fields, you can click the 'Reset'. 
            - This will clear the selected encryption algorithm, key input fields, and text areas, allowing you to start fresh.
        '''


        description_para3 = QTextEdit()
        description_para3.setReadOnly(True)
        description_para3.setPlainText(description_para_text)
        description_para3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        page_layout3.addWidget(description_label3)
        page_layout3.addWidget(description_para3)


        #create page 4
        page_frame4 = QFrame()
        page_layout4 = QVBoxLayout(page_frame4)
        page_layout4.setAlignment(Qt.AlignCenter)

        description_label4 = QLabel("Tutorial for File Encryption/Decryption : ")
        description_para_text = ''' 
        1.  Enter Key :
            - Enter the encryption key in the 'Key' input field provided. This key will be used for both encryption and 
              decryption.

        2.  Select File :
            - You can either click the 'Browse' button to select a file using the file dialog or drag and drop a file 
              into the designated drop area labeled "Drop File Here".
            - The path of the selected file will be displayed below the "Select File" label.

        3.  Generate Key :
            - If you prefer, you can generate a random encryption key by clicking the 'Generate Key' button. 
              The generated key will be displayed in the 'Key' input field.

        4.  Encrypt :
            - After selecting a file and entering the encryption key, you can proceed with file encryption by 
              clicking the 'Encrypt' button.
            - The selected file will be encrypted using the provided key, and a new encrypted file will be created with 
              the '.encrypted' extension in the same directory as the original file.

        5.  Decrypt :
            - To decrypt a previously encrypted file, ensure that you have the correct encryption key used for encryption.
            - Select the encrypted file by clicking the 'Browse' button or dragging and dropping it into the designated drop area.
            - Enter the encryption key used for encryption into the 'Key' input field.
            - Click the 'Decrypt' button to decrypt the file. The decrypted file will be saved in the 
              same directory as the encrypted file, removing the '.encrypted' extension.
        '''
        description_para4 = QTextEdit()
        description_para4.setReadOnly(True)
        description_para4.setPlainText(description_para_text)
        description_para4.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        page_layout4.addWidget(description_label4)
        page_layout4.addWidget(description_para4)

        #create page 5
        page_frame5 = QFrame()
        page_layout5 = QVBoxLayout(page_frame5)
        page_layout5.setAlignment(Qt.AlignCenter)

        description_label5 = QLabel("Tutorial for Steganography : ")
        description_para_text = ''' 
        1.  Select Image :
            - Click the 'Select Image' button to choose an image file (PNG, JPG, or BMP) from your system.
            - The selected image path will be displayed besides the button.

        2.  Data to Embed :
            - Enter the data you want to embed into the image in the 'Data to Embed' text box provided.
            - This data can be any text or information you wish to hide within the image.

        3.  Embed :
            - After selecting an image and entering the data, click the 'Embed' button to hide the data within the selected image.
            - The embedded image will be saved with the embedded data, and a 
              success message will be displayed with the path to the saved image.

        4.  Extract :
            - To extract hidden data from an image, first, select an image that contains embedded data.
            - Click the 'Extract' button to reveal and extract the hidden data from the selected image.
            - The extracted data will be displayed in the 'Extracted Data' text box.

        Note: LSB (Least Significant Bit) steganography is used to embed and extract data from images. 
        Ensure that the image format supports lossless compression to maintain data integrity.
        '''
        description_para5 = QTextEdit()
        description_para5.setReadOnly(True)
        description_para5.setPlainText(description_para_text)
        description_para5.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        page_layout5.addWidget(description_label5)
        page_layout5.addWidget(description_para5)

        #create page 6
        page_frame6 = QFrame()
        page_layout6 = QVBoxLayout(page_frame6)
        page_layout6.setAlignment(Qt.AlignCenter)

        description_label6 = QLabel("Tutorial for Password Manager : ")
        description_para_text = '''
        1. Authentication:
           - When you open the Password Manager application, you'll first see the authentication screen.
           - Enter your username and password in the respective input fields.
           - Click the 'Login' button to authenticate yourself and access your password vault.

        2. Adding a New Entry:
           - Once logged in, you'll be presented with your password vault.
           - To add a new entry, click on the 'Add New' button.
           - This will clear the input fields for website, username, and password.
           - Enter the website, username, and password for the new entry in the respective input fields.
           - You can also check your password's strength in real time using the password strength meter.
           - Click the eye icon next to the password input field to toggle between showing and hiding the password.
           - Click the 'Save' button to save the new entry to your vault.
        
        3. Viewing and Editing Entries:
           - To view or edit an existing entry, simply click on the entry in the website list.
           - This will populate the input fields with the details of the selected entry.
           - To edit them, click the 'Edit' button and now you can edit any of the fields as needed.
           - Click the eye icon next to the password input field to toggle between showing and hiding the password.
           - Click the 'Save' button to save your changes.
        
        4. Copying Passwords:
           - To copy a password to the clipboard, simply click on the copy icon in the password entry field.
           - This will automatically copy the password to your clipboard, ready for pasting.
        
        5. Deleting Entries:
           - To delete an entry, select the entry in the website list.
           - Click the 'Delete' button to delete the selected entry from your vault.
        
        6. Logging Out:
           - To log out of the Password Manager application, click the 'Logout' button.
           - This will return you to the authentication screen, where you'll need to log in again to access your vault.
        
        7. Encryption and Security:
           - The Password Manager securely encrypts your passwords to keep them safe.
           - All your credentials are stored locally and in a hashed format , safe from external threats.
           - You don't need to worry about your passwords being exposed or compromised.
        
        That's it! You're now ready to use the Password Manager to securely store and manage your passwords with added features like 
        password hiding/showing, password strength meter, and logout button.
        '''
        description_para6 = QTextEdit()
        description_para6.setReadOnly(True)
        description_para6.setPlainText(description_para_text)
        description_para6.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        page_layout6.addWidget(description_label6)
        page_layout6.addWidget(description_para6)




        outer_frame = QFrame(self)
        outer_frame_layout = QVBoxLayout(outer_frame)
        window_width = QApplication.primaryScreen().size().width()
        window_height = QApplication.primaryScreen().size().height()
        frame_Width = int(0.75 * window_width)
        frame_Height = int(0.65 * window_height)
        outer_frame.setFixedWidth(frame_Width)
        outer_frame.setFixedHeight(frame_Height)

        self.stacked_widget = QStackedWidget(outer_frame)
        self.stacked_widget.addWidget(self.stacked_box1)
        self.stacked_widget.addWidget(page_frame2)
        self.stacked_widget.addWidget(page_frame3)
        self.stacked_widget.addWidget(page_frame4)
        self.stacked_widget.addWidget(page_frame5)
        self.stacked_widget.addWidget(page_frame6)
        self.stacked_widget.setCurrentIndex(0)



        # setting object name for qss
        self.stacked_widget.setObjectName("stacked_widget")
        outer_frame.setObjectName("outer_frame")
        self.left_arrow.setObjectName("left_arrow")
        self.right_arrow.setObjectName("right_arrow")
        self.stacked_box1.setObjectName("stacked_box1")
        logo_label.setObjectName("logo_label")
        description_label.setObjectName("description_label")
        description_para.setObjectName("description_para")
        page_frame2.setObjectName("page_frame2")
        description_label2.setObjectName("description_label2")
        description_para2.setObjectName("description_para2")
        page_frame3.setObjectName("page_frame3")
        description_label3.setObjectName("description_label3")
        description_para3.setObjectName("description_para3")
        page_frame4.setObjectName("page_frame4")
        description_label4.setObjectName("description_label4")
        description_para4.setObjectName("description_para4")
        page_frame5.setObjectName("page_frame5")
        description_label5.setObjectName("description_label5")
        description_para5.setObjectName("description_para5")
        page_frame6.setObjectName("page_frame6")
        description_label6.setObjectName("description_label6")
        description_para6.setObjectName("description_para6")


        outer_frame_layout.addWidget(self.left_arrow, alignment=Qt.AlignLeft)
        outer_frame_layout.addWidget(self.stacked_widget)
        outer_frame_layout.addWidget(self.right_arrow, alignment=Qt.AlignRight)
        outer_frame_layout.setAlignment(Qt.AlignCenter)

        create_drop_shadow(outer_frame)

        layout_main.addWidget(outer_frame)
        layout_main.setAlignment(Qt.AlignCenter)

        central_widget.setLayout(layout_main)
        print("settingupui done")




    def show_previous_page(self):
        if self.stacked_widget.currentIndex() > 0:
            self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() - 1)
        # Disable previous page button if at the first page
        if self.stacked_widget.currentIndex() == 0:  # Assuming the first page is at index 0
            self.left_arrow.setEnabled(False)
        # Enable next page button
        self.right_arrow.setEnabled(True)

    def show_next_page(self):
        if self.stacked_widget.currentIndex()  < self.stacked_widget.count() - 1:
            self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex()  + 1)
        # Disable next page button if at the last page
        if self.stacked_widget.currentIndex()  == self.stacked_widget.count() - 1:  # Assuming the last page is at index count() - 1
            self.right_arrow.setEnabled(False)
        # Enable previous page button
        self.left_arrow.setEnabled(True)


if __name__ == "__main__":
    app = QApplication([])
    mainWindow = HomePage()
    mainWindow.show()
    mainWindow.showMaximized()
    sys.exit(app.exec())
