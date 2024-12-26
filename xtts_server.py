from flask import Flask, request, send_file
from gtts import gTTS
import io
import os
from pydub import AudioSegment
import time

app = Flask(__name__)
index_file = "index.txt"

def save_index(index):
    """Save the  index to a file."""
    with open(index_file, 'w') as file:
        file.write(str(index))
    print(f" index saved: {index}")

def load_index():
    """Load the  index from a file."""
    if os.path.exists(index_file):
        with open(index_file, 'r') as file:
            return int(file.read().strip())
    return 0


@app.route('/synthesize', methods=['POST'])
def synthesize_text():
    text = request.form.get('text', '')

    if not text:
        return {"error": "No text provided"}, 400

    # Split the text into smaller chunks (e.g., 1000 characters per chunk)
    chunk_size = 5400
    text_chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    # Store audio files here
    audio_files = []
    
    if not os.path.exists(index_file):
        save_index(0)
    
    index = load_index()
    
    for i, chunk in enumerate(text_chunks, start=index):
        try:
            if i % 18 == 0 and i != 0:
                print("suspend for 15 minutes")
                time.sleep(900)
                print("proceeding..")
            # Generate TTS for the current chunk
            tts = gTTS(text=chunk, lang='en')
            audio = io.BytesIO()
            tts.write_to_fp(audio)
            audio.seek(0)

            # Save this audio chunk to a file
            audio_filename = f"audio_{i+1}.mp3"
            with open(audio_filename, 'wb') as f:
                f.write(audio.read())
            audio_files.append(audio_filename)
            save_index(i+1)
        except Exception as e:
            print(f"Error generating audio for chunk {i+1}: {str(e)}")
            i=i-1
            print("suspend for 1 hour")
            time.sleep(3600)
            print("proceeding..")
            continue
            #return {"error": f"Error generating audio for chunk {i+1}: {str(e)}"}, 500
            
            

    # Combine the audio files using pydub
    combined_audio = AudioSegment.empty()
    for audio_file in audio_files:
        audio_chunk = AudioSegment.from_mp3(audio_file)
        combined_audio += audio_chunk

    # Save the combined audio to a file
    combined_audio.export("combined_output.mp3", format="mp3")

    # Clean up individual audio files
    for audio_file in audio_files:
        os.remove(audio_file)
    
    #starting indes to zero
    save_index(0)
    # Return the combined audio file
    return send_file("combined_output.mp3", mimetype='audio/mpeg', as_attachment=True, download_name='output.mp3')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

