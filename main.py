import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'logic'))
from voting_logic import VotingLogic
from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.ui_voting_gui import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox

class Controller(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logic = VotingLogic()
        self.results_jane_label.setText("Jane: 0")
        self.results_john_label.setText("John: 0")
        self.results_jiselle_label.setText("Jiselle: 0")
        self.submit_button.clicked.connect(self.process_vote)
        self.clear_button.clicked.connect(self.clear_fields)

    def process_vote(self):
        try:
            voter_id = self.voter_id_input.text()
            
            if not voter_id.isdecimal() or len(voter_id) != 5:
                QMessageBox.warning(self, "Invalid Input", "Voter ID must be 5 numbers.")
                return

            candidate = None
            if self.jane_radio.isChecked(): candidate = 'Jane'
            elif self.john_radio.isChecked(): candidate = 'John'
            elif self.jiselle_radio.isChecked(): candidate = 'Jiselle'

            if candidate is None:
                QMessageBox.warning(self, "Selection Required", "Please select a candidate.")
                return
            print(f"DEBUG: Candidate being sent to logic is: '{candidate}'")

            if self.logic.cast_vote(candidate, voter_id):
                self.update_display()
                self.clear_fields()
                QMessageBox.information(self, "Success", "Vote cast successfully!")
            else:
                QMessageBox.warning(self, "Error", "This ID has already voted.")

        except Exception as e:
            print(f"Error caught: {e}")
            QMessageBox.critical(self, "Crash Prevented", f"Error: {str(e)}")

    def clear_fields(self):
        self.voter_id_input.clear()
        
        self.jane_radio.setAutoExclusive(False)
        self.john_radio.setAutoExclusive(False)
        self.jiselle_radio.setAutoExclusive(False)
        
        self.jane_radio.setChecked(False)
        self.john_radio.setChecked(False)
        self.jiselle_radio.setChecked(False)
        
        self.jane_radio.setAutoExclusive(True)
        self.john_radio.setAutoExclusive(True)
        self.jiselle_radio.setAutoExclusive(True)
        
        self.voter_id_input.setFocus()

    def update_display(self):
        counts = self.logic.get_results()
        self.results_jane_label.setText(f"Jane: {counts ['Jane']}")
        self.results_john_label.setText(f"John: {counts ['John']}")
        self.results_jiselle_label.setText(f"Jiselle: {counts ['Jiselle']}")


def main():
    app = QApplication(sys.argv)
    window = Controller()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()