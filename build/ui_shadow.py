from PySide6.QtWidgets import QGraphicsDropShadowEffect
from PySide6.QtGui import QColor

def create_drop_shadow(frame):
    shadow1 = QGraphicsDropShadowEffect(frame)
    shadow1.setBlurRadius(3)
    shadow1.setOffset(5, 5)
    shadow1.setColor(QColor(0,0,0,75))  # Shadow color
    frame.setGraphicsEffect(shadow1)