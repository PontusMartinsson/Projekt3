import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
# SCOPES = ["https://www.googleapis.com/auth/documents.readonly"]
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

def main():
  """Shows basic usage of the Docs API.
  Prints the title of a sample document.
  """
  creds = None
  # The file token.json stores the user"s access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("docs", "v1", credentials=creds)

    # Retrieve the documents contents from the Docs service.
    document = service.documents().create(body={"title":"textTest"}).execute() #create document

    _id = document.get("documentId") #get id
  
    text = "placeholder\n"
    xRes = len(text)
    yRes = 5
    red = 0.0
    green = 0.0
    blue = 0.0
    fontFamily = "Courier Prime"
    fontSize = 5
    lineSpacing = 60 # target times 100
    i = 0

    while(i < yRes):
      startIndex = xRes * i + 1
      endIndex = startIndex + xRes

      requests = [
        {
          "insertText": {
            "text": text,
            "location": {
              "index": startIndex
            }
          }
        },
        {
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
        },
        {
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
        }
      ]

      write = service.documents().batchUpdate(documentId=_id, body={"requests": requests}).execute()
      i += 1

  except HttpError as err:
    print(err)

print(__name__)

if __name__ == "__main__":
  main()