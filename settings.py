from PyQt5.QtWidgets import QMenu, QAction, QMenuBar, QVBoxLayout, QDialog, QPushButton, QLabel, QMainWindow,QMessageBox
from PyQt5.QtGui import QKeySequence
from tab_manager import TabManager

class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.tab_manager = TabManager(self)

        # Add a label for menu
        self.menu_label = QLabel("Settings Menu")
        layout.addWidget(self.menu_label)

        # Create a menu bar
        self.menu_bar = QMenuBar(self)
        layout.addWidget(self.menu_bar)

        # Create menu
        self.settings_menu = QMenu("Settings", self)
        self.menu_bar.addMenu(self.settings_menu)

        # Add actions to menu
        self.add_action("New Tab", "Ctrl+T", self.new_tab)
        self.add_action("Open File", "Ctrl+O", self.open_file_dialog)
        self.add_action("History", "Ctrl+H", self.show_history)
        self.add_action("Downloads", "Ctrl+J", self.show_downloads)
        self.add_action("Favorites", "Ctrl+B", self.show_favorites)
        self.add_action("Zoom In", "Ctrl+Plus", self.zoom_in)
        self.add_action("Zoom Out", "Ctrl+Minus", self.zoom_out)
        self.add_action("Reset Zoom", "Ctrl+0", self.reset_zoom)
        self.add_action("Print", "Ctrl+P", self.print_page)
        self.add_action("View Source", "Ctrl+U", self.view_source)
        self.add_action("Find", "Ctrl+F", self.find_text)
        self.add_action("Developer Tools", "Ctrl+Shift+I", self.open_dev_tools)
        self.add_action("Settings", "Ctrl+Comma", self.open_settings)
        self.add_action("About", "Ctrl+Shift+A", self.about_browser)
        self.add_action("Exit", "Ctrl+Q", self.exit_browser)

    def add_action(self, text, shortcut, slot):
        action = QAction(text, self)
        action.setShortcut(QKeySequence(shortcut))
        action.triggered.connect(slot)
        self.settings_menu.addAction(action)

    # Define slots for each menu action
    def new_tab(self):
        self.tab_manager.add_new_tab()

    def open_file_dialog(self):
        """Open a file dialog and load an HTML file."""
        file_dialog = QFileDialog()
        file_name, _ = file_dialog.getOpenFileName(self, "Open File", "", "HTML Files (*.html);;All Files (*)")
        if file_name:
            self.browser_window.load_url(QUrl.fromLocalFile(file_name))
            print(f"File {file_name} opened.")

    def show_history(self):
        """Display browser history."""
        # Assuming you have a history viewer widget or method
        history_window = self.browser_window.show_history()
        history_window.exec_()  # Open the history dialog
        print("History window opened.")

    def show_downloads(self):
        """Display browser downloads."""
        # Assuming a downloads manager is implemented
        downloads_window = self.browser_window.show_downloads()
        downloads_window.exec_()  # Open the downloads dialog
        print("Downloads window opened.")

    def show_favorites(self):
        """Display the list of favorite/bookmarked pages."""
        # Assuming a favorites/bookmarks manager is implemented
        favorites_window = self.browser_window.show_favorites()
        favorites_window.exec_()  # Open the favorites dialog
        print("Favorites window opened.")

    def zoom_in(self):
        """Zoom in the current web page."""
        current_tab = self.browser_window.tab_manager.currentWidget()
        if current_tab:
            current_tab.setZoomFactor(current_tab.zoomFactor() + 0.1)
            print("Zoomed in.")

    def zoom_out(self):
        """Zoom out the current web page."""
        current_tab = self.browser_window.tab_manager.currentWidget()
        if current_tab:
            current_tab.setZoomFactor(current_tab.zoomFactor() - 0.1)
            print("Zoomed out.")

    def reset_zoom(self):
        """Reset the zoom to the default level."""
        current_tab = self.browser_window.tab_manager.currentWidget()
        if current_tab:
            current_tab.setZoomFactor(1.0)
            print("Zoom reset to default.")

    def print_page(self):
        """Print the current web page."""
        current_tab = self.browser_window.tab_manager.currentWidget()
        if current_tab:
            current_tab.page().printToPdf("output.pdf")  # Print to a PDF file
            print("Page sent to printer (or saved as PDF).")

    def view_source(self):
        """View the source code of the current web page."""
        current_tab = self.browser_window.tab_manager.currentWidget()
        if current_tab:
            current_tab.page().toHtml(self._handle_source_code)
            print("Viewing source code.")

    def _handle_source_code(self, html):
        """Callback to handle the HTML source."""
        # Open a dialog or editor to display the HTML
        source_dialog = QDialog(self)
        source_dialog.setWindowTitle("Page Source")
        layout = QVBoxLayout()
        source_edit = QTextEdit()
        source_edit.setPlainText(html)
        layout.addWidget(source_edit)
        source_dialog.setLayout(layout)
        source_dialog.resize(800, 600)
        source_dialog.exec_()
        print("Source code displayed.")

    def find_text(self):
        """Open a find bar to search text in the current page."""
        current_tab = self.browser_window.tab_manager.currentWidget()
        if current_tab:
            find_dialog = QDialog(self)
            find_dialog.setWindowTitle("Find Text")
            layout = QVBoxLayout()
            find_input = QLineEdit()
            find_input.setPlaceholderText("Enter text to find...")
            layout.addWidget(find_input)

            find_button = QPushButton("Find")
            find_button.clicked.connect(lambda: current_tab.findText(find_input.text()))
            layout.addWidget(find_button)

            find_dialog.setLayout(layout)
            find_dialog.exec_()
            print(f"Searching for: {find_input.text()}")

    def open_dev_tools(self):
        """Open the developer tools for the current tab."""
        current_tab = self.browser_window.tab_manager.currentWidget()
        if current_tab:
            dev_tools = QWebEngineView()
            dev_tools_page = current_tab.page().createDevToolsPage()
            dev_tools.setPage(dev_tools_page)
            dev_tools_window = QMainWindow()
            dev_tools_window.setCentralWidget(dev_tools)
            dev_tools_window.setWindowTitle("Developer Tools")
            dev_tools_window.show()
            print("Developer tools opened.")

    def open_settings(self):
        pass

    def about_browser(self):
        msg = QMessageBox()
        msg.setWindowTitle("About Browser")
        msg.setText("Simple python browser")
        msg.exec_()

    def exit_browser(self):
        pass
