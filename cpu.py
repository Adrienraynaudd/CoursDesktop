import os
import sys
import time
import psutil
import wmi
import subprocess
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QSlider, QCheckBox, QPushButton, QListWidget, QTabWidget, QTreeWidgetItem, QTreeWidget
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QIcon
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Widget pour afficher le graphique d'utilisation du CPU
class CPUGraph(QWidget):
    def __init__(self):
        super().__init__()
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_graph(self, cpu_percent):
        self.ax.clear()
        self.ax.plot(cpu_percent)
        self.ax.set_title('CPU Usage (%)')
        self.canvas.draw()

# Widget pour afficher le graphique d'utilisation de la mémoire
class MemoryGraph(QWidget):
    def __init__(self):
        super().__init__()
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_graph(self, memory_percent):
        self.ax.clear()
        self.ax.plot(memory_percent)
        self.ax.set_title('Memory Usage (%)')
        self.canvas.draw()

# Widget principal pour surveiller le système
class SystemMonitor(QWidget):
    def __init__(self, wmi_instance):
        super().__init__()
        layout = QVBoxLayout()

        self.cpu_label = QLabel("CPU Usage: ")
        self.memory_label = QLabel("Memory Usage: ")
        self.network_label = QLabel("Network Stats:")
        self.battery_label = QLabel("Battery: ")

        self.wmi = wmi_instance
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setMinimum(0)
        self.brightness_slider.setMaximum(100)
        self.brightness_slider.setValue(100)
        self.brightness_slider.setTickInterval(10)
        self.brightness_slider.setTickPosition(QSlider.TicksBelow)
        self.brightness_slider.valueChanged.connect(self.update_brightness)

        layout.addWidget(self.cpu_label)
        layout.addWidget(self.memory_label)
        layout.addWidget(self.network_label)
        layout.addWidget(self.battery_label)
        layout.addWidget(QLabel("Screen Brightness:"))
        layout.addWidget(self.brightness_slider)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_system_info)
        self.timer.start(700)

        self.prev_net_io_counters = psutil.net_io_counters()
        self.prev_time = psutil.boot_time()
        self.last_network_update = 0
        self.network_update_interval = 0.5

        self.cpu_graph = CPUGraph()
        self.memory_graph = MemoryGraph()
        layout.addWidget(self.cpu_graph)
        layout.addWidget(self.memory_graph)

        self.cpu_percent_data = []
        self.memory_percent_data = []

    def update_system_info(self):
        current_time = time.time()
        if current_time - self.last_network_update >= self.network_update_interval:
            cpu_percent = psutil.cpu_percent()
            memory_percent = psutil.virtual_memory().percent
            battery_percent = psutil.sensors_battery().percent if psutil.sensors_battery() else "Unknown"
            self.cpu_label.setText("CPU Usage: {}%".format(cpu_percent))
            self.memory_label.setText("Memory Usage: {}%".format(memory_percent))
            if battery_percent < 15:
                self.battery_label.setText(f"Low Battery: {battery_percent}%🪫")
            else:
                self.battery_label.setText(f"Battery: {battery_percent}%🔋")
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
                # Afficher les statistiques réseau précédentes
                download_speed_str = self.format_speed((net_io_counters.bytes_recv - self.prev_net_io_counters.bytes_recv) / time_elapsed)
                upload_speed_str = self.format_speed((net_io_counters.bytes_sent - self.prev_net_io_counters.bytes_sent) / time_elapsed)

                network_stats = "Download: {}\nUpload: {}\n".format(download_speed_str, upload_speed_str)

                self.network_label.setText("Network Stats:\n{}".format(network_stats))

        self.cpu_percent_data.append(cpu_percent)
        self.memory_percent_data.append(memory_percent)
        self.cpu_graph.update_graph(self.cpu_percent_data)
        self.memory_graph.update_graph(self.memory_percent_data)

    def toggle_update_notifications(self, checked):
        if checked:
            print("Notifications de mises à jour activées")
        else:
            print("Notifications de mises à jour désactivées")

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

# Widget pour afficher les logiciels en arrière-plan
class LogicielsWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.logiciels_label = QLabel("Logiciels en arrière-plan:")
        layout.addWidget(self.logiciels_label)
        self.tree_logiciels = QTreeWidget()
        self.tree_logiciels.setHeaderLabels(["Nom du Processus", "Utilisateur", "CPU", "Mémoire", "Disque"])
        layout.addWidget(self.tree_logiciels)
        self.setLayout(layout)
        self.update_logiciels()

    def update_logiciels(self):
        self.tree_logiciels.clear()
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                pinfo = proc.info
                item = QTreeWidgetItem([pinfo['name'], pinfo['username'], '', '', ''])
                cpu_percent = proc.cpu_percent()
                memory_info = proc.memory_info()
                disk_info = proc.io_counters()
                item.setData(2, Qt.DisplayRole, f"{cpu_percent}%")
                item.setData(3, Qt.DisplayRole, f"{memory_info.rss / (1024 * 1024):.2f} MB")
                item.setData(4, Qt.DisplayRole, f"{disk_info.read_bytes / (1024 * 1024):.2f} MB")
                self.tree_logiciels.addTopLevelItem(item)
            except psutil.NoSuchProcess:
                pass

# Fenêtre principale de l'application
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("System Monitor")
        self.setWindowIcon(QIcon("icon.png"))

        central_widget = QTabWidget()
        # Vérifie si le système d'exploitation est Windows
        if sys.platform == 'win32':
            system_monitor = SystemMonitor(wmi.WMI(namespace='wmi'))
            logiciels_widget = LogicielsWidget()
        else:
            # Affiche un avertissement si le système d'exploitation n'est pas Windows
            warning_label = QLabel("Cette fonctionnalité est disponible uniquement sur Windows.")
            logiciels_widget = QWidget()
            layout = QVBoxLayout()
            layout.addWidget(warning_label)
            logiciels_widget.setLayout(layout)
            system_monitor = None

        # Ajoute les onglets à la fenêtre principale
        central_widget.addTab(system_monitor, "Système")
        central_widget.addTab(logiciels_widget, "Logiciels")

        self.setCentralWidget(central_widget)

# Point d'entrée de l'application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
