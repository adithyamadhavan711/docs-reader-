import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.

SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/documents.readonly",
]


def get_documents_drive():

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("drive", "v3", credentials=creds)

    documents = []
    page_token = None

    while True:

        results = (
            service.files()
            .list(
                q="mimeType='application/vnd.google-apps.document'",
                pageSize=1000,
                pageToken=page_token,
                fields="nextPageToken, files(id,name,modifiedTime)",
            )
            .execute()
        )

        documents.extend(results["files"])

        page_token = results.get("nextPageToken")

        if page_token is None:
            break

    return documents


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """

    creds = None

    # The file token.json stores the user's access and refresh tokens,
    # and is created automatically when the authorization flow completes
    # for the first time.

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available,
    # let the user log in.

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)

            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)
        documents = get_documents_drive()

        for document in documents:
            print("ID:", document["id"])
            print("Name:", document["name"])
            print("Modified:", document["modifiedTime"])
            print()

    except HttpError as error:

        print("An error occurred:", error)


if __name__ == "__main__":
    main()
