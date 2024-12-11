import requests

# Function to read the content of the text file
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to send text to the XTTS server and receive the audio response
def text_to_speech(text):
    url = "http://localhost:5000/synthesize"
    payload = {'text': text}  # Sending the text as form data
    print("Processing ..")
    try:
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            # Save the received audio as an MP3 file
            with open('output.mp3', 'wb') as audio_file:
                audio_file.write(response.content)
            print("Audio file has been saved as 'output.mp3'")
        else:
            print(f"Error: {response.status_code}. Could not generate audio.")
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

# Main function to load the file and send it to XTTS
def main():
    # Automatically use 'ebook.txt' as the file path
    file_path = "input.txt"
    text = read_text_file(file_path)
    
    # Sending the text to the XTTS server
    text_to_speech(text)

if __name__ == "__main__":
    main()
