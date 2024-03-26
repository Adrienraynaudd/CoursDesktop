import sys
import time
import psutil
import wmi
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QSlider
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QIcon

class SystemMonitor(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.cpu_label = QLabel("CPU Usage: ")
        self.memory_label = QLabel("Memory Usage: ")
        self.network_label = QLabel("Network Stats:")
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.memory_label)
        layout.addWidget(self.network_label)

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
        self.wmi = wmi.WMI(namespace='wmi')
        self.timer.start(1000)

        self.prev_net_io_counters = psutil.net_io_counters()
        self.prev_time = psutil.boot_time()
        self.last_network_update = 0
        self.network_update_interval = 0.5

    def update_system_info(self):
        current_time = time.time()
        if current_time - self.last_network_update >= self.network_update_interval:
            cpu_percent = psutil.cpu_percent()
            memory_percent = psutil.virtual_memory().percent
            self.cpu_label.setText("CPU Usage: {}%".format(cpu_percent))
            self.memory_label.setText("Memory Usage: {}%".format(memory_percent))

            net_io_counters = psutil.net_io_counters()
            time_elapsed = current_time - self.prev_time
            self.prev_time = current_time

            if time_elapsed > 0 and net_io_counters != self.prev_net_io_counters:
                download_speed = (net_io_counters.bytes_recv - self.prev_net_io_counters.bytes_recv) / time_elapsed
                upload_speed = (net_io_counters.bytes_sent - self.prev_net_io_counters.bytes_sent) / time_elapsed

                download_speed_str = self.format_speed(download_speed)
                upload_speed_str = self.format_speed(upload_speed)

                network_stats = "Download: {}\nUpload: {}\n".format(download_speed_str, upload_speed_str)

                self.network_label.setText("Network Stats:\n{}".format(network_stats))

                self.prev_net_io_counters = net_io_counters
                self.last_network_update = current_time
            else:
                self.network_label.setText("Network Stats:\nUnable to calculate speed due to short time interval or no network activity.")

    def format_speed(self, speed):
        units = ['B/s', 'KB/s', 'MB/s', 'GB/s']
        unit_index = 0
        while speed > 1024 and unit_index < len(units) - 1:
            speed /= 1024
            unit_index += 1
        return "{:.2f} {}".format(speed, units[unit_index])

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
        self.setWindowIcon(QIcon("icon.png"))
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
    sys.exit(app.exec())
