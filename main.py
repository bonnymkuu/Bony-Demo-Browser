import sys
from PyQt5.QtWidgets import QApplication
from browser_window import BrowserWindow

def main():
    app = QApplication(sys.argv)
    browser = BrowserWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()    