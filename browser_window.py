from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from navigation_bar import NavigationBar
from tab_manager import TabManager
from settings import SettingsDialog
import fitz
import pyttsx3
import os

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bonny Browser")
        self.setGeometry(100,100,1200,800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.navigation_bar = NavigationBar(self)
        self.layout.addWidget(self.navigation_bar)

        self.tab_manager = TabManager(self)
        self.layout.addWidget(self.tab_manager)

        self.text_to_speech_engine = pyttsx3.init()

        self.setStyleSheet("""
            QMainWindow {
                background-color: #2e2e2e;  /* Dark background color */
            }
            QLineEdit {
                background-color: #404040;  /* Darker background for URL bar */
                color: #ffffff;            /* White text */
                border: 1px solid #606060; /* Slightly lighter border */
                padding: 5px;
            }
            QPushButton {
                background-color: #505050;  /* Button background */
                color: #ffffff;            /* White text */
                border: 1px solid #707070; /* Button border */
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #606060;  /* Button hover background */
            }
            QLabel {
                color: #ffffff;            /* White text for labels */
            }
        """)

        self.show()

    def load_url(self,url):
        if url.startswith("file://") and url.endswith(".pdf"):
            local_path = url[7:]
            self.read_pdf_aloud(local_path)
        else:    
            self.tab_manager.current_tab().setUrl(QUrl(url)) 

    def read_pdf_aloud(self, file_path):
        doc = fitz.open(file_path)
        full_text = ""
        for page_nim in range(len(doc)):
            page = doc.load_page(page_num)
            full_text += page.get_text()

        self.text_to_speech_engine.say(full_text)
        self.text_to_speech_engine.runAndWait()            

    def go_back(self):
        self.tab_manager.current_tab().back()

    def go_forward(self):
        self.tab_manager.current_tab().forward()

    def reload_page(self):
        self.tab_manager.current_tab().reload()
  
    def open_settings(self):
        self.settings_dialog = SettingsDialog(self)
        self.settings_dialog.exec_()