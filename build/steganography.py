import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QFileDialog,QTextEdit, QMessageBox, QVBoxLayout,QHBoxLayout, QFrame
from PIL import Image
from stegano import lsb
from custom_button import CustomButton, CustomHoverButton
from PySide6.QtCore import QTimer,Qt
from ui_shadow import create_drop_shadow
from themesignal import emitter
class SteganographyPage(QMainWindow):
    def __init__(self):
        super().__init__()
        print("SteganographyPage init")

        self.theme = "classic"
        self.initUI()
        self.applyTheme()
        emitter.theme_signal.connect(self.changeTheme)

    def applyTheme(self):
        # print(f"Applying {theme} theme")
        stylesheet_file = "stylesheets/steganography_style_classic.qss"  # Use theme-specific stylesheets
        with open(stylesheet_file, "r") as f:
            stylesheet = f.read()
            self.setStyleSheet(stylesheet)

    def changeTheme(self, theme):
        self.hide()
        self.theme = theme
        print(self.theme)
        print(f"received signal: {theme}")
        stylesheet_file = f"stylesheets/steganography_style_{theme}.qss"
        with open(stylesheet_file, "r") as f:
            stylesheet = f.read()
            self.setStyleSheet(stylesheet)
        self.show()

    def initUI(self):
        self.setWindowTitle("SecureCipher - Steganography")
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # self.setGeometry(100, 100, 600, 400)
        # Create layout
        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()
        layout4 = QHBoxLayout()
        layout5 = QHBoxLayout()



        self.image_label = QLabel("")
        self.select_image_button = CustomHoverButton("Select Image",min_size=(85,25),max_size=(85,25))
        self.select_image_button.setFixedWidth(85)
        self.select_image_button.setFixedHeight(25)
        # After creating self.image_label and self.select_image_button

        # After creating self.image_label and self.select_image_button

        self.embed_data_button = CustomButton(" Embed ", min_size=(252, 60), max_size=(252, 60))
        self.embed_data_button.setFixedHeight(60)

        self.extract_data_button = CustomButton(" Extract ", min_size=(252, 60), max_size=(252, 60))
        self.extract_data_button.setFixedHeight(60)

        frame_input = QFrame()
        frame_input.setFixedWidth(574)
        self.data_input_label = QLabel("Data to Embed:", frame_input)
        self.data_input_textbox = QTextEdit(frame_input)
        layout_input = QVBoxLayout(frame_input)
        layout_input.addWidget(self.data_input_label)
        layout_input.addWidget(self.data_input_textbox)
        frame_input.setLayout(layout_input)
        #frame_input will be added in layout2 below with other layouts

        frame_output = QFrame()
        frame_output.setFixedWidth(574)
        self.output_label = QLabel("Extracted Data: ",frame_output)
        self.output_textbox = QTextEdit(frame_output)
        self.output_textbox.setReadOnly(True)
        layout_output=QVBoxLayout(frame_output)
        layout_output.addWidget(self.output_label)
        layout_output.addWidget(self.output_textbox)
        frame_output.setLayout(layout_output)
        #frame_output will be added in layout3 below with other layouts



        # Connect buttons to functions
        self.select_image_button.clicked.connect(self.select_image)
        self.embed_data_button.clicked.connect(self.embed_data)
        self.extract_data_button.clicked.connect(self.extract_data)


        # Create a QGroupBox

        # Create a QFrame
        frame = QFrame()
        outer_frame = QFrame()
        frame.setFrameShape(QFrame.Box)
        frame.setFixedHeight(43)
        frame.setFixedWidth(554)
        # Set the frame shape to StyledPanel for a sunken border
        # Set layout4 as the layout for the QFormLayout
        layout4 = QHBoxLayout()
        # Set the layout for the frame
        layout4.addWidget(self.image_label)
        layout4.addWidget(self.select_image_button)
        frame.setLayout(layout4)
        frame.setParent(outer_frame)
        framelayout = QVBoxLayout()
        framelayout.addWidget(frame)
        outer_frame.setLayout(framelayout)
        layout3.addWidget(outer_frame)

        # Add the frame to layout2
        layout2.addWidget(frame_input)
        layout2.addSpacing(31)
        layout5.addWidget(self.embed_data_button)
        layout5.addSpacing(65)
        layout5.addWidget(self.extract_data_button)
        layout5.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout3.addLayout(layout5)
        layout3.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout2.addWidget(frame_output)
        layout2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout1.addLayout(layout3)
        layout1.addLayout(layout2)

        layout5.setContentsMargins(30,0,30,0)
        layout3.setContentsMargins(70,30,70,10)
        layout2.setContentsMargins(70,25,70,60)


        #drop shadow
        create_drop_shadow(outer_frame)
        create_drop_shadow(frame_input)
        create_drop_shadow(frame_output)

        #setting object name for qss
        self.image_label.setObjectName("image_label")
        self.select_image_button.setObjectName("select_image_button")
        self.embed_data_button.setObjectName("embed_data_button")
        self.extract_data_button.setObjectName("extract_data_button")
        frame_input.setObjectName("frame_input")
        frame_output.setObjectName("frame_output")
        frame.setObjectName("frame")
        outer_frame.setObjectName("outer_frame")
        self.data_input_label.setObjectName("data_input_label")
        self.data_input_textbox.setObjectName("data_input_textbox")
        self.output_label.setObjectName("output_label")
        self.output_textbox.setObjectName("output_textbox")



        central_widget.setLayout(layout1)
        # self.showMaximized()

    def select_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        image_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Image Files (*.png *.jpg *.bmp)", options=options)
        if image_path:
            self.image_label.setText("Image: " + image_path)
            self.image_path = image_path

    def embed_data(self):
        # Get the data to embed from the text box
        data_to_embed = self.data_input_textbox.toPlainText()

        # Check if an image is selected and data is entered
        if not hasattr(self, 'image_path') or not data_to_embed:
            self.show_message_box(
                "Embed Data", "Please select an image and enter data to embed.")
            return

        # Open the image using Pillow
        image = Image.open(self.image_path)
        # Embed the data into the image using LSB steganography
        embedded_image = lsb.hide(image, data_to_embed)

        # Save the embedded image
        embedded_image_path, _ = QFileDialog.getSaveFileName(
            self, "Save Embedded Image", "", "Image Files (*.png *.jpg *.bmp)")
        if embedded_image_path:
            embedded_image.save(embedded_image_path)
            # Display an information message with the saved image path
            info_message = f"Data embedded successfully!\nEmbedded image saved at:\n{embedded_image_path}"
            self.show_message_box("Embed Data", info_message)

    def extract_data(self):
        # Check if an image is selected
        if not hasattr(self, 'image_path'):
            self.show_message_box( "Extract Data", "Please select an image to extract data.")
            return

        # Open the image using Pillow
        image = Image.open(self.image_path)

        # Extract the data from the image using LSB steganography
        try:
            extracted_data = lsb.reveal(image)
            # self.output_textbox.setPlainText(
            #     "Extracted Data:\n" + extracted_data)

            self.output_textbox.setPlainText(extracted_data)
            self.show_message_box("Extract Data", "Data extracted successfully!")

        except ValueError as ve :
            self.show_message_box("Extract Data",
                                str(ve))
        except IndexError as e:
            self.show_message_box("Extract Data", str(e))

    def show_message_box(self, title, content):
        QTimer.singleShot(0, lambda: self._show_message_box(title, content))

    def _show_message_box(self, title, content):
        message_box = QMessageBox()
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
        message_box.setIcon(QMessageBox.Information)
        message_box.setWindowTitle(title)
        message_box.setText(content)

        ok_button = message_box.addButton("OK", QMessageBox.AcceptRole)
        ok_button.setStyleSheet(button_style)

        message_box.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SteganographyPage()
    window.show()
    sys.exit(app.exec())
