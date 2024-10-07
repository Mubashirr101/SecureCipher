from PySide6.QtCore import Signal, QTimer
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QPushButton, QGraphicsDropShadowEffect, QFrame
from shiboken6 import isValid
from themesignal import emitter
class CustomShadowEffect(QGraphicsDropShadowEffect):
    def __init__(self, parent=None):
        super().__init__(parent)


    def setProperties(self, blur_radius, color, offset):
        self.setBlurRadius(blur_radius)
        self.setColor(color)

        if len(offset) == 2:
            self.setOffset(offset[0], offset[1])
        elif len(offset) == 1:
            self.setOffset(offset[0])


class CustomButton(QPushButton):
    # Signal for button hover
    hovered = Signal()

    def __init__(self, text, parent=None, min_size=None, max_size=None):
        super().__init__(text, parent)

        emitter.theme_signal.connect(self.set_theme)
        self.theme = "classic"


        self.is_clicked = False
        # Set minimum and maximum sizes if provided, or use default values
        self.setMinimumSize(min_size[0], min_size[1]) if min_size else self.setMinimumSize(130, 40)
        self.setMaximumSize(max_size[0], max_size[1]) if max_size else self.setMaximumSize(130, 40)

        print(f"Theme in custom button: {self.theme}")

        # Create a custom shadow effect for the button
        self.shadow = CustomShadowEffect(self)
        self.setGraphicsEffect(self.shadow)
        self.shadow.setEnabled(False)  # Initially disabled
        # Connect signals for click and hover
        self.clicked.connect(self.on_button_clicked)
        self.default_size = self.size()

    def set_theme(self, theme):
        self.theme = theme


    def enterEvent(self, event):
        super().enterEvent(event)

        if not self.shadow.isEnabled():
            if self.theme == "classic":
                print("theme in hover",self.theme)
                self.shadow.setProperties(15, QColor(0, 0, 0, 150), (5, 5))
            elif self.theme == "light":
                print("theme in hover ",self.theme)
                self.shadow.setProperties(50, QColor(0,191,255), (5, 5))
            self.shadow.setEnabled(True)
            self.hovered.emit()

        # Calculate desired scaled size with padding
        # Enlarge button size directly
        self.setFixedWidth(self.size().width() )  # Adjust scale factor as needed
        self.setFixedHeight(self.size().height() * 1.03)

    def leaveEvent(self, event):
        super().leaveEvent(event)

        if self.shadow and not isValid(self.shadow):
            return
        if self.shadow and self.shadow.isEnabled():
            self.shadow.setEnabled(False)
            self.hovered.emit()

        self.setFixedWidth(self.default_size.width())
        self.setFixedHeight(self.default_size.height())

    def on_button_clicked(self):
        # Check if the on_button_clicked method should be executed or not
        if self.is_clicked:
            return

        glow_effect = CustomShadowEffect(self)
        if self.theme == "classic":
            glow_effect.setProperties(20, QColor(0, 0, 0, 150), (0, 0))
        if self.theme == "light":
            glow_effect.setProperties(50, QColor(0,191,255), (0, 0))
        self.setGraphicsEffect(glow_effect)

        # Create a new shadow effect after the delay
        QTimer.singleShot(200, self.restore_shadow_effect)

        # Set the flag to True to prevent the on_button_clicked method from being executed again
        self.is_clicked = True
        # Set the flag  False, to allow the on_button_clicked method to be executed again
        self.is_clicked = False

    def restore_shadow_effect(self):
        self.shadow = CustomShadowEffect(self)
        if self.theme == "classic":
            self.shadow.setProperties(15, QColor(0, 0, 0, 150), (5, 5))
        if self.theme == "light":
            self.shadow.setProperties(50, QColor(0,191,255), (5, 5))
        self.setGraphicsEffect(self.shadow)


class CustomHoverButton(QPushButton):
    # Signal for button hover
    hovered = Signal()
    def __init__(self, text, parent=None, min_size=None, max_size=None):
        super().__init__(text, parent)

        emitter.theme_signal.connect(self.set_theme)
        self.theme = "classic"

        self.is_clicked = False
        # Set minimum and maximum sizes if provided, or use default values
        self.setMinimumSize(min_size[0], min_size[1]) if min_size else self.setMinimumSize(130, 40)
        self.setMaximumSize(max_size[0], max_size[1]) if max_size else self.setMaximumSize(130, 40)

        # Create a custom shadow effect for the button
        self.shadow = CustomShadowEffect(self)
        self.setGraphicsEffect(self.shadow)
        self.shadow.setEnabled(False)  # Initially disabled
        # Connect signals for click and hover
        self.default_size = self.size()

    def set_theme(self, theme):
        self.theme = theme



    def enterEvent(self, event):
        super().enterEvent(event)

        if not self.shadow.isEnabled():
            if self.theme == "classic":
                self.shadow.setProperties(15, QColor(0, 0, 0, 100), (5, 5))
            elif self.theme == "light":
                self.shadow.setProperties(50, QColor(0,191,255), (4, 4))
            self.shadow.setEnabled(True)
            self.hovered.emit()

        # Calculate desired scaled size with padding
        # Enlarge button size directly
        self.setFixedWidth(self.size().width() )  # Adjust scale factor as needed
        self.setFixedHeight(self.size().height() * 1.03)

    def leaveEvent(self, event):
        super().leaveEvent(event)

        if self.shadow and not isValid(self.shadow):
            return
        if self.shadow and self.shadow.isEnabled():
            self.shadow.setEnabled(False)
            self.hovered.emit()

        self.setFixedWidth(self.default_size.width())
        self.setFixedHeight(self.default_size.height())

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
                        "QFrame { background-color: #D6D6D6;color:737373;border: 1px solid #D6D6D6; }"
                        "QLabel { border: 1px solid #D6D6D6;")
            else:
                parent_widget.setStyleSheet("")
