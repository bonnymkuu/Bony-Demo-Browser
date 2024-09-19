from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout,QWidget, QMenuBar, QAction, QMenu, QFileDialog, QLabel
from settings import SettingsDialog

class NavigationBar(QWidget):
    def __init__(self, browser_window):
        super().__init__()
        self.browser_window = browser_window
        self.init_ui()
    
    def init_ui(self):
        self.layout = QHBoxLayout()

        self.logo_label = QLabel()
        self.logo_pixmap = QPixmap("moo.png")
        self.logo_label.setPixmap(self.logo_pixmap)
        self.logo_label.setFixedSize(30,30)
        self.layout.addWidget(self.logo_label)

        self.back_button = QPushButton("<")
        self.back_button.setFixedSize(30,30)
        self.back_button.clicked.connect(self.browser_window.go_back)
        self.layout.addWidget(self.back_button)    

        self.forward_button = QPushButton(">")
        self.forward_button.setFixedSize(30,30)
        self.forward_button.clicked.connect(self.browser_window.go_forward)
        self.layout.addWidget(self.forward_button)

        self.reload_button = QPushButton()
        self.reload_button.setIcon(QIcon("refresh.png"))
        self.reload_button.setFixedSize(30,30)
        self.reload_button.clicked.connect(self.browser_window.reload_page)
        self.layout.addWidget(self.reload_button)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter Url link ...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.layout.addWidget(self.url_bar,1)

        self.open_file_button = QPushButton()
        self.open_file_button.setIcon(QIcon("open.png"))
        self.open_file_button.setFixedSize(30,30)
        self.open_file_button.clicked.connect(self.open_file_dialog)
        self.layout.addWidget(self.open_file_button)

        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon("moo.png"))
        self.settings_button.setFixedSize(30,30)
        self.settings_button.clicked.connect(self.open_setting_dialog)
        self.layout.addWidget(self.settings_button)

        self.setLayout(self.layout)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http://") and not url.startswith("https://") and not url.startswith("file://"):
            url = "http://" + url
        self.browser_window.load_url(url)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open HTML File", "", "HTML Files (*.html *.htm);;All Files (*)")
        if file_path:
            local_url = "file://" + file_path
            self.browser_window.load_url(local_url)    
    
    def open_setting_dialog(self):
        settings_dialog = SettingsDialog()
        settings_dialog.exec_()        

    def update_url_bar(self, url):
        self.url_bar.setText(url.toString())            

    def show_about(self):
        from PyQt5.QtWidget import QMessageBox
        msg = QMessageBox()
        msg.setWindowTitle("About Browser")
        msg.setText("Simple python browser")
        msg.exec_()