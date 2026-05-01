import sys
from logic.voting_logic import Logic
from PyQt6.QtWidgets import QApplication

def main() -> None:
    app = QApplication(sys.argv)

    # Initialize logic class
    window = Logic()
    window.show()

    # Start the event loop
    sys.exit(app.exec())

if __name__ == '__main__':
    main()