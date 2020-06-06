# Imports of external libraries
from tabulate import tabulate
import csv
import sys, argparse, csv

# Global Variables
users = {}
expenseHistory = {}

# Main Method
def main():

    # Variables to store data inside main
    username = ""
    password = ""

    # Reads data from users.csv to the users dictionary of program evertime program runs
    readUsers()
    readExpenseHistory()
    print(expenseHistory)

    while(True):
        # Program start running
        printInitials()

        # Getting Choice
        while(True):
            try:
                choice = int(input("What do you want to do? Enter Choice: "))
                if(choice > 0 and choice < 5):
                    break
            except:
                print("Please Enter Integer for choice between 1,2 and 3")

        # User Functionality
        if(choice == 1):
            username, password = getCredentials()
            if(password == ""):
                continue
            else:
                while(True):
                    userMenu()
                    while(True):
                        try:
                            choice1 = int(input("What do you want to do? Enter Choice: "))
                            if(choice1 > 0 and choice1 < 6):
                                break
                        except:
                            print("Please Enter Integer for choice between 1,2 and 3")
                    
                    # Amount in Wallet showing
                    if(choice1 == 1):
                        print(f"Amount in the wallet is: {users[username][0]}\n")

                    # Updating Expense
                    elif(choice1 == 2):

                        expenseInfo = input("Enter Expense Info: ")
                        
                        while(True):
                            try:
                                expense = int(input("Enter the expense amount: "))
                                break
                            
                            except:
                                print("Please Enter integers for expense amount")

                        if(expense < users[username][0]):
                            users[username][0] -= expense
                            expenseHistory[username][expenseInfo] = expense
                        else:
                            print("You have less money than expense, Can't Update Wallet")

                    # Entering Money in wallet    
                    elif(choice1 == 3):
                        while(True):
                            try:
                                money = int(input("Enter the money to add: "))
                                break
                            
                            except:
                                print("Please Enter integers for expense")
                        if(money > 0):
                            users[username][0] += money
                        else:
                            print("Entered amount was invalid, Can't Update Wallet")

                    # Printing Expense History of this user
                    elif(choice1 == 4):
                        printExpenseHistory(username)
                            
                    # Logout 
                    elif(choice1 == 5):
                        break

        # Registeration of a new Member Functionality
        elif(choice == 2):
            registerMember()

        # Admin Functionality
        elif(choice == 3):
            username, password = getAdminCredentials()

            if(username == "admin" and password == "admin@123"):
                while(True):
                    adminMenu()
                    while(True):
                        try:
                            choice3 = int(input("What do you want to do? Enter Choice: "))
                            if(choice3 > 0 and choice3 < 4):
                                break
                        except:
                            print("Please Enter Integer for choice between 1 and 2")

                    if(choice3 == 1):
                        total = calculateTotal() 
                        print(f"Total Money in Bank of All Users is: {total}")
                    elif(choice3 == 2):
                        printDetails()
                    elif(choice3 == 3):
                        break
            else:
                print("Incorrect username or password")

        # Writes data into users.csv file and Exits the Program
        elif(choice == 4):
            writeUsers()
            writeExpenseHistory()
            return

    return


# My Functions
# Prints the Welcome Screen and Main Menu
def printInitials():
    print("=========== Welcome to Pocket Manager ===========")
    print()
    print("1) Login to Your Wallet")
    print("2) Dont have a wallet, Make One!")
    print("3) Admin Login")
    print("4) Exit Program")

    return


# User Menu
def userMenu():
    print("1) Check amount in your Wallet")
    print("2) Enter expense in your Wallet")
    print("3) Enter money in your Wallet")
    print("4) View Expense History")
    print("5) Logout")
    return

# Admin Menu
def adminMenu():
    print("1) Check total amount in bank")
    print("2) Details of All the Customers in bank")
    print("3) Logout")
    return

# Getting valid username and password from user 
def getCredentials():

    username = ""
    password = ""

    u = input("Enter Username: ")
    p = input("Enter Password: ")

    for user in users:
        if(u == user):
            username = u
            break

    if(username != ""):
        if(users[username][1] ==  p):
            password = p
        else:
            print("Incorrect Password")
    else:
        print("Incorrect Username")


    #print(username, password)    
    return username, password

# Getting Admin Credentials
def getAdminCredentials():

    username = ""
    password = ""

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    return username, password

# Registering a new user and making his wallet
def registerMember():

    while(True):
        username = input("Enter username for your wallet: ")
        if(username not in users):
            break
        else:
            print("Username is already taken, Try different username")
            continue

    password = input("Enter a strong password for your wallet: ")

    users[username] = [0,password]
    expenseHistory[username] = {}

    print("Registeration Successfull")

    return

# Calculates Total of all the wallets in bank 
def calculateTotal():

    total = 0
    
    for user in users:
        total += users[user][0]

    return total

# Print Usernames and amounts of all the wallets in bank
def printDetails():

    myData = []

    for user in users:
        myData.append((user, users[user][0]))

    headers = ["Username", "Amount"]

    print()
    print(tabulate(myData, headers = headers, tablefmt = "grid"))

    return

# Writes users data into users.csv file
def writeUsers():
    f = open("users.csv", "w+")

    for user in users:
        print()
        f.write(f"{user},{users[user][0]},{users[user][1]}\n")
    print()    

    f.close()
    return

def readUsers():

    try:
        with open('users.csv', mode = 'r') as infile:
            reader = csv.reader(infile)
            temp = 'null'

            counter = 0
            for row in reader:
                users[row[0]] = [int(row[1]),row[2]]
                
    except OSError as e:
        print("File recipes.csv not found for reading or error in their format")
        return 1

    return

# Prints Expense History of a specific user
def printExpenseHistory(username):
    
    expenses = expenseHistory[username]

    myData = []

    for expense in expenses:
        myData.append((expense, expenses[expense]))

    headers = ["Expense", "Amount"]

    print(f"Expense History of {username} is:-\n")
    print(tabulate(myData, headers = headers, tablefmt = "grid"))    

    return

# Reads expenseHistory.csv file
def readExpenseHistory():

    try:
        with open('expenseHistory.csv', mode = 'r') as infile:
            reader = csv.reader(infile)
            temp = 'null'

            counter = 0
            for row in reader:
                for item in range(len(row)):
                    if(item == 0):
                        expenseHistory[row[0]] = {}
                        continue
                    if(item%2 == 1):
                        expenseHistory[row[0]][row[item]] = 0
                        temp = row[item]
                    elif(item%2 == 0):
                        expenseHistory[row[0]][temp] = int(row[item])
                    
                    counter+=1

                counter = 0
    except OSError as e:
        print("File recipes.csv not found for reading or error in their format")
        return 1

    return

def writeExpenseHistory():

    f = open("expenseHistory.csv", "w+")

    for user in expenseHistory:
        print(user)
        f.write(f"{user},")
        count = 0
        for expense in expenseHistory[user]:
            print(expense)
            f.write(f"{expense},{expenseHistory[user][expense]}")
            count+=1
            if(count < len(expenseHistory[user])):
                f.write(",")
                            
        f.write("\n")    

    f.close()

    return

# Declaration of Main
main()
