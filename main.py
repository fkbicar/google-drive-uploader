import base64
import io

from googleapiclient import discovery, http
from httplib2 import Http
from oauth2client import file, client, tools

#Application credentials
SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)

# Construct the resource to connect to Google API
service = discovery.build('drive', 'v3', http=creds.authorize(Http()))

# List drives including shared drives
list_drives = service.drives().list().execute()
print(list_drives)

# List specific drive
list_drives = service.drives().get(driveId='<driveId>').execute()
print(list_drives)

# List folders
folder_list = service.files().list(q="name='<folder name>' and mimeType='application/vnd.google-apps.folder'",
                                corpora='drive',
                                supportsAllDrives=True,
                                includeItemsFromAllDrives=True,
                                driveId='<driveId>',
                                spaces='drive',
                                fields='*',
                                pageSize=1000).execute()
print(folder_list)  

# List folders under a specified parent 
folder_list = service.files().list(q="parents in '<parent_file_id>'",
                                corpora='drive',
                                supportsAllDrives=True,
                                includeItemsFromAllDrives=True,
                                driveId='<driveId>',
                                spaces='drive',
                                fields='files(id, name, parents, teamDriveId, driveId)',
                                pageSize=1000).execute()
print(folder_list)  

# Download files
drive_list = service.files().get_media(fileId='<fileId>')
fh = io.FileIO('<filename>', mode='wb')
downloader = http.MediaIoBaseDownload(fh, drive_list)
done = False
while done is False:
    status, done = downloader.next_chunk()
    print("Download %d%%." % int(status.progress() * 100))

# Upload file
file_metadata = {
'name': '<filename_to_upload>',
'mimeType': '*/*',
'parents':
    [
        '<parentId(s)>'
    ]
}
media = http.MediaFileUpload('<filename_to_upload>',
                        mimetype='*/*',
                        resumable=True)
file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
print ('File ID: ' + file.get('id'))    
