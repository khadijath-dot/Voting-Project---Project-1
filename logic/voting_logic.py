import csv
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from ui.ui_voting_gui import Ui_MainWindow

class Logic (QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.votes = {'John': 0, 'Jane': 0, 'Jiselle': 0}
        self.voted_ids = set()
        self.results_jane_label.setText("Jane: 0")
        self.results_john_label.setText("John: 0")
        self.results_jiselle_label.setText("Jiselle: 0")
        self.submit_button.clicked.connect(self.process_vote)
        self.clear_button.clicked.connect(self.clear_fields)
        self.update_display()

    def cast_vote(self, candidate_name, voter_id):
        if voter_id in self.voted_ids:
            return False 
        if candidate_name in self.votes:
            self.votes[candidate_name] += 1
            self.voted_ids.add(voter_id)
            return True
        return False
    
    def get_results(self):
        return self.votes

    def process_vote(self):
        try:
            voter_id = self.voter_id_input.text().strip()
            
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

            if self.cast_vote(candidate, voter_id):
                self.save_votes()
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
        counts = self.get_results()
        self.results_jane_label.setText(f"Jane: {counts ['Jane']}")
        self.results_john_label.setText(f"John: {counts ['John']}")
        self.results_jiselle_label.setText(f"Jiselle: {counts ['Jiselle']}")

    def save_votes(self):
        with open('results.csv', 'w', newline = '') as f:
            writer = csv.writer(f)
            writer.writerow(['Candidate', 'Votes'])
            for name, count in self.votes.items():
                writer.writerow([name, count])

    
    