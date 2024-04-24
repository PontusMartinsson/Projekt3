import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def multipleChoice(question, options):
    question += "\n"
    valid = ""
    i = 0

    while i < len(options):
        question += chr(i + 97)
        valid += chr(i + 97)
        question += ") "
        question += options[i]
        question += "\n"

        i += 1

    while True:
        userInput = input(question)
        if (userInput in valid) and (len(userInput) == 1):
            return options[ord(userInput) - 97]
        else:
            print("Invalid input")

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

def main():
    login()

    imageFiles = []
    for fileName in os.listdir("img"):
        if fileName.endswith(".png") or fileName.endswith(".jpg"):
            imageFiles.append(fileName)

    image = multipleChoice("Which image would you like to use?", imageFiles)

    image = os.path.join("img", image)

    print(image)
 


    # match mode:
    #     case "a":
    #         simple()
    #     case "b":
    #         advanced()
    
    #contnuie

main()

# login

# preset?
# directory
# width (height is automatic)
# color
# custom symbols?
# save preset?
# name preset

# image
# rescale (if applicable)
# document name