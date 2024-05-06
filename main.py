import os
import re
import cv2
import numpy as np

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from PIL import Image, ImageDraw, ImageFont
from alive_progress import alive_bar

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

    return creds

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
            options[0] = str(re.sub(r'^.*?=', "", value).replace("\n", "").replace(" ", ""))
        elif "grayscale=" in value:
            options[1] = bool(re.sub(r'^.*?=', "", value).replace("\n", ""))
        elif "width=" in value:
            options[2] = int(re.sub(r'^.*?=', "", value).replace("\n", ""))
        elif "fontsize=" in value:
            options[3] = int(re.sub(r'^.*?=', "", value).replace("\n", ""))
        elif "rowspacing=" in value:
            options[4] = int(re.sub(r'^.*?=', "", value).replace("\n", ""))

    return options

# saves options to a new text document
# returns an array containing the various option values
def savePreset(options):
    optionsText = options.copy()
    # reformat the options array
    order = ["characters", "grayscale", "width", "fontsize", "rowspacing"]
    i = 0

    while i < len(optionsText):
        optionsText[i] = order[i] + "=" + str(optionsText[i]) + "\n"
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
        file.writelines(optionsText)

    print("Preset successfully saved in:", path)

# manual setup
# returns an array containing the various option values
def manual():
    options = []

    # characters
    options.append(input("Please enter all of the characters you would like to use\nDefault is (ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789#*+-=.,!?%&~/$@)\nThe same character is allowed more than once\nAny spaces will be ignored\n").replace(" ", ""))
    print()

    # grayscale
    match yesNo("Would you like the image to be grayscale?"):
        case "y":
            options.append(True)
        case "n":
            options.append(False)

    # width
    options.append(intQuestion("How wide would you like the image to be?\nDefault is §\nHeight is calculated automatically"))

    # font size
    options.append(intQuestion("What font size would you like?\nDefault is §"))

    # row spacing
    options.append(intQuestion("What row spacing would you like?\nDefault is §\nGoogle Docs will divide this value by 100, so 60 --> 0.6"))

    # perform font analysis
    print("A font analysis has to be performed")
    print("Depending on how many characters you have chosen, the time this takes might vary")
    options[0] = analyze(options[0], 1000)
    print()

    return(options) 

# draw, analyze and sort selected characters based on the amount of black pixels
# returns a string containing the selected characters in order from most to least amount of pixels
def analyze(characters, resolution):
    pixels = []
    font = ImageFont.truetype("font.ttf", resolution)

    # characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789#*+-=.,!?%&~/$@ " #default characters
    char_list = list(characters)

    # create a blank canvas to render the symbols
    canvas_size = (resolution, resolution)
    canvas = Image.new("L", canvas_size, color=255)
    draw = ImageDraw.Draw(canvas)

    with alive_bar(len(characters)) as bar:
        for char in char_list:
            draw.text((0, 0), char, font=font, fill=0) # draw the symbol onto the canvas

            glyph_array = np.array(canvas)
            binary_glyph_array = (glyph_array > 128).astype(np.uint8) * 255
            
            img = Image.fromarray(binary_glyph_array)
            img.save("letter.png")

            img_analysis = cv2.imread("letter.png", cv2.IMREAD_GRAYSCALE)
            
            pixels.append(np.sum(img_analysis == 0))

            draw.rectangle([0, 0, resolution, resolution], fill=255) #clear canvas

            bar()

    i = 0

    while i < len(pixels):
        j = 1

        while j < len(pixels) - i:
            if pixels[j] > pixels[j-1]:
                pixels[j], pixels[j-1] = pixels[j-1], pixels[j]
                char_list[j], char_list[j-1] = char_list[j-1], char_list[j]

            j += 1
        
        i += 1

    os.remove("letter.png")

    characters = "".join(char_list)

    return characters

# convert the image to grayscale and translate each pixel to a character
# returns an array of strings where each character represents a pixel 
def grayscale(characters, yRes):
    image = cv2.imread('temp.png', cv2.IMREAD_GRAYSCALE)
    output = [""] * yRes
    i = 0

    while i < yRes:
        for pixel in image[i]:
            output[i] += characters[int(float(pixel / 255) * (len(characters) - 1))]
        i += 1

    return output

def writeDoc(creds, grayscale, docName, content, xRes, yRes, fontSize, lineSpacing):
    try:
        service = build("docs", "v1", credentials=creds)
        document = service.documents().create(body={"title":docName}).execute() # create document

        _id = document.get("documentId") # get id
    
        # text = "placeholder\n"
        # xRes = len(text)
        # yRes = 5
        red = 0.0
        green = 0.0
        blue = 0.0
        fontFamily = "Courier Prime"
        # fontSize = 5
        # lineSpacing = 60 # target times 100
        i = 0

        requests = []

        while(i < yRes):
            startIndex = xRes * i + 1
            endIndex = startIndex + xRes

            requests.append({
                "insertText": {
                    "text": content[i],
                    "location": {
                        "index": startIndex
                    }
                }
            })

            requests.append({
                "updateParagraphStyle": {
                    "range": {
                        "startIndex": startIndex,
                        "endIndex": endIndex
                    },
                    "paragraphStyle": {
                        "lineSpacing":lineSpacing
                    },
                    "fields": "lineSpacing"
                }
            })

            requests.append({
                "updateTextStyle": {
                    "range": {
                        "startIndex": startIndex,
                        "endIndex": endIndex
                    },
                    "textStyle": {
                        "weightedFontFamily": {
                            "fontFamily": fontFamily
                        },
                        "fontSize": {
                            "magnitude": fontSize,
                            "unit": "PT"
                        },
                        "foregroundColor": {
                            "color": {
                                "rgbColor": {
                                    "red": red,
                                    "green": green,
                                    "blue": blue
                                }
                            }
                        }
                    },
                    "fields": "weightedFontFamily, fontSize, foregroundColor"
                }
            })

            i += 1

        write = service.documents().batchUpdate(documentId=_id, body={"requests": requests}).execute()

    except HttpError as err:
        print(err)

# main
def main():
    creds = login()

    options = []
    match yesNo("Would you like to use a preset?\nTo create a new preset, choose n"):
        case "y":
            options = preset()
        case "n":
            options = manual()
            if yesNo("Would you like to save this as a new preset?") == "y":
                savePreset(options)

    image = Image.open(pickFile("Which image would you like to use?", "img", [".png", ".jpg", ".jpeg"]))

    print(options)
    xRes = options[2]
    yRes = int(float(xRes / image.width) * image.height)
    image.resize((xRes, yRes)).save("temp.png")

    docName = input("What would you like to name the output document?\n")

    match options[1]:
        case True:
            writeDoc(creds, True, docName, grayscale(options[0], yRes), xRes, yRes, options[3], options[4])
        case False:
            writeDoc(creds, False, docName, color(options[0], yRes), xRes, yRes, options[3], options[4])
    
    os.remove("temp.png")

main()