import sys
import psutil
import wmi
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QSlider
from PySide6.QtCore import QTimer, Qt

class SystemMonitor(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.cpu_label = QLabel("CPU Usage: ")
        self.memory_label = QLabel("Memory Usage: ")
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.memory_label)
        
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setMinimum(0)
        self.brightness_slider.setMaximum(100)
        self.brightness_slider.setValue(100) 
        self.brightness_slider.setTickInterval(10)
        self.brightness_slider.setTickPosition(QSlider.TicksBelow)
        self.brightness_slider.valueChanged.connect(self.update_brightness)
        layout.addWidget(QLabel("Screen Brightness:"))
        layout.addWidget(self.brightness_slider)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_system_info)
        self.timer.start(1000) 

        self.wmi = wmi.WMI(namespace='wmi')

    def update_system_info(self):
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        self.cpu_label.setText("CPU Usage: {}%".format(cpu_percent))
        self.memory_label.setText("Memory Usage: {}%".format(memory_percent))

    def update_brightness(self):
        brightness_value = self.brightness_slider.value()
        self.set_brightness(brightness_value)

    def set_brightness(self, brightness):
        brightness = min(max(brightness, 0), 100)

        for methods in self.wmi.WmiMonitorBrightnessMethods():
            methods.WmiSetBrightness(brightness, 0)





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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
