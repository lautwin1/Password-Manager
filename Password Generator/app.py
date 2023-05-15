# Imports
from tkinter import *
import random
import json
global currUser
global symbols

# Variables
password = ""
sec = '416c6578616e6465724c6175383038'
currUser = ""
symbols = [
    "~",
    "`",
    "!",
    "@",
    "#",
    "$",
    "%",
    "^",
    "&",
    "*",
    "()",
    "_",
    "-",
    "+",
    "=",
    "{",
    "[",
    "}",
    "]",
    "|",
    ":",
    ";",
    "'",
    "<",
    ",",
    ">",
    ".",
    "?",
    "/",
    "\\"
]

# ----------Functions---------- #


# GUI to Sign in
def signIn():
    clearScreen(mainFrame)
    webLabel = Label(master=mainFrame, text="Password")
    webLabel.pack()
    input = Entry(master=mainFrame, show="*")
    input.bind('<Return>', entry)
    input.pack()

    enterButton = Button(master=mainFrame, text="Enter", command=entry)
    enterButton.pack()
    create = Label(master=mainFrame, text="Don't have an account? Sign Up")
    cerateAccountBtn = Button(
        master=mainFrame, text="Create an account", command=createAccount)
    create.pack()
    cerateAccountBtn.pack()


# Checks Password
def entry():
    # Gets user input
    password = input.get()
    # Opens the user list as 'data'
    with open("userList.json") as data:
        # Loads json
        userInfo = json.load(data)
        for i in userInfo["user_data"]:
            # Checks the password ('1' is for developement only. Delete when project over)
            if i["password"] == password or password == "1":
                # Sets the user as guest if '1' is entered
                if password == "1":
                    global currUser
                    currUser = "Guest"
                # Sets the user to whatver wherever the password belongs too
                else:
                    currUser = i["name"]
                clearScreen(mainFrame)
                home()
                break
            # If not correct answer was inputed then prompt user to restart
            else:
                input.delete(0, len(password))
                print("You are not allowed in")


# Main home/menu function
def home():
    title = Label(master=mainFrame, text="Welcome Back", font=('Arial', 20))
    title.pack(pady=10)
    generatePass = Button(
        master=mainFrame, text='Generate a new password', command=newPassword)
    generatePass.pack()
    seePass = Button(master=mainFrame, text="See your passwords", command=seePassword)
    seePass.pack()


# GUI for creating a new password
def newPassword():
    clearScreen(mainFrame)
    q1 = Label(master=mainFrame, text="Website Name: ")
    res1 = Entry(master=mainFrame)
    q1.pack()
    res1.pack()

    q2 = Label(master=mainFrame, text="Area Code: ")
    res2 = Entry(master=mainFrame)
    q2.pack()
    res2.pack()

    q3 = Label(master=mainFrame, text="Whats your favorite cheese: ")
    res3 = Entry(master=mainFrame)
    q3.pack()
    res3.pack()

    var = StringVar(mainFrame)
    var.set(symbols[0])
    q4 = Label(master=mainFrame, text="Please pick a unique symbol")
    res4 = OptionMenu(mainFrame, var, *symbols)
    q4.pack()
    res4.pack()

    submit = Button(master=mainFrame, text="Submit", command=lambda: createPassword_and_clearInput(
        res1.get(), res2.get(), res3.get(), var.get()))
    submit.pack()

    def clearInput():
        res1.delete(0, len(res1.get()))
        res2.delete(0, len(res2.get()))
        res3.delete(0, len(res3.get()))

    # Function to create the password and clear the input of the user
    def createPassword_and_clearInput(input1, input2, input3, input4):
        if res1.get() != "" and res2.get() != "" and res3.get() != "":
            clearScreen(passwordFrame)
            clearInput()
            createPassword(input1, input2, input3, input4)
        else:
            clearScreen(passwordFrame)
            passwordWarning = Label(
                master=passwordFrame, text="Please answer all the questions", foreground="red")
            passwordWarning.pack()


# Creates a new password object and writes it to the master file
def createPassword(websiteName, areaCode, favCheese, symbol):
    newUserPassword = websiteName + areaCode + favCheese
    userPassword = {
        "user": currUser,
        "website": websiteName,
        "password": encryption(newUserPassword)
    }
    writeData(userPassword, "passwords.json")
    userPasswordLabel = Label(
        master=passwordFrame, text="Your new password is: " +
        password(websiteName, areaCode, favCheese, symbol)).pack()


def password(str1, str2, str3, symbol):

    return symbol + str1[0:2] + str1[-1] + str2[1] + str3[0: (len(str3)//2)] + symbol


def createAccount():
    clearScreen(mainFrame)
    accountTitle = Label(
        master=mainFrame, text="Create an account", font=("Arial", 20)).pack()
    namePrompt = Label(master=mainFrame, text="Name: ").pack()
    userName = Entry(master=mainFrame)
    userName.pack()
    passwordPrompt = Label(master=mainFrame, text="Master Password: ").pack()
    userPassword = Entry(master=mainFrame, show="*")
    userPassword.pack()
    createBtn = Button(master=mainFrame, text="Create Account",
                       command=lambda: createUserAccount(userName.get(), userPassword.get()))
    createBtn.pack()


def createUserAccount(name, password):
    newUser = {
        "name": name,
        "password": password
    }
    writeData(newUser, 'userList.json')
    signIn()

def seePassword():
    clearScreen(mainFrame)
    title = Label(
        master=mainFrame, text="Your passwords", font=("Arial", 20)).pack()

    with open('passwords.json', 'r') as passwordsList:
        passwords = json.load(passwordsList)
        for i in passwords["passwords"]:
            if i["user"] == currUser:
                test = Label(master=mainFrame, text=i["webiste"] + " - " + i["password"]).pack()


def writeData(new_data, filename):
    dataArray = ""
    if filename == "userList.json":
        dataArray = "user_data"
    else:
        dataArray = "passwords"
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data[dataArray].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)


# Encrypts userpassword
def encryption(val):
    encrypt = ""
    for i in range(len(val)):
        ch = val[i]
        in1 = ord(ch)
        part = hex(in1).lstrip("0x").rstrip("L")
        encrypt += part
    return encrypt


def decode(val):
    toDecode = val
    str = bytes.fromhex(toDecode)
    str = str.decode("ascii")
    return str


# Clears frame from all widgets
def clearScreen(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def entryBind(event):
    entry()


# Function to import website data
"""
def importData():
    with open("websites.json", 'r+') as webData:
        file = json.load(webData)
        print(file)
        webList = open('websiteList.txt', 'r')
        for i in webList:
            website = {
                "name": i
            }
            splicedStr = i.split(".")
            if splicedStr[-1].strip() != "org" and splicedStr[-1].strip() != "com":
                file[".xx"].append(website)
                webData.seek(0)
                json.dump(file, webData, indent=4)
                """


# ----------Window Widgets----------#
root = Tk()
root.title("Password Manager")
root.geometry("500x500")

mainFrame = Frame()
passwordFrame = Frame()
webLabel = Label(master=mainFrame, text="Password")
webLabel.pack()
input = Entry(master=mainFrame, show="*")
input.bind('<Return>', entryBind)
input.pack()

enterButton = Button(master=mainFrame, text="Enter", command=entry)
enterButton.pack()
create = Label(master=mainFrame, text="Don't have an account? Sign Up")
cerateAccountBtn = Button(
    master=mainFrame, text="Create an account", command=createAccount)
create.pack()
cerateAccountBtn.pack()


mainFrame.pack()
passwordFrame.pack()
root.mainloop()
