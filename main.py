import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'logic'))
from voting_logic import VotingLogic
from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.ui_voting_gui import Ui_MainWindow

class Controller(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logic = VotingLogic()
        self.submit_button.clicked.connect(self.process_vote)

    def process_vote(self):
        if self.jane_radio.isChecked():
            self.logic.cast_vote('Jane')
            print("Voted Jane")
        elif self.john_radio.isChecked():
            self.logic.cast_vote('John')
            print("Voted John")
        elif self.other_radio.isChecked():
            self.logic.cast_vote('Other')
            print("Voted Other")

    def update_display(self):
        counts = self.logic.get_results()
        self.results_john_label.setText(f"John: {counts['John']}")
        self.results_jane_label.setText(f"Jane: {counts['Jane']}")
        self.results_other_label.setText(f"Other: {counts['Other']}")

    def process_vote(self):
        if self.jane_radio.isChecked():
            self.logic.cast_vote('Jane')
        elif self.john_radio.isChecked():
            self.logic.cast_vote('John')
        elif self.other_radio.isChecked():
            self.logic.cast_vote('Other')
        self.update_display()



def main():
    app = QApplication(sys.argv)
    window = Controller()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()