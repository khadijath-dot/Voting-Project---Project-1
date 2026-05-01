import sys
#import os
#sys.path.append(os.path.join(os.path.dirname(__file__), 'logic'))
from logic.voting_logic import Logic
from PyQt6.QtWidgets import QApplication
#from ui.ui_voting_gui import Ui_MainWindow
#from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox

def main():
    app = QApplication(sys.argv)
    window = Logic()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()