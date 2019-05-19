from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import io
from apiclient.http import * # changed 
import datetime

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']
MONTHS= dict([(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')])


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
   #driv
    # Call the Drive v3 API
    target = "Heroku Accsessed Log"
    targetFile = target+".txt"
    result = {}
    wasFound = False
    while not wasFound:
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name,mimeType)").execute()
        items = results.get('files', [])
        

        if not items:
            print('No files found.')
            wasFound = True
            print("File Not found")
        else:
            for item in items:
                if item['name'] == target:
                    result = item;
                    wasFound = True
                    break
    print(f"the target file {target} has been found with id {item['id']}, and type {item['mimeType']}.")
    request = service.files().export_media(fileId=item['id'],mimeType='text/plain')
    fh = io.FileIO(targetFile,"wb")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        #print "Download %d%%." % int(status.progress() * 100)
    fh.close()

    print("file Downloaded")
   
    dwnldFile = open(targetFile,"a")
    #dwnldFile.write("Hello")
    dwnldFile.write(f"\nheroku Launched at {str(datetime.datetime.now())}")
    dwnldFile.close()
    media = MediaFileUpload(targetFile,
                        mimetype='application/rtf')
    print(item)
    del item['name']
    del item['mimeType']
    file = service.files().update(fileId = item['id'],media_body = media).execute()
    print("file re-uploaded")





if __name__ == '__main__':
        main()