import sys
import re
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QSpinBox
)

from auth_client import AuthClient


class LoginTab(QWidget):
    """Login tab UI."""

    def __init__(self, auth_client: AuthClient, on_login_success=None):
        super().__init__()
        self.auth_client = auth_client
        self.on_login_success = on_login_success
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Login")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Email
        layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        layout.addWidget(self.email_input)

        # Password
        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Login button
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self._on_login)
        layout.addWidget(login_btn)

        layout.addStretch()
        self.setLayout(layout)

    def _on_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Validation Error", "Email and password are required")
            return

        if not self._is_valid_email(email):
            QMessageBox.warning(self, "Validation Error", "Invalid email format")
            return

        # Call backend
        result = self.auth_client.login(email, password)
        if result["success"]:
            QMessageBox.information(
                self, "Success",
                f"Welcome, {result['data']['user']['name']}!"
            )
            self.email_input.clear()
            self.password_input.clear()
            if self.on_login_success:
                self.on_login_success(result['data'])
        else:
            QMessageBox.critical(
                self, "Login Failed",
                f"Error: {result['error']}"
            )

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None


class RegisterTab(QWidget):
    """Register tab UI."""

    def __init__(self, auth_client: AuthClient, on_register_success=None):
        super().__init__()
        self.auth_client = auth_client
        self.on_register_success = on_register_success
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Register")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Name
        layout.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your full name")
        layout.addWidget(self.name_input)

        # Email
        layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        layout.addWidget(self.email_input)

        # Password
        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter a password (min 6 chars)")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Confirm Password
        layout.addWidget(QLabel("Confirm Password:"))
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm your password")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_password_input)

        # Register button
        register_btn = QPushButton("Register")
        register_btn.clicked.connect(self._on_register)
        layout.addWidget(register_btn)

        layout.addStretch()
        self.setLayout(layout)

    def _on_register(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()

        # Validation
        if not all([name, email, password, confirm_password]):
            QMessageBox.warning(self, "Validation Error", "All fields are required")
            return

        if not self._is_valid_email(email):
            QMessageBox.warning(self, "Validation Error", "Invalid email format")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "Validation Error", "Password must be at least 6 characters")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Validation Error", "Passwords do not match")
            return

        # Call backend
        result = self.auth_client.register(name, email, password)
        if result["success"]:
            QMessageBox.information(
                self, "Success",
                f"User {name} registered successfully! You can now login."
            )
            self._clear_fields()
            if self.on_register_success:
                self.on_register_success(result['data'])
        else:
            QMessageBox.critical(
                self, "Registration Failed",
                f"Error: {result['error']}"
            )

    def _clear_fields(self):
        self.name_input.clear()
        self.email_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None


class DashboardTab(QWidget):
    """Dashboard shown after successful login."""

    def __init__(self, on_logout=None):
        super().__init__()
        self.on_logout = on_logout
        self.user_data = None
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()

        # Welcome message
        self.welcome_label = QLabel("Welcome to Dashboard")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        self.welcome_label.setFont(title_font)
        layout.addWidget(self.welcome_label)

        # User info
        self.info_label = QLabel()
        layout.addWidget(self.info_label)

        layout.addStretch()

        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self._on_logout)
        layout.addWidget(logout_btn)

        self.setLayout(layout)

    def set_user_data(self, user_data):
        self.user_data = user_data
        user = user_data.get("user", {})
        self.welcome_label.setText(f"Welcome, {user.get('name', 'User')}!")
        self.info_label.setText(
            f"Email: {user.get('email', 'N/A')}\n"
            f"User ID: {user.get('id', 'N/A')}\n"
            f"Token: {user_data.get('access_token', '')[:30]}..."
        )

    def _on_logout(self):
        if self.on_logout:
            self.on_logout()


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Authentication System - PyQt6 & FastAPI")
        self.setMinimumSize(QSize(500, 400))
        self.resize(600, 500)

        # Auth client
        self.auth_client = AuthClient(base_url="http://localhost:8000")

        # Create tabs
        self.tabs = QTabWidget()

        self.login_tab = LoginTab(self.auth_client, on_login_success=self._on_login_success)
        self.register_tab = RegisterTab(self.auth_client, on_register_success=self._on_register_success)
        self.dashboard_tab = DashboardTab(on_logout=self._on_logout)

        self.tabs.addTab(self.login_tab, "Login")
        self.tabs.addTab(self.register_tab, "Register")
        self.tabs.addTab(self.dashboard_tab, "Dashboard")

        # Initially disable dashboard tab
        self.tabs.setTabEnabled(2, False)

        self.setCentralWidget(self.tabs)

    def _on_login_success(self, user_data):
        """Handle successful login."""
        self.dashboard_tab.set_user_data(user_data)
        self.tabs.setTabEnabled(2, True)
        self.tabs.setCurrentIndex(2)

    def _on_register_success(self, user_data):
        """Handle successful registration."""
        self.tabs.setCurrentIndex(0)  # Switch to login tab

    def _on_logout(self):
        """Handle logout."""
        self.auth_client.token = None
        self.auth_client.user = None
        self.tabs.setTabEnabled(2, False)
        self.login_tab.email_input.clear()
        self.login_tab.password_input.clear()
        self.tabs.setCurrentIndex(0)
        QMessageBox.information(self, "Logged Out", "You have been logged out successfully")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
