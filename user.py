class User:
    def __init__(self, name, lastName, birthdate, idNumber, email, password, balance, accountStatement):
        self.name = name
        self.lastName = lastName
        self.birthdate = birthdate
        self.idNumber = idNumber
        self.email = email
        self.password = password
        self.balance = balance
        self.accountStatement = accountStatement

    # Main methods
    def home(self):
        return self.balance

    def deposit(self, value: float):
        if value <= 0:
            status = False
            msg = None
            return status, msg
        else:
            status = True
            msg = "Deposit completed successfully"
            self.balance += value
            return status, msg

    def withdraw(self, value: float):
        if value <= 0:
            status = False
            msg = None
            return status, msg
        else:
            status = True
            msg = "Withdraw completed successfully"
            self.balance -= value
            return status, msg

    def pix (self, value: float, recipientPix, typePix):
        recipient = User.findRecipient(recipientPix, typePix)
        
        if value <= 0:
            status = False
            msg = None
            return status, msg
        
        if self.balance < value:
            status = False
            msg = "Insufficient account balance"
        else:
            status = True
            msg = f"Transaction of R$ {value:.2f} for {recipient.name} {recipient.lastName} completed successfully"
            self.balance -= value
            recipient.balance += value

        return status, msg

    def shop(self):
        pass

    def statement(self):
        return self.accountStatement
        
    # Auxiliar methods
    @staticmethod # These are the methods that do not have self as an argument
    def findRecipient(recipientPix, typePix):
        recipient = None
        return recipient