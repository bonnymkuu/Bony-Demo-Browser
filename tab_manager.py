from PyQt5.QtWidgets import QTabWidget, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class TabManager(QTabWidget):
    def __init__(self, browser_window):
        super().__init__()
        self.browser_window = browser_window
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)

        self.new_tab_button = QPushButton("+")
        self.new_tab_button.clicked.connect(self.add_new_tab_button_click)
        self.setCornerWidget(self.new_tab_button)

        self.add_new_tab("http://www.duckduckgo.com")

    def add_new_tab(self,url):
        new_tab = QWebEngineView()
        new_tab.setUrl(QUrl(url))

        self.addTab(new_tab,"New Tab")
        self.setCurrentWidget(new_tab)

        new_tab.urlChanged.connect(lambda qurl: self.browser_window.navigation_bar.update_url_bar(qurl))
        self.currentChanged.connect(lambda index: self.update_url_for_active_tab())

    def add_new_tab_button_click(self):
        self.add_new_tab("http://www.duckduckgo.com")

    def update_url_for_active_tab(self):
            current_tab = self.currentWidget()
            if current_tab:
                url = current_tab.url().toString()
                self.browser_window.navigation_bar.update_url_bar(url)

    def current_tab(self):
            return self.currentWidget()    

    def close_tab(self, index):
            if self.count() > 1:
                self.removeTab(index)
            else:
                self.browser_window.close()                