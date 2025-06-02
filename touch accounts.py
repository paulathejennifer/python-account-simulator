import datetime

    @property
    def date(self):
        return self._date

    @property
    def time(self):
        return self._time

    def __str__(self):
        return (f"Date: {self.date}, Time: {self.time}, Type: {self.transaction_type}, "
                f"Amount: {self.amount:.2f}, Narration: {self.narration}")

class Account:
    _interest_rate = 0.05 

    def __init__(self, account_number, account_owner, initial_balance=0.0):
        self._account_number = account_number
        self._account_owner = account_owner
        self._transactions = []  
        self._loan_amount = 0.0
        self._is_frozen = False
        self._minimum_balance = 0.0

        
        if initial_balance > 0:
            self._add_transaction(initial_balance, 'deposit', 'Initial deposit')


    @property
    def account_number(self):
        return self._account_number

    @property
    def account_owner(self):
        return self._account_owner

    @account_owner.setter
    def account_owner(self, new_owner):
        if isinstance(new_owner, str) and new_owner.strip():
            self._account_owner = new_owner
        else:
            print("Invalid account owner name.")

    @property
    def balance(self):
        return self.get_balance()

    def _add_transaction(self, amount, transaction_type, narration):
        transaction = Transaction(amount, transaction_type, narration)
        self._transactions.append(transaction)

    def get_balance(self):
        """Method to calculate an account balance from deposits and withdrawals."""
        balance = 0.0
        for transaction in self._transactions:
            if transaction.transaction_type == 'deposit' or transaction.transaction_type == 'transfer_in' or \
               transaction.transaction_type == 'loan_request' or transaction.transaction_type == 'interest':
                balance += transaction.amount
            elif transaction.transaction_type == 'withdrawal' or transaction.transaction_type == 'transfer_out' or \
                 transaction.transaction_type == 'loan_repayment':
                balance -= transaction.amount
        return balance

    def deposit(self, amount):
        """Method to deposit funds, store the deposit and return a message with the new balance to the customer."""
        if self._is_frozen:
            return "Account is frozen. Cannot deposit funds."
        if amount <= 0:
            return "Deposit amount must be positive."
        self._add_transaction(amount, 'deposit', 'Cash deposit')
        return f"Deposit successful. New balance: {self.get_balance():.2f}"

    def withdraw(self, amount):
        """Method to withdraw funds, store the withdrawal and return a message with the new balance to the customer.
           An account cannot be overdrawn. Cannot withdraw if balance is less than minimum balance."""
        if self._is_frozen:
            return "Account is frozen. Cannot withdraw funds."
        if amount <= 0:
            return "Withdrawal amount must be positive."
        current_balance = self.get_balance()
        if current_balance - amount < self._minimum_balance:
            return f"Withdrawal denied. Your balance cannot go below the minimum balance of {self._minimum_balance:.2f}. Current balance: {current_balance:.2f}"
        if current_balance < amount:
            return "Insufficient funds."
        self._add_transaction(amount, 'withdrawal', 'Cash withdrawal')
        return f"Withdrawal successful. New balance: {self.get_balance():.2f}"

    def transfer_funds(self, target_account, amount):
        """Method to transfer funds from one account to an instance of another account."""
        if self._is_frozen:
            return "Source account is frozen. Cannot transfer funds."
        if target_account._is_frozen:
            return "Target account is frozen. Cannot transfer funds."
        if amount <= 0:
            return "Transfer amount must be positive."
        current_balance = self.get_balance()
        if current_balance < amount:
            return "Insufficient funds for transfer."
        if self._account_number == target_account.account_number:
            return "Cannot transfer funds to the same account."

        
        self._add_transaction(amount, 'transfer_out', f"Transfer to {target_account.account_number}")
        target_account._add_transaction(amount, 'transfer_in', f"Transfer from {self._account_number}")
        return (f"Transfer of {amount:.2f} successful from {self.account_number} to {target_account.account_number}. "
                f"Your new balance: {self.get_balance():.2f}")

    def request_loan(self, amount):
        """Method to request a loan amount."""
        if self._is_frozen:
            return "Account is frozen. Cannot request a loan."
        if amount <= 0:
            return "Loan amount must be positive."
        self._loan_amount += amount
        self._add_transaction(amount, 'loan_request', 'Loan requested')
        return f"Loan of {amount:.2f} requested successfully. Total loan amount: {self._loan_amount:.2f}. New balance: {self.get_balance():.2f}"

    def repay_loan(self, amount):
        """Method to repay a loan with a given amount."""
        if self._is_frozen:
            return "Account is frozen. Cannot repay loan."
        if amount <= 0:
            return "Repayment amount must be positive."
        if self._loan_amount == 0:
            return "No outstanding loan to repay."
        if amount > self._loan_amount:
            self._add_transaction(self._loan_amount, 'loan_repayment', 'Loan fully repaid (overpayment)')
            self._loan_amount = 0
            return f"Loan fully repaid. Overpayment of {amount - self._loan_amount:.2f} credited. New balance: {self.get_balance():.2f}"
        
        self._loan_amount -= amount
        self._add_transaction(amount, 'loan_repayment', 'Loan repayment')
        return f"Loan repayment of {amount:.2f} successful. Remaining loan amount: {self._loan_amount:.2f}. New balance: {self.get_balance():.2f}"

    def view_account_details(self):
        """Method to display the account owner's details and current balance."""
        status = "Frozen" if self._is_frozen else "Active"
        return (f"\n--- Account Details for Account Number: {self.account_number} ---\n"
                f"Account Owner: {self.account_owner}\n"
                f"Current Balance: {self.get_balance():.2f}\n"
                f"Outstanding Loan: {self._loan_amount:.2f}\n"
                f"Minimum Balance Requirement: {self._minimum_balance:.2f}\n"
                f"Account Status: {status}\n"
                f"--------------------------------------------------")

    def change_account_owner(self, new_owner_name):
        """Method to update the account owner's name."""
        self.account_owner = new_owner_name  
        return f"Account owner updated to: {self.account_owner}"

    def account_statement(self):
        """Method to generate a statement of all transactions in an account. (Print using a for loop)."""
        if not self._transactions:
            return "No transactions to display."
        statement = f"\n--- Account Statement for Account Number: {self.account_number} ---\n"
        statement += f"Owner: {self.account_owner}\n"
        statement += "--------------------------------------------------\n"
        statement += "Date       Time     Type        Amount      Narration\n"
        statement += "--------------------------------------------------\n"
        for transaction in self._transactions:
            statement += (f"{transaction.date} {transaction.time} "
                          f"{transaction.transaction_type:<11} {transaction.amount:>10.2f} {transaction.narration}\n")
        statement += "--------------------------------------------------\n"
        statement += f"Current Balance: {self.get_balance():.2f}\n"
        statement += "--------------------------------------------------\n"
        return statement

    def interest_calculation(self):
        """Method to calculate and apply an interest to the balance. Use 5% interest."""
        if self._is_frozen:
            return "Account is frozen. Cannot calculate interest."
        current_balance = self.get_balance()
        if current_balance <= 0:
            return "Balance is zero or negative. No interest applied."
        interest_amount = current_balance * self._interest_rate
        self._add_transaction(interest_amount, 'interest', 'Interest applied')
        return f"Interest of {interest_amount:.2f} applied. New balance: {self.get_balance():.2f}"

    def freeze_account(self):
        """Method to freeze the account for security reasons."""
        if self._is_frozen:
            return "Account is already frozen."
        self._is_frozen = True
        return "Account frozen successfully."

    def unfreeze_account(self):
        """Method to unfreeze the account."""
        if not self._is_frozen:
            return "Account is already unfrozen."
        self._is_frozen = False
        return "Account unfrozen successfully."

    def set_minimum_balance(self, amount):
        """Method to enforce a minimum balance requirement."""
        if amount < 0:
            return "Minimum balance cannot be negative."
        self._minimum_balance = amount
        return f"Minimum balance set to: {self._minimum_balance:.2f}"

    def close_account(self):
        """Method to close the account and set all balances to zero and empty all transactions."""
        self._add_transaction(self.get_balance(), 'withdrawal', 'Account closure adjustment') 
        self._transactions = []
        self._loan_amount = 0.0
        self._is_frozen = True 
        return "Account closed successfully. All balances are zero and transactions cleared."


if __name__ == "__main__":

    account1 = Account("ACC001", "Alice Smith", 1000)
    account2 = Account("ACC002", "Bob Johnson", 500)

    print(account1.view_account_details())
    print(account2.view_account_details())

    print("\n--- Testing Deposit ---")
    print(account1.deposit(200))
    print(account1.deposit(-50)) 
    print(account1.view_account_details())

  
    print("\n--- Testing Withdraw ---")
    print(account1.withdraw(150))
    print(account1.withdraw(2000)) 
    print(account1.withdraw(-100)) 
    print(account1.view_account_details())


    print("\n--- Testing Transfer Funds ---")
    print(account1.transfer_funds(account2, 300))
    print(account1.transfer_funds(account2, 10000)) 
    print(account1.transfer_funds(account1, 50))
    print(account1.view_account_details())
    print(account2.view_account_details())

  
    print("\n--- Testing Request Loan ---")
    print(account1.request_loan(500))
    print(account1.view_account_details())

  
    print("\n--- Testing Repay Loan ---")
    print(account1.repay_loan(200))
    print(account1.repay_loan(400)) 
    print(account1.view_account_details())


    print("\n--- Testing Change Account Owner ---")
    print(account1.change_account_owner("Alice Wonderland"))
    print(account1.view_account_details())


    print("\n--- Testing Interest Calculation ---")
    print(account2.interest_calculation())
    print(account2.view_account_details())


    print("\n--- Testing Freeze/Unfreeze Account ---")
    print(account1.freeze_account())
    print(account1.deposit(100)) 
    print(account1.unfreeze_account())
    print(account1.deposit(100)) 
    print(account1.view_account_details())

   
    print("\n--- Testing Minimum Balance ---")
    print(account1.set_minimum_balance(500))
    print(account1.withdraw(500))
    print(account1.withdraw(100)) 
    print(account1.view_account_details())

 
    print("\n--- Testing Account Statement ---")
    print(account1.account_statement())
    print(account2.account_statement())


    print("\n--- Testing Close Account ---")
    print(account1.close_account())
    print(account1.view_account_details())
    print(account1.deposit(100)) 
