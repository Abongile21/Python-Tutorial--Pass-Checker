import re
import math
import random
import string
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

class PasswordStrengthCheckerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Set up the main window
        self.setWindowTitle('Password Strength Checker')

        # Create widgets
        self.label_instruction = QLabel('Enter your password:')
        self.entry_password = QLineEdit()
        self.entry_password.setEchoMode(QLineEdit.Password)

        # Buttons for checking strength and suggesting random password
        self.button_check_strength = QPushButton('Check Password Strength')
        self.button_check_strength.clicked.connect(self.password_strength_checker)

        self.button_suggest_password = QPushButton('Suggest Random Password')
        self.button_suggest_password.clicked.connect(self.suggest_random_password)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_instruction)
        layout.addWidget(self.entry_password)
        layout.addWidget(self.button_check_strength)
        layout.addWidget(self.button_suggest_password)

        self.setLayout(layout)

    def check_length(self, password):
        return len(password) >= 8

    def check_character_types(self, password):
        return any(c.isupper() for c in password) and any(c.islower() for c in password) \
               and any(c.isdigit() for c in password) and any(c.isalnum() for c in password)

    def check_common_password(self, password):
        common_passwords = ["password", "123456", "qwerty", "abc123"]
        return password.lower() not in common_passwords

    def calculate_entropy(self, password):
        character_set_size = 26 + 26 + 10 + 33
        return len(password) * math.log2(character_set_size)

    def password_strength_checker(self):
        # Retrieve the password from the input field
        password = self.entry_password.text()
        suggestions = []

        # Check for password length
        if not self.check_length(password):
            suggestions.append("Use a password with at least 8 characters.")

        # Check for a mix of character types
        if not self.check_character_types(password):
            suggestions.append("Include a mix of uppercase letters, lowercase letters, numbers, and special characters.")

        # Check against common passwords
        if not self.check_common_password(password):
            suggestions.append("Avoid common passwords.")

        # Display suggestions if the password is weak
        if suggestions:
            message = "Password is weak. Suggestions:\n" + "\n".join(suggestions)
            QMessageBox.warning(self, 'Password Strength', message)
        else:
            # If the password is strong, display entropy information
            entropy = self.calculate_entropy(password)
            QMessageBox.information(self, 'Password Strength', f'Password strength: Strong (Entropy: {entropy:.2f})')

    def suggest_random_password(self):
        # Generate a random password
        suggested_password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=12))
        self.entry_password.setText(suggested_password)

        # Save suggested password to a text file
        self.save_to_text_file(suggested_password)

    def save_to_text_file(self, password):
        try:
            with open("suggested_password.txt", "w") as file:
                file.write(password)
            QMessageBox.information(self, 'Password Suggestion', 'Suggested password saved to suggested_password.txt')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to save suggested password to file: {str(e)}')

if __name__ == '__main__':
    app = QApplication([])
    window = PasswordStrengthCheckerApp()
    window.show()
    app.exec_()
