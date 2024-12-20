from flask import Flask, request, send_file
from gtts import gTTS
import io
import os
from pydub import AudioSegment

app = Flask(__name__)

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

    for i, chunk in enumerate(text_chunks):
        try:
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
        except Exception as e:
            return {"error": f"Error generating audio for chunk {i+1}: {str(e)}"}, 500

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

    # Return the combined audio file
    return send_file("combined_output.mp3", mimetype='audio/mpeg', as_attachment=True, download_name='output.mp3')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

