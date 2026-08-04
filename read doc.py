
from google.oauth2.credentials import Credentials    
    
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/documents.readonly"
]

creds = Credentials.from_authorized_user_file("token.json", SCOPES)

docs = build("docs", "v1", credentials=creds)

DOCUMENT_ID = "1SpLDRO9oDo17ufaLr9f-WUpSEUq5K38ajEsESAV_zGM"

document = docs.documents().get(documentId=DOCUMENT_ID).execute()

print("Title:", document["title"])

text = ""

for item in document["body"]["content"]:
    if "paragraph" in item:
        for element in item["paragraph"]["elements"]:
            if "textRun" in element:
                text += element["textRun"]["content"]

print(text)
