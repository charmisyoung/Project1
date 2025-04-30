"""
Module for the Account and SavingAccount classes
Contains Account class + child class SavingAccount
"""
import csv
import os

class Account:
    """
    A class that emulates a basic bank account
    """

    def __init__(self, name: str, balance: float = 0, pin="0000") -> None:
        """
        Initialize an Account

        :param name: The name of the account
        :param balance: The initial balance, default 0
        :param pin (str): The account PIN, defaulted to 0000
        """
        self.__account_name = name
        self.__balance = balance
        self.__pin = pin
        self.set_balance(balance)


    def deposit(self, amount: float) -> bool:
        """
        Deposit money into the account selected
        :param amount: The amount being deposited
        :return: bool True if deposit is successful, False if not
        """
        if amount <= 0:
            return False
        self.__balance += amount
        return True


    def withdraw(self, amount: float) -> bool:
        """
        Withdraw money from the account selected

        :param amount: The amount to withdraw
        :return: bool True if withdraw successful, False if not
        """
        if amount <= 0 or amount > self.__balance:
            return False
        self.__balance -= amount
        return True

    def get_balance(self) -> float:
        """
        Retrieve the balance of the selected account
        :return: float: Current balance
        """
        return self.__balance


    def get_name(self) -> str:
        """
        Retrieve the name of the account
        :return: str: The account name
        """
        return self.__account_name


    def set_balance(self, value: float) -> None:
        """
        Set the balance of the selected account to specified value

        :param value: float: The new balance of the account
        """
        self.__balance = max(0, value)


    def set_name(self, value: str) -> None:
        """
        Set the name of the selected account to specified value

        :param value: str: Set the new account name
        """
        self.__account_name = value


    def verify_pin(self, user_pin) -> str:
        """Verify PIN entered matches account PIN

        :param user_pin (str): The PIN entered by the user
        :return: bool True if PIN is correct, False if not
        """
        return self.__pin == user_pin


    def set_pin(self, new_pin) -> str:
        """Set a PIN for the account.

        :param new_pin (str): The new PIN
        """
        self.__pin = new_pin


    def get_pin(self) -> str:
        """Get the PIN for the account

        :return (str): account PIN
        """
        return self.__pin


    def __str__(self) -> str:
        """
        Return a summary of the selected account details in string format

        :return: str: Summary of account details
        """
        return f'Account name = {self.get_name()}, Account balance = {self.get_balance():.2f}'


class AccountManager:
    """
    A class that manages storage of account info

    Saves accounts to a CSV file, and loads them from a CSV file.
    """

    def __init__(self, file_path="accounts.csv") -> None:
        """Initialize the AccountManager"""
        self.file_path = file_path
        self.accounts = []

        if not os.path.exists(file_path):
            with open('accounts.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['account_type', 'name', 'balance', 'deposit_count'])

        self.load_accounts()


    def create_account(self, name: str, balance: float = 0, pin="0000") -> None:
        """
        create a new account and add it to accounts list

        :param name (str): Name of the account
        :param balance (float): The initial balance; default 0
        :param pin (str): The account pin, defaulted to 0000
        :return: The new account
        """

        account = Account(name, balance, pin)

        self.accounts.append(account)
        self.save_accounts()
        return account


    def get_account(self, name: str) -> None:
        """
        get an account by name
        :param name: str: The name of the account
        :return: str: Account or SavingAccount or None (account if found, None if not)
        """
        for account in self.accounts:
            if account.get_name().lower() == name.lower():
                return account
        return None


    def get_all_accounts(self) -> None:
        """
        Get all accounts
        :return: list of all accounts
        """
        return self.accounts


    def save_accounts(self) -> None:
        """
        Save all accounts to the CSV
        """
        with open(self.file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'balance', 'pin'])

            for account in self.accounts:
                writer.writerow([
                    account.get_name(),
                    account.get_balance(),
                    account.get_pin()
                ])

    def load_accounts(self) -> None:
        """
        Load all accounts from the CSV file
        """
        self.accounts = []

        try:
            with open(self.file_path, 'r', newline='') as file:
                reader = csv.reader(file)
                header = next(reader)

                for row in reader:
                    try:
                        name, balance, pin = row
                        balance = float(balance)

                        account = Account(name, balance, pin)
                        self.accounts.append(account)

                    except (ValueError, IndexError) as e:
                        print(f"Error loading account from row {row}: {e}")
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading accounts from {self.file_path}: {e}")
