import sys
import threading
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QLabel,
    QDateTimeEdit,
    QComboBox,
    QHBoxLayout,
    QCheckBox,
    QSystemTrayIcon,
    QAction,
    QMenu,
)
from PyQt5.QtCore import QDateTime, QTimer, Qt
from PyQt5.QtGui import QIcon
from plyer import notification

class ToDoListApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('To-Do List')
        self.setGeometry(100, 100, 400, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.task_entry = QTextEdit(self)
        self.task_entry.setPlaceholderText('Enter a task...')
        self.layout.addWidget(self.task_entry)

        self.due_datetime = QDateTimeEdit(self)
        self.due_datetime.setDateTime(QDateTime.currentDateTime())
        self.layout.addWidget(self.due_datetime)

        self.time_format_label = QLabel("Time Format:")
        self.time_format_combo = QComboBox(self)
        self.time_format_combo.addItems(["12-Hour", "24-Hour"])
        self.layout.addWidget(self.time_format_label)
        self.layout.addWidget(self.time_format_combo)

        self.add_button = QPushButton('Add Task', self)
        self.add_button.clicked.connect(self.add_task)
        self.layout.addWidget(self.add_button)

        self.task_container = QWidget(self)
        self.task_layout = QVBoxLayout()
        self.task_container.setLayout(self.task_layout)
        self.layout.addWidget(self.task_container)

        self.central_widget.setLayout(self.layout)

        self.tasks = []

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_due_tasks)
        self.timer.start(1000)

        self.tray_icon = QSystemTrayIcon(QIcon('icon.png'), self)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.toggle_minimize)

        self.tray_menu = self.setup_tray_menu()
        self.tray_icon.setContextMenu(self.tray_menu)

    def setup_tray_menu(self):
        menu = QMenu()
        restore_action = QAction("Restore", self)
        exit_action = QAction("Exit", self)
        restore_action.triggered.connect(self.restore)
        exit_action.triggered.connect(self.exit)
        menu.addActions([restore_action, exit_action])
        return menu

    def toggle_minimize(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            if self.isMinimized() or not self.isVisible():
                self.show()
                self.setWindowState(Qt.WindowNoState)
            else:
                self.hide()

    def restore(self):
        self.show()
        self.setWindowState(Qt.WindowNoState)

    def exit(self):
        self.tray_icon.hide()
        sys.exit()

    def add_task(self):
        task_text = self.task_entry.toPlainText()
        due_datetime = self.due_datetime.dateTime()
        time_format = self.time_format_combo.currentText()

        if task_text:
            due_datetime_str = due_datetime.toString('yyyy-MM-dd hh:mm AP') if time_format == "12-Hour" else due_datetime.toString('yyyy-MM-dd HH:mm')
            task = {"text": task_text, "due_datetime": due_datetime_str, "time_format": time_format, "finished": False, "sound_enabled": True}
            self.tasks.append(task)
            self.update_task_list()
            self.task_entry.clear()

    def update_task_list(self):
        for i in reversed(range(self.task_layout.count())):
            widget = self.task_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for idx, task in enumerate(self.tasks, start=1):
            task_text = f"[{idx}: {'Done' if task['finished'] else 'Due'}] [{task['due_datetime']}] {task['text']}:"
            task_widget = QWidget(self)
            task_layout = QHBoxLayout()
            task_widget.setLayout(task_layout)

            task_label = QLabel(self)
            task_label.setTextFormat(Qt.RichText)
            task_label.setStyleSheet("color: green;" if task['finished'] else "color: red;")
            task_label.setText(task_text)
            task_layout.addWidget(task_label)

            if not task["finished"]:
                finish_button = QPushButton('Finish Task', self)
                finish_button.clicked.connect(lambda _, task=task: self.finish_task(task))
                task_layout.addWidget(finish_button)

            delete_button = QPushButton('Delete Task', self)
            delete_button.clicked.connect(lambda _, task=task: self.delete_task(task))
            task_layout.addWidget(delete_button)

            sound_checkbox = QCheckBox('Sound', self)
            sound_checkbox.setChecked(task['sound_enabled'])
            sound_checkbox.stateChanged.connect(lambda state, task=task: self.toggle_sound(task, state))
            task_layout.addWidget(sound_checkbox)

            self.task_layout.addWidget(task_widget)

    def check_due_tasks(self):
        current_datetime = QDateTime.currentDateTime()
        for task in self.tasks:
            due_datetime = QDateTime.fromString(task["due_datetime"], 'yyyy-MM-dd hh:mm AP')
            time_difference = due_datetime.secsTo(current_datetime)
            if 0 <= time_difference <= 1:
                self.notify_task_due(task)

    def notify_task_due(self, task):
        text = task["text"]
        notification_title = "Task Due"
        notification_message = f"Task: {text}"

        if task["sound_enabled"]:
            notification.notify(title=notification_title, message=notification_message, timeout=10)
            threading.Thread(target=self.vibrate_sound).start()

    def vibrate_sound(self):
        import time
        import winsound

        for _ in range(10):
            winsound.Beep(500, 200)
            time.sleep(0.5)

    def finish_task(self, task):
        task["finished"] = True
        task["sound_enabled"] = False
        self.update_task_list()

    def delete_task(self, task):
        self.tasks.remove(task)
        self.update_task_list()

    def toggle_sound(self, task, state):
        task["sound_enabled"] = state == Qt.Checked

def main():
    app = QApplication(sys.argv)
    window = ToDoListApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()