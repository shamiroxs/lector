from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
import os

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Token file where credentials will be saved
CREDENTIALS_FILE = 'token.json'

def get_authenticated_service():
    credentials = None
    # If there are credentials already stored, load them
    if os.path.exists(CREDENTIALS_FILE):
        credentials = Credentials.from_authorized_user_file(CREDENTIALS_FILE, SCOPES)

    # If there are no valid credentials available, prompt the user to log in
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            credentials = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(CREDENTIALS_FILE, 'w') as token:
            token.write(credentials.to_json())

    # Build the YouTube API client with the credentials
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
                'privacyStatus': 'private',  # Change this to 'private' for uploading as private
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

def read_title_and_description(file_path):
    """Reads the title and description from the given file."""
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist!")
        return None, None

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    if len(lines) == 0:
        print("Error: The description.txt file is empty!")
        return None, None

    title = lines[0].strip()  # First line is the title
    description = ''.join(lines[1:]).strip()  # Remaining lines are the description

    return title, description

def main():
    file = "vout.mp4"  # Video file path
    description_file = "./input/description.txt"  # File containing the title and description

    title, description = read_title_and_description(description_file)

    if not title or not description:
        return  # Exit if title or description is missing

    if not os.path.exists(file):
        print(f"Error: {file} does not exist!")
        return

    youtube = get_authenticated_service()
    upload_video(youtube, file, title, description)

if __name__ == "__main__":
    main()

