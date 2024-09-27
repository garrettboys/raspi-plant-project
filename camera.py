import os
from picamera import PiCamera
from time import sleep
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_google_drive_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/home/rami035/Arduino/cam_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

def upload_file(service, filename, filepath, mimetype):
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath, mimetype=mimetype)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'File ID: {file.get("id")}')

def take_picture(camera, filename):
    camera.start_preview()
    sleep(2)  # Camera warm-up time
    camera.capture(filename)
    camera.stop_preview()
    print(f"Picture taken: {filename}")

def main():
    camera = PiCamera()
    service = get_google_drive_service()

    try:
        while True:
            # Get current time in CDT
            current_time = datetime.now(timezone('America/Chicago'))
            timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"picture_{timestamp}.jpg"

            take_picture(camera, filename)
            upload_file(service, filename, filename, 'image/jpeg')

            # Delete local file after upload
            os.remove(filename)

            # Wait for the next hour
            next_hour = current_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            sleep_time = (next_hour - current_time).total_seconds()
            sleep(sleep_time)

    finally:
        camera.close()

if __name__ == '__main__':
    main()