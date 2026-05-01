import csv
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from ui.ui_voting_gui import Ui_MainWindow

class Logic (QMainWindow, Ui_MainWindow):
    '''
    Main logic class for the voting system.
    '''

    def __init__(self) -> None:
        '''
        Initializes the window, UI components, and data structures
        '''
        super().__init__()
        self.setupUi(self)

        # Initialize tallying
        self.votes = {'John': 0, 'Jane': 0, 'Jiselle': 0}
        self.voted_ids = set()

        # Set initial UI state that tallies the votes
        self.results_jane_label.setText("Jane: 0")
        self.results_john_label.setText("John: 0")
        self.results_jiselle_label.setText("Jiselle: 0")

        # Connect buttons to respective functions
        self.submit_button.clicked.connect(self.process_vote)
        self.clear_button.clicked.connect(self.clear_fields)

        # Syncs display with initial data
        self.update_display()


    def cast_vote(self, candidate_name: str, voter_id: str) -> bool:
        '''
        Checks if a voter has already voted and adds the data to tally

        :param candidate_name: string name of selected candidate
        :param voter_id: the 5-digit voter ID which is a string
        return: true if vote was successful, false if ID already exists
        '''
        # Check for duplicate voting by verifying if ID is in the set of voted IDs
        if voter_id in self.voted_ids:
            return False 
        
        # Update vote dictionary and mark ID as used by adding to voted set
        if candidate_name in self.votes:
            self.votes[candidate_name] += 1
            self.voted_ids.add(voter_id)
            return True
        return False
    

    def get_results(self) -> bool:
        '''
        Return current voting dictionary
        '''
        return self.votes


    def process_vote(self) -> None:
        '''
        Gathers input, validates, updates the model, and saves data
        '''
        try:
            # Clean ID input by converting the input value to text and removing trailing spaces
            voter_id = self.voter_id_input.text().strip()
            
            # Validate input to make sure input is 5 digits
            if not voter_id.isdecimal() or len(voter_id) != 5:
                QMessageBox.warning(self, "Invalid Input", "Voter ID must be 5 numbers.")
                return

            # Determine candidate selection from radio buttons
            candidate = None
            if self.jane_radio.isChecked(): candidate = 'Jane'
            elif self.john_radio.isChecked(): candidate = 'John'
            elif self.jiselle_radio.isChecked(): candidate = 'Jiselle'

            # if statement for if a no candidate is selected
            if candidate is None:
                QMessageBox.warning(self, "Selection Required", "Please select a candidate.")
                return
            #print(f"DEBUG: Candidate being sent to logic is: '{candidate}'")

            # Record the vote
            if self.cast_vote(candidate, voter_id):
                # Save and clear if the vote was valid and unique (ID is 5 digits and not repeated)
                self.save_votes()
                self.update_display()
                self.clear_fields()
                QMessageBox.information(self, "Success", "Vote cast successfully!")
            else:
                QMessageBox.warning(self, "Error", "This ID has already voted.")
        
        except Exception as e:
            # Prevents app from crashing on sudden errors
            print(f"Error caught: {e}")
            QMessageBox.critical(self, "Crash Prevented", f"Error: {str(e)}")
            

    def clear_fields(self) -> None:
        '''
        Resets input fields and candidate radio buttons after each vote is casted
        '''
        self.voter_id_input.clear()
        # Temporarily disable auto-exclusive to allow for unchecking all buttons
        self.jane_radio.setAutoExclusive(False)
        self.john_radio.setAutoExclusive(False)
        self.jiselle_radio.setAutoExclusive(False)
        
        self.jane_radio.setChecked(False)
        self.john_radio.setChecked(False)
        self.jiselle_radio.setChecked(False)
        
        # Re-enable auto-exclusive buttons for next selection
        self.jane_radio.setAutoExclusive(True)
        self.john_radio.setAutoExclusive(True)
        self.jiselle_radio.setAutoExclusive(True)
        
        self.voter_id_input.setFocus()


    def update_display(self) -> None:
        '''
        Refreshes tally labels with latest vote counts
        '''
        counts = self.get_results()
        self.results_jane_label.setText(f"Jane: {counts ['Jane']}")
        self.results_john_label.setText(f"John: {counts ['John']}")
        self.results_jiselle_label.setText(f"Jiselle: {counts ['Jiselle']}")


    def save_votes(self) -> None:
        """
        Writes the current vote tallies from the dictionary to a .csv file.
        Each time, the file is overwritten to reflect the latest totals.
        """
        with open('results.csv', 'w', newline = '') as f:
            writer = csv.writer(f)
            writer.writerow(['Candidate', 'Votes'])
            for name, count in self.votes.items():
                writer.writerow([name, count])

    
    