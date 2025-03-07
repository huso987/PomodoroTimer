import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QFont, QIcon


class PomodoroApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PomodoroTimer")
        self.setFixedSize(600, 300)
        self.setWindowIcon(QIcon('icon.ico'))
        # Timer ayarları
        self.work_time = 25 * 60  # 25 dakika (saniye cinsinden)
        self.break_time = 5 * 60  # 5 dakika
        self.current_time = self.work_time
        self.is_work = True
        self.is_running = False
        self.session_count = 0

        # Widget'lar
        self.time_label = QLabel(self.format_time(self.current_time))
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setFont(QFont('Arial', 32))

        self.start_button = QPushButton("Başlat")
        self.reset_button = QPushButton("Sıfırla")
        self.counter_label = QLabel("Tamamlanan Pomodoro: 0")

        # Buton stilleri
        self.start_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.reset_button.setStyleSheet("background-color: #f44336; color: white;")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.time_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.counter_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        # Buton bağlantıları
        self.start_button.clicked.connect(self.toggle_timer)
        self.reset_button.clicked.connect(self.reset_timer)

    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def toggle_timer(self):
        self.is_running = not self.is_running
        if self.is_running:
            self.start_button.setText("Durdur")
            self.timer.start(1000)
        else:
            self.start_button.setText("Devam Et")
            self.timer.stop()

    def update_timer(self):
        self.current_time -= 1
        self.time_label.setText(self.format_time(self.current_time))

        if self.current_time <= 0:
            self.timer.stop()
            self.is_running = False
            self.start_button.setText("Başlat")

            if self.is_work:
                self.session_count += 1
                self.counter_label.setText(f"Tamamlanan Pomodoro: {self.session_count}")
                self.statusBar().showMessage("Mola zamanı! 🎉", 5000)
                self.current_time = self.break_time
                self.is_work = False
            else:
                self.statusBar().showMessage("Çalışma zamanı! 💪", 5000)
                self.current_time = self.work_time
                self.is_work = True

            self.time_label.setText(self.format_time(self.current_time))

    def reset_timer(self):
        self.timer.stop()
        self.is_running = False
        self.current_time = self.work_time
        self.is_work = True
        self.session_count = 0
        self.time_label.setText(self.format_time(self.current_time))
        self.start_button.setText("Başlat")
        self.counter_label.setText("Tamamlanan Pomodoro: 0")
        self.statusBar().clearMessage()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PomodoroApp()
    window.show()
    sys.exit(app.exec_())