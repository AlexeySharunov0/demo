import sys
from PyQt6.QtWidgets import QApplication

from auth.registration import RegistrationWindow


def main() -> None:
    app = QApplication(sys.argv)
    window = RegistrationWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
