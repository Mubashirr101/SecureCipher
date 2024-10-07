from PySide6.QtCore import QObject, Signal

class ThemeSignal(QObject):
    theme_signal = Signal(str)
emitter = ThemeSignal()
def trigger_signal(theme):
    print(f"Emitting signal with message:: {theme}")
    emitter.theme_signal.emit(theme)
