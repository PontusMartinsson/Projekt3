import os
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from PIL import Image

from font_analysis import analyze

# help functions --------------------------------------------------

# display and validate a multiple choice question
# returns a string containing a single character
def multipleChoice(question, options):
    question += "\n"
    valid = ""
    i = 0

    while i < len(options):
        question += (chr(i + 97) + ") " + options[i] + "\n")
        valid += chr(i + 97)

        i += 1

    while True:
        userInput = input(question)
        if (userInput in valid) and (len(userInput) == 1):
            print()
            return options[ord(userInput) - 97]
        else:
            print("Invalid input")
            print()

# display and validate a question that expects an int
# returns an int depending on the value inputted
def intQuestion(question):
    question += "\n"

    while True:
        userInput = input(question)
        if userInput.isnumeric():
            print()
            return int(userInput)
        else:
            print("Invalid input")
            print()

# display and validate a yes or no question
# returns a string containing eiter "y" or "n"
def yesNo(question):
    question += "\n(y/n)\n"

    while True:
        userInput = input(question)
        if (userInput == "y"):
            print()
            return "y"
        elif (userInput == "n"):
            print()
            return "n"
        else:
            print("Invalid input")
            print()

# prompt the user to select a file of one or more selected file types in a specified folder
# returns the relative path of the selected file
def pickFile(question, targetFolder, filetypes):
    files = []

    for filename in os.listdir(targetFolder):
        
        for fileExtension in filetypes:
            if filename.endswith(fileExtension):
                files.append(filename)

    file = multipleChoice(question, files)

    return os.path.join(targetFolder, file)

# specific functions/methods ----------------------------------------------

# prompt user to give the program access to Drive
def login():
    SCOPES = ["https://www.googleapis.com/auth/drive.file"]
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

# select a custom preset
# returns an array containing the various option values
def preset():
    path = pickFile("Which preset would you like to use?", "presets", [".txt"])
    preset = []

    with open(path, "r") as file:
        preset = file.readlines()

    options = [None] * 5

    for value in preset:
        if "characters=" in value:
            options[0] = str(re.sub(r'^.*?=', '', value).strip())
        elif "greyscale=" in value:
            options[1] = bool(re.sub(r'^.*?=', '', value).strip())
        elif "width=" in value:
            options[2] = int(re.sub(r'^.*?=', '', value).strip())
        elif "fontsize=" in value:
            options[2] = int(re.sub(r'^.*?=', '', value).strip())
        elif "rowspacing=" in value:
            options[2] = int(re.sub(r'^.*?=', '', value).strip())

    return options

# saves options to a new text document
# returns an array containing the various option values
def savePreset(options):
    # reformat the options array
    order = ["characters", "greyscale", "width", "fontsize", "rowspacing"]
    i = 0

    while i < len(options):
        options[i] = order[i] + "=" + str(options[i]) + "\n"
        i += 1

    # get desired filename from user
    filename = ""
    valid = False

    while not valid:
        filename = input("Please enter your desired file name\n")
        filename += ".txt"
        valid = True

        for file in os.listdir("presets"):
            if file == filename:
                valid = False
                print("There already exists a file with that name, please choose a different one")

    path = os.path.join("presets", filename)

    # create a new .txt file and write to it
    with open(path, "w") as file:
        file.writelines(options)

    print("Preset successfully saved in:", path)

# manual setup
# returns an array containing the various option values
def manual():
    options = []

    # characters
    options.append(input("Please enter all of the characters you would like to use\nDefault is (ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789#*+-=.,!?%&~/$@ ) including space\nThe same character is allowed more than once\n"))
    print()

    # greyscale
    match yesNo("Would you like the image to be greyscale?"):
        case "y":
            options.append(True)
        case "n":
            options.append(False)

    # width
    options.append(intQuestion("How wide would you like the image to be?\nDefault is §\nHeight is calculated automatically"))

    # font size
    options.append(intQuestion("What font size would you like?\nDefault is §"))

    # row spacing
    options.append(intQuestion("What row spacing would you like?\nDefault is §\nGoogle Docs will divide this value by 100, so 50 --> 0.5"))

    # perform font analysis
    print("A font analysis has to be performed")
    print("Depending on how many characters you have chosen, the time this takes might vary")
    options[0] = analyze(options[0], 1000)
    print()

    return(options)  

# main
def main():
    login()

    options = []
    match yesNo("Would you like to use a preset?\nTo create a new preset, choose n"):
        case "y":
            options = preset()
        case "n":
            options = manual()
            if yesNo("Would you like to save this as a new preset?") == "y":
                savePreset(options)

    image = Image.open(pickFile("Which image would you like to use?", "img", [".png", ".jpg", ".jpeg"]))

    docName = input("What would you like to name the output document?\n")

    xRes = options[2]
    yRes = int(float(xRes / image.width) * image.height)

    image.resize((xRes, yRes)).save("temp.png")

    # convert = int((float(val) / 255) * len(options[0]))

main()

# login

# preset?
# custom symbols?
# color
# width (height is automatic)
# save preset?
# name preset

# image
# rescale (if applicable)
# document name