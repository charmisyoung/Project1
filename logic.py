"""
Module for Banking Application logic
Contains Logic class that connects UI to account management logic
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *

from gui import *
from accounts import *


class Logic(QMainWindow, Ui_BankingApplication):
    """
    Main logic for banking app

    Logic class connects UI and account management logic
    """
    def __init__(self) -> None:
        """Initialize logic for banking app"""
        super().__init__()

        self.setupUi(self)

        self.account_manager = AccountManager()
        self.current_account = None
        self.last_verified_account = ""

        self.create_acct_button.clicked.connect(self.create_account)
        self.deposit_button.clicked.connect(self.deposit)
        self.withdraw_button.clicked.connect(self.withdraw)
        self.select_acct_combobox.currentTextChanged.connect(self.account_selection_change)
        self.login_button.clicked.connect(self.login)
        self.nav_to_create_button.clicked.connect(self.show_create_account)
        self.nav_to_login_button.clicked.connect(self.show_login)
        self.enter_pin_validate.clicked.connect(self.verify_selected_account)

        self.show_create_account()

        self.deposit_button.setEnabled(False)
        self.withdraw_button.setEnabled(False)

        self.refresh_ui()


    def refresh_ui(self) -> None:
        """Refresh with latest account data"""
        self.update_select_acct_combobox()
        self.update_account_details()


    def update_select_acct_combobox(self) -> None:
        accounts = self.account_manager.get_all_accounts()

        current_text = self.select_acct_combobox.currentText()

        self.select_acct_combobox.clear()

        self.select_acct_combobox.addItem("--Select an account--")

        for account in accounts:
            self.select_acct_combobox.addItem(account.get_name())

        if current_text:
            index = self.select_acct_combobox.findText(current_text)
            if index >= 0:
                self.select_acct_combobox.setCurrentIndex(index)
        else:
            self.select_acct_combobox.setCurrentIndex(0)

        index = self.select_acct_combobox.findText(current_text)
        if index >= 0:
            self.select_acct_combobox.setCurrentIndex(index)


    def update_account_details(self) -> None:
        """Update account details of selected account"""
        account_name = self.select_acct_combobox.currentText()
        account = self.account_manager.get_account(account_name)

        if self.current_account:
            self.balance_message_label.setText(f"Welcome {account.get_name()}\n"
                                               f"Your account balance is ${account.get_balance():.2f}")
            self.deposit_button.setEnabled(True)
            self.withdraw_button.setEnabled(True)
        else:
            self.balance_message_label.setText(f"Welcome. Create or select an account to continue.")
            self.deposit_button.setEnabled(False)
            self.withdraw_button.setEnabled(False)


    def account_selection_change(self) -> None:
        """Handle when account selection changes"""
        account_name = self.select_acct_combobox.currentText()

        if account_name != self.last_verified_account:
            self.current_account = None
            self.update_account_details()

            if account_name and account_name != "--Select Account --":
                self.statusbar.showMessage(f"{account_name}, please verify your PIN to continue.")
            else:
                self.statusbar.showMessage("")


    def verify_selected_account(self) -> None:
        """PIN verification for select account section"""
        account_name = self.select_acct_combobox.currentText()

        if not account_name or account_name == "--Select Account--":
            QMessageBox.warning(self, "Error", "Please select an account")
            return

        user_pin = self.pin_input.text()

        if not user_pin:
            QMessageBox.warning(self, "Error", "Please enter your PIN")
            return

        account = self.account_manager.get_account(account_name)

        if not account:
            QMessageBox.warning(self, "Error", "Account not found")
            return

        if not account.verify_pin(user_pin):
            QMessageBox.warning(self, "Error", "Incorrect PIN")
            return

        self.current_account = account
        self.last_verified_account = account_name
        self.update_account_details()
        self.statusbar.showMessage(f"Welcome, {account_name}.")
        self.pin_input.clear()


    def show_login(self) -> None:
        """Show login form once account created"""
        self.login_box.setVisible(True)
        self.create_account_box.setVisible(False)
        self.select_acct_box.setVisible(True)
        self.transaction_box.setVisible(True)
        self.balance_message_label.setVisible(True)


    def show_create_account(self) -> None:
        """Show create account screen upon entering"""
        self.create_account_box.setVisible(True)
        self.login_box.setVisible(False)
        self.select_acct_box.setVisible(True)
        self.transaction_box.setVisible(True)
        self.balance_message_label.setVisible(True)


    def login(self) -> None:
        """Handle the login process"""
        try:
            account_name = self.account_login_input.text()
            pin = self.pin_login_input.text()

            if not account_name:
                QMessageBox.warning(self, "Error", "Please enter an account name")
                return

            if not pin:
                QMessageBox.warning(self, "Error", "Please enter your PIN")
                return

            account = self.account_manager.get_account(account_name)

            if not account:
                QMessageBox.warning(self, "Error", "Account not found")
                return

            if not account.verify_pin(pin):
                QMessageBox.warning(self, "Error", "Incorrect PIN")
                return

            index = self.select_acct_combobox.findText(account_name)
            if index >= 0:
                self.select_acct_combobox.setCurrentIndex(index)

                self.update_account_details()

                self.account_login_input.clear()
                self.pin_login_input.clear()

                self.statusbar.showMessage(f"Logged in as {account_name}")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {e}")


    def create_account(self) -> None:
        """Create a new account with UI data"""
        try:
            name = self.account_name_input.text()

            if not name:
                QMessageBox.warning(self, "Error",  "Account name cannot be empty")
                return

            account_type = 'regular'
            
            pin = self.set_pin_input.text()
            
            if not pin.isdigit() or len(pin) != 4:
                QMessageBox.warning(self,"Error", "PIN must be 4 digits.")
                return

            try:
                balance = float(self.initial_balance_input.text() or "0")
                if balance < 0:
                    QMessageBox.warning(self, "Error",  "Initial balance cannot be negative.")
                    return
            except ValueError:
                QMessageBox.warning(self, "Error",  "Enter a valid number for initial balance.")
                return

            if self.account_manager.get_account(name):
                QMessageBox.warning(self, "Error",  "An account with this name already exists.")
                return

            account = self.account_manager.create_account(name, balance, pin)

            self.refresh_ui()
            self.statusbar.showMessage(f"Account '{name}' created successfully.")

            self.account_name_input.clear()
            self.initial_balance_input.clear()
            self.set_pin_input.clear()

            self.account_login_input.setText(name)

            self.show_login()

        except Exception as e:
            QMessageBox.warning(self, "Error",  f"An error occurred: {e}")


    def verify_pin(self) -> bool:
        """Verify PIN before transaction"""
        account_name = self.select_acct_combobox.currentText()
        account = self.account_manager.get_account(account_name)

        if not account:
            QMessageBox.warning(self,"Error", "No account selected.")
            return False

        user_pin = self.pin_input.text()

        if not user_pin:
            QMessageBox.warning(self,"Error", "Please enter your PIN")
            return False

        if not account.verify_pin(user_pin):
            QMessageBox.warning(self,"Error", "Incorrect PIN")
            return False

        return True


    def deposit(self) -> None:
        """Deposit money into selected account"""
        try:
            if not self.verify_pin():
                return

            account_name = self.select_acct_combobox.currentText()

            try:
                amount = float(self.amount_input.text() or "0")
                if amount <= 0:
                    QMessageBox.warning(self, "Error",  "Amount must be greater than zero.")
                    return
            except ValueError:
                QMessageBox.warning(self, "Error",  "Please enter a valid number.")
                return

            account = self.account_manager.get_account(account_name)

            if not account:
                QMessageBox.warning(self, "Error",  "No account selected.")
                return

            success = account.deposit(amount)

            if success:
                self.account_manager.save_accounts()
                self.refresh_ui()
                self.statusbar.showMessage(f"Deposit successful")

                self.amount_input.clear()
                self.pin_input.clear()
            else:
                QMessageBox.warning(self, "Error",  "Deposit failed.")
        except Exception:
            return

    def withdraw(self) -> None:
        """Withdraw money from the selected account"""
        try:
            if not self.verify_pin():
                return

            account_name = self.select_acct_combobox.currentText()

            try:
                amount = float(self.amount_input.text() or "0")
                if amount <= 0:
                    QMessageBox.warning(self, "Error",  "Amount must be greater than zero.")
                    return
            except ValueError:
                QMessageBox.warning(self, "Error",  "Enter a valid number.")
                return

            account = self.account_manager.get_account(account_name)

            if not account:
                QMessageBox.warning(self,"Error","No account selected.")
                return

            success = account.withdraw(amount)

            if success:
                self.account_manager.save_accounts()
                self.refresh_ui()
                self.statusbar.showMessage(f"Withdrawal successful")

                self.amount_input.clear()
                self.pin_input.clear()
            else:
                QMessageBox.warning(self, "Error",  "Withdrawal failed.")
        except Exception:
            return