from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from gui.logininterface import Ui_MainWindowLogIn
from gui.signininterface import Ui_MainWindowSignIn
from gui.bankinterface import Ui_MainWindowBank
from user import User
import json


class ChangeMode():
    def __init__(self):
        ChangeMode.logInApp = LogInApp()
        ChangeMode.signInApp = SignInApp()
        ChangeMode.bankApp = BankApp(None)

class LogInApp(QMainWindow, Ui_MainWindowLogIn):
    def __init__(self):
        super().__init__() 
        super().setupUi(self)
        
        # Call the logIn method when the Log in pushbutton is pressed
        self.login_button.clicked.connect(self.logIn)

        # Call the signIn method when the Sign in pushbutton is pressed
        self.signin_button.clicked.connect(self.signIn)

    # --------------------------------------------------------------------------------
    # This method verifies if the login information is valid. If it is, the user is 
    # successfully logged in.
    def logIn(self):
        # Get email and password from lineEdits
        email = self.email_lineEdit.text()
        password = self.password_lineEdit.text()

        # Load users data from users.json file
        with open("./data/users.json", "r") as sourceR:
            usersData = json.load(sourceR)
        usersList = usersData["users"]

        # Check if the email and password provided in the lineEdits exist in the database
        for userDict in usersList:
            # If so, create an object of the User class and initiate the main interface 
            # of the bank
            if userDict["Email"] == email and userDict["Password"] == password:
                user = User(name=userDict["Name"], lastName=userDict["LastName"], 
                            birthdate=userDict["Birthdate"], idNumber=userDict["IdNumber"],
                            email=userDict["Email"], password=userDict["Password"], 
                            balance=userDict["Balance"], accountStatement=userDict["AccountStatement"])

                ChangeMode.logInApp.hide()
                ChangeMode.bankApp.setUser(user)
                ChangeMode.bankApp.show()
                break

            else:
                # Otherwise, display a message indicating invalid email or password
                self.invalidMsg_label.setText("Invalid e-mail or password")

    # --------------------------------------------------------------------------------
    # This method is called when the user wishes to create a new user account. The 
    # login interface is hidden and the sign-in interface is displayed.
    def signIn(self):
        ChangeMode.logInApp.hide()
        ChangeMode.signInApp.clear()
        ChangeMode.signInApp.show()

    # --------------------------------------------------------------------------------
    # This method clears the text in some interface elements of the login interface
    def clear(self):
        self.email_lineEdit.clear()
        self.password_lineEdit.clear()
        self.invalidMsg_label.clear()

class SignInApp(QMainWindow, Ui_MainWindowSignIn):
    def __init__(self):
        super().__init__() 
        super().setupUi(self)

        # Call the backToLogIn method when the back pushbutton is pressed
        self.back_button.clicked.connect(self.backToLogIn)

        # Call the createUser method when the create pushbutton is pressed
        self.create_button.clicked.connect(self.createUser)

    # --------------------------------------------------------------------------------
    # This method is called when the user wishes to go back to the login interface. 
    # The sign-in interface is hidden and the login interface is displayed.
    def backToLogIn(self):
        ChangeMode.signInApp.hide()
        ChangeMode.logInApp.clear()
        ChangeMode.logInApp.show()

    # --------------------------------------------------------------------------------
    # This method is responsible for creating a new user account. It is necessary to 
    # check whether the information provided is valid.
    def createUser(self):
        # Get information from lineEdits
        name = self.name_lineEdit.text()
        lastName = self.lastName_lineEdit.text()
        birthdateDay = self.birthdateDay_lineEdit.text()
        birthdateMonth = self.birthdateMonth_lineEdit.text()
        birthdateYear = self.birthdateYear_lineEdit.text()
        idNumber = self.idNumber_lineEdit.text()
        email = self.email_lineEdit.text()
        password = self.password_lineEdit.text()

        # Call the checkUserInformation method
        check, msg = self.checkUserInformation(name, lastName, birthdateDay, birthdateMonth, birthdateYear, idNumber)

        if check:
            # If check is true, it means that the information provided to create the 
            # account is coherent and a new user can be created.
            newUser = {
                "Name": name,
                "LastName": lastName,
                "Birthdate": birthdateDay + "/" + birthdateMonth + "/" + birthdateYear,
                "IdNumber": idNumber,
                "Email": email,
                "Password": password,
                "Balance": 0.0,
                "AccountStatement": []
            }

            # Load users data from users.json file
            with open("./data/users.json", "r") as sourceR:
                usersData = json.load(sourceR)
            usersList = usersData["users"]

            # Append the new user dictionary in the userList
            usersList.append(newUser)

            # Save the new usersData in the users.json file
            usersData = {"users": usersList}
            with open("./data/users.json", "w") as sourceW:
                json.dump(usersData, sourceW)

            # Call backToLogIn method
            ChangeMode.signInApp.backToLogIn()
            
        else:
            # Otherwise, display an invalid message indicating the issue
            self.invalidMsg_label.setText(msg)

    # --------------------------------------------------------------------------------
    # This method checks whether the information provided to create a new user is valid.
    # It returns a boolean, and an error message. If the user can be created, the error
    # message is none.
    def checkUserInformation(self, name, lastName, birthdateDay, birthdateMonth, birthdateYear, idNumber):
        # Check if the name has not alphabetic characters
        if not name.isalpha():
            return False, "Invalid name"
        
        # Check if the last name has not alphabetic characters
        if not lastName.isalpha():
            return False, "Invalid last name"
        
        # In the case of the date of birth, we first check if the characters are not
        # numeric. Then, we analyze if the date is valid.
        if not birthdateYear.isnumeric():
            return False, "Invalid birthdate"
        
        if not birthdateMonth.isnumeric() and birthdateMonth > 12:
            return False, "Invalid birthdate"
        
        if not birthdateDay.isnumeric():
            return False, "Invalid birthdate"
        else:
            # The months of January, March, May, July, August, October and December have
            # a maximum of 31 days
            if (int(birthdateMonth) == 1 or int(birthdateMonth) == 3 or int(birthdateMonth) == 5 or int(birthdateMonth) ==7 or 
                int(birthdateMonth) == 8 or int(birthdateMonth) == 10 or int(birthdateMonth) == 12):
                if int(birthdateDay) > 31:
                    return False, "Invalid birthdate"
            
            # The months of April, June, September and November have a maximum of 30 days
            elif (int(birthdateMonth) == 4 or int(birthdateMonth) == 6 or int(birthdateMonth) == 9 or int(birthdateMonth) == 11):
                if int(birthdateDay) > 30:
                    return False, "Invalid birthdate"
            
            # The month of February has a maximum of 29 days if the year is a leap year, 
            # and a maximum of 28 days if the year is not a leap year
            elif (int(birthdateMonth) == 2):
                # Leap year
                if (int(birthdateYear)%4 == 0 and int(birthdateYear)%100 != 0) or (int(birthdateYear)%400 == 0):
                    if int(birthdateDay) > 29:
                        return False, "Invalid birthdate"
                # Non-leap year
                else:
                    if int(birthdateDay) > 28:
                        return False, "Invalid birthdate"
                    
        # Checks if the id number has no numeric characters and 11 digits
        if not idNumber.isnumeric() and len(idNumber) != 11:
            return False, "Invalid Id number"
        
        # If reached here, all the information is valid
        return True, None
    
    # --------------------------------------------------------------------------------
    # This method clears the text in some interface elements of the sign-in interface
    def clear(self):
        self.name_lineEdit.clear()
        self.lastName_lineEdit.clear()
        self.birthdateDay_lineEdit.clear()
        self.birthdateMonth_lineEdit.clear()
        self.birthdateYear_lineEdit.clear()
        self.idNumber_lineEdit.clear()
        self.email_lineEdit.clear()
        self.password_lineEdit.clear()
        self.invalidMsg_label.clear()

class BankApp(QMainWindow, Ui_MainWindowBank): 
    def __init__(self, user): 
        super().__init__() 
        super().setupUi(self)

        # User propertie
        self.user = user

        # Initially hide icon widget and start with Home page set
        self.icon_only_widget.hide()
        self.home_button.setChecked(True)
        self.stackedWidget.setCurrentIndex(0)

        # Call methods for changing pages
        self.home_button.toggled['bool'].connect(self.setHomePage)
        self.deposit_button.toggled['bool'].connect(self.setDepositPage)
        self.withdraw_button.toggled['bool'].connect(self.setWithdrawPage)
        self.pix_button.toggled['bool'].connect(self.setPixPage)
        self.shop_button.toggled['bool'].connect(self.setShopPage)
        self.statement_button.toggled['bool'].connect(self.setStatementPage)
        self.settings_button.toggled['bool'].connect(self.setSettingsPage)

        # Call push buttons methods
        self.confirm_deposit_button.clicked.connect(self.deposit)

        # Call push buttons methods
        self.confirm_withdraw_button.clicked.connect(self.withdraw)

        # Call push buttons methods
        self.confirm_pix_button.clicked.connect(self.pix)

        # Call push buttons methods
        self.product1Shop_button.clicked.connect(self.shop1)
        self.product2Shop_button.clicked.connect(self.shop2)
        self.product3Shop_button.clicked.connect(self.shop3)
        self.product4Shop_button.clicked.connect(self.shop4)
        self.product5Shop_button.clicked.connect(self.shop5)
        self.product6Shop_button.clicked.connect(self.shop6)

        # Call method for log out
        self.logOut_button.clicked.connect(self.logOut)

        # Call method for Confirm change email or password
        self.changeEmailorPassword_button.clicked.connect(self.changeEmailorPassword)

        self.deleteAccount_button.clicked.connect(self.deleteAccount)
        
    # --------------------------------------------------------------------------------
    # Methods for changing pages
    def setHomePage(self):
        self.stackedWidget.setCurrentIndex(0)
        self.clear()

    def setDepositPage(self):
        self.stackedWidget.setCurrentIndex(1)
        self.clear()

    def setWithdrawPage(self):
        self.stackedWidget.setCurrentIndex(2)
        self.clear()

    def setPixPage(self):
        self.stackedWidget.setCurrentIndex(3)
        self.clear()

    def setShopPage(self):
        self.stackedWidget.setCurrentIndex(4)
        self.clear()

    def setStatementPage(self):
        self.stackedWidget.setCurrentIndex(5)
        self.clear()

    def setSettingsPage(self):
        self.stackedWidget.setCurrentIndex(6)
        self.clear()

    # --------------------------------------------------------------------------------
    # push buttons methods
    def deposit(self):
        try:
            depositValue = float(self.depositValue_lineEdit.text().replace(",", "."))
            if depositValue <= 0.0:
                msg = "Invalid value"

            else:
                msg = "Deposit successfully authorized, please go to an ATM machine to complete your request."
                self.user.balance += depositValue
                self.user.accountStatement.append(["Deposit ", str(depositValue)])
        except:
            msg = "Invalid value"

        self.msgDeposit_label.setText(msg)
        self.depositValue_lineEdit.clear()

        # Load users data from users.json file
        with open("./data/users.json") as sourceR:
            usersData = json.load(sourceR)
        usersList = usersData["users"]

        # Find current user on data
        for userDict in usersList:
            if userDict["Email"] == self.user.email and userDict["Password"] == self.user.password:
                usersList.remove(userDict)
                userDict ["Balance"] = self.user.balance
                userDict ["AccountStatement"] = self.user.accountStatement
                usersList.append(userDict)
                break

        # Save users data on users.json file
        usersData = {"users": usersList}
        with open("./data/users.json", "w") as sourceW:
            json.dump(usersData, sourceW)

        self.setHome()
        self.setStatement()
        self.setSettings()

    # --------------------------------------------------------------------------------
    # push buttons methods
    def withdraw(self):
        try:
            withdrawValue = float(self.withdrawValue_lineEdit.text().replace(",", "."))
            if withdrawValue <= 0.0:
                msg = "Invalid value"

            elif self.user.balance < withdrawValue:
                msg = "You do not have enough balance to make the withdrawal"
        
            else:
                msg = "Withdraw successfully authorized, please go to ATM machine to complete your request."
                self.user.balance -= withdrawValue
                self.user.accountStatement.append(["Withdraw ", str(withdrawValue)])
        except:
            msg = "Ivalid value"

        self.withdrawValue_lineEdit.clear() 
        self.msgWithdraw_label.setText(msg)

        # Load users data from users.json file
        with open("./data/users.json") as sourceR:
            usersData = json.load(sourceR)
        usersList = usersData["users"]

        # Find current user on data
        for userDict in usersList:
            if userDict["Email"] == self.user.email and userDict["Password"] == self.user.password:
                usersList.remove(userDict)
                userDict ["Balance"] = self.user.balance
                userDict ["AccountStatement"] = self.user.accountStatement
                usersList.append(userDict)
                break

        # Save users data on users.json file
        usersData = {"users": usersList}
        with open("./data/users.json", "w") as sourceW:
            json.dump(usersData, sourceW)

        self.setHome()
        self.setStatement()
        self.setSettings()
          
    # --------------------------------------------------------------------------------
    # push buttons methods
    def pix(self):
        try:
            pixValue = float(self.transferPixValue_lineEdit.text().replace(",", "."))
            if pixValue <= 0.0:
                msg = "Invalid value"

            elif self.user.balance < pixValue:
                msg = "You do not have enough balance to make the pix"
        
            else:
                idNumber = self.idPix_lineEdit.text()
                if not idNumber.isnumeric() and len(idNumber) != 11:
                    msg = "Invalid idNumber"

                else:
                    # Load users data from users.json file
                    with open("./data/users.json") as sourceR:
                        usersData = json.load(sourceR)
                    usersList = usersData["users"]

                    # Check if the id number provided in the lineEdit exists in the database
                    for userDict in usersList:
                        if userDict["IdNumber"] == idNumber:
                            Name = userDict["Name"]
                            LastName = userDict["LastName"]
                            msg = f"pix successfully made for {Name} {LastName}"
                            self.user.balance -= pixValue
                            self.user.accountStatement.append(["Pix sent ", str(pixValue)])

                            usersList.remove(userDict)
                            userDict["Balance"] += pixValue
                            userDict["AccountStatement"].append(["Pix received ", str(pixValue)])
                            usersList.append(userDict)
                            break

                    # Save users data on users.json file
                    usersData = {"users": usersList}
                    with open("./data/users.json", "w") as sourceW:
                        json.dump(usersData, sourceW)

        except:
            msg = "Ivalid value"

        self.transferPixValue_lineEdit.clear()
        self.idPix_lineEdit.clear()
        self.msgpix_label.setText(msg)

        # Load users data from users.json file
        with open("./data/users.json") as sourceR:
            usersData = json.load(sourceR)
        usersList = usersData["users"]

        # Check email and password
        for userDict in usersList:
            if userDict["Email"] == self.user.email and userDict["Password"] == self.user.password:
                usersList.remove(userDict)
                userDict ["Balance"] = self.user.balance
                userDict ["AccountStatement"] = self.user.accountStatement
                usersList.append(userDict)
                break

        # Save users data on users.json file
        usersData = {"users": usersList}
        with open("./data/users.json", "w") as sourceW:
            json.dump(usersData, sourceW)

        self.setHome()
        self.setStatement()
        self.setSettings()      

    # --------------------------------------------------------------------------------
    def shop1(self):
        shopItem = "Monitor Alienware "
        shopValue = 2700.0
        self.shop(shopItem, shopValue)
    
    def shop2(self):
        shopItem = "Mouse G pro "
        shopValue = 650.0
        self.shop(shopItem, shopValue)

    def shop3(self):
        shopItem = "Headset A50 "
        shopValue = 1600.0
        self.shop(shopItem, shopValue)

    def shop4(self):
        shopItem = "Playstation 5 "
        shopValue = 3719.0
        self.shop(shopItem, shopValue)

    def shop5(self):
        shopItem = "Xbox series X "
        shopValue = 2780.0
        self.shop(shopItem, shopValue)

    def shop6(self):
        shopItem = "Keyboard "
        shopValue = 589.6
        self.shop(shopItem, shopValue)

    # push buttons methods
    def shop(self, shopItem, shopValue):
        if self.user.balance < shopValue:
            msg = "Insufficient balance to make this purchase"
    
        else:
            msg = shopItem + "purchase made successfully"
            self.user.balance -= shopValue
            self.user.accountStatement.append([(shopItem + "Purchase "), str(shopValue)])

        self.msgShop_label.setText(msg)

        # Load users data from users.json file
        with open("./data/users.json") as sourceR:
            usersData = json.load(sourceR)
        usersList = usersData["users"]

        # Find current user on data
        for userDict in usersList:
            if userDict["Email"] == self.user.email and userDict["Password"] == self.user.password:
                usersList.remove(userDict)
                userDict ["Balance"] = self.user.balance
                userDict ["AccountStatement"] = self.user.accountStatement
                usersList.append(userDict)
                break

        # Save users data on users.json file
        usersData = {"users": usersList}
        with open("./data/users.json", "w") as sourceW:
            json.dump(usersData, sourceW)

        self.setHome()
        self.setStatement()
        self.setSettings()

    # --------------------------------------------------------------------------------
    # push buttons methods
    def changeEmailorPassword(self):
        newEmail = self.changeEmail_lineEdit.text()
        newPassword = self.changePassword_lineEdit.text()

        if len(newEmail) != 0 and len(newPassword) == 0:
            msg = "E-mail changed successfully"
        elif len(newEmail) == 0 and len(newPassword) != 0:
            msg = "Password changed successfully"
        elif len(newEmail) != 0 and len(newPassword) != 0:
            msg = "E-mail and Password changed successfully"

        # Load users data from users.json file
        with open("./data/users.json") as sourceR:
            usersData = json.load(sourceR)
        usersList = usersData["users"]

        # Find current user on data
        for userDict in usersList:
            if userDict["Email"] == self.user.email and userDict["Password"] == self.user.password:
                usersList.remove(userDict)
                if len(newEmail) != 0:
                    userDict ["Email"] = newEmail
                if len(newPassword) != 0:
                    userDict ["Password"] = newPassword
                usersList.append(userDict)
                break        

        # Save users data on users.json file
        usersData = {"users": usersList}
        with open("./data/users.json", "w") as sourceW:
            json.dump(usersData, sourceW)

        self.changeEmail_lineEdit.clear()
        self.changePassword_lineEdit.clear()
        self.msgChangeAccount_label.setText(msg)

        self.setHome()
        self.setStatement()
        self.setSettings()

    # --------------------------------------------------------------------------------
    # push buttons methods
    def deleteAccount(self):
        # Load users data from users.json file
        with open("./data/users.json") as sourceR:
            usersData = json.load(sourceR)
        usersList = usersData["users"]

        # Find current user on data
        for userDict in usersList:
            if userDict["Email"] == self.user.email and userDict["Password"] == self.user.password:
                usersList.remove(userDict)
                break        

        # Save users data on users.json file
        usersData = {"users": usersList}
        with open("./data/users.json", "w") as sourceW:
            json.dump(usersData, sourceW)

        self.logOut()

    # --------------------------------------------------------------------------------
    # Set user
    def setUser(self, user):
        self.user = user
        self.setHome()
        self.setStatement()
        self.setSettings()
    
    # Set home
    def setHome(self):
        # Update name and last name
        self.name_label.setText(self.user.name + " " + self.user.lastName)

        balanceStr = str(f'{self.user.balance:.2f}')
        newBalanceStr = list(balanceStr.split(".")[0])
        for i in range(len(newBalanceStr))[::-3][1:]:
            newBalanceStr.insert(i + 1, ".")
        newBalanceStr = "".join(newBalanceStr) + "," + balanceStr.split(".")[1]
        self.balance_label.setText("R$ " + newBalanceStr)

    # Set statement
    def setStatement(self):
        # Ui_MainWindowBank.statementContent(self.user.accountStatement)
    # def statementContent(self, statement):
        _translate = QtCore.QCoreApplication.translate
        font = QtGui.QFont()
        font.setPointSize(11)
        h = 70
        for item in self.user.accountStatement:
            label_left = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            label_left.setGeometry(QtCore.QRect(10, h, 341, 31))
            label_left.setFont(font)
            label_left.setAlignment(QtCore.Qt.AlignCenter)
            label_left.setObjectName("label_left")
            label_left.setText(_translate("MainWindowBank", item[0]))

            label_right = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            label_right.setGeometry(QtCore.QRect(370, h, 341, 31))
            label_right.setFont(font)
            label_right.setAlignment(QtCore.Qt.AlignCenter)
            label_right.setObjectName("label_right")
            label_right.setText(_translate("MainWindowBank", item[1]))

            h += 50
        pass
        pass

    # Set settings
    def setSettings(self):
        pass

    # --------------------------------------------------------------------------------
    # Clear user
    def clearUser(self):
        self.user = None

    def logOut(self):
        self.clearUser()
        ChangeMode.bankApp.hide()
        ChangeMode.logInApp.clear()
        ChangeMode.logInApp.show()

    def clear(self):
        self.depositValue_lineEdit.clear()
        self.msgDeposit_label.clear()

        self.withdrawValue_lineEdit.clear() 
        self.msgWithdraw_label.clear()

        self.transferPixValue_lineEdit.clear()
        self.idPix_lineEdit.clear()
        self.msgpix_label.clear()

        self.msgShop_label.clear()

        self.msgChangeAccount_label.clear()

