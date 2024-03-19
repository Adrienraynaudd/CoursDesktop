import sys
import psutil
import ctypes
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import QTimer

class SystemMonitor(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.cpu_label = QLabel("CPU Usage: ")
        self.memory_label = QLabel("Memory Usage: ")
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.memory_label)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_system_info)
        self.timer.start(1000)

    def update_system_info(self):
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        self.cpu_label.setText("CPU Usage: {}%".format(cpu_percent))
        self.memory_label.setText("Memory Usage: {}%".format(memory_percent))

class BrightnessControl:
    @staticmethod
    def set_brightness(level):
        user32 = ctypes.windll.LoadLibrary("user32.dll")
        SetDeviceGammaRamp = user32.SetDeviceGammaRamp
        SetDeviceGammaRamp.restype = ctypes.c_bool
        SetDeviceGammaRamp.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_short)]

        brightness = int(level * 255 / 100)
        ramp = (ctypes.c_short * 256 * 3)()

        for i in range(256):
            ramp[i] = ramp[i + 256] = ramp[i + 512] = ctypes.c_short(brightness)

        return SetDeviceGammaRamp(None, ctypes.byref(ramp))

class BrightnessControlButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("Adjust Brightness", parent)
        self.clicked.connect(self.adjust_brightness)

    def adjust_brightness(self):
        BrightnessControl.set_brightness(50)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("System Monitor")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        system_monitor = SystemMonitor()
        layout.addWidget(system_monitor)

        brightness_button = BrightnessControlButton()
        layout.addWidget(brightness_button)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
