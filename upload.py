from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
import os

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret.json', SCOPES)
    credentials = flow.run_console()
    return build('youtube', 'v3', credentials=credentials)

def upload_video(youtube, file, title, description):
    try:
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': [],
                'categoryId': '22',  # Category: People & Blogs
            },
            'status': {
                'privacyStatus': 'public',
                'embeddable': True,
                'license': 'youtube',
            }
        }

        media = MediaFileUpload(file, chunksize=-1, resumable=True)
        request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )

        response = request.execute()
        print(f"Upload successful! Video ID: {response['id']}")
    except Exception as e:
        print(f"An error occurred during upload: {e}")

def main():
    file = "vout.mp4"
    title = input("Enter the video title: ")
    description = input("Enter the video description: ")

    if not os.path.exists(file):
        print(f"Error: {file} does not exist!")
        return

    youtube = get_authenticated_service()
    upload_video(youtube, file, title, description)

if __name__ == "__main__":
    main()

