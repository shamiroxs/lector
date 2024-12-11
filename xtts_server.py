from flask import Flask, request, send_file
from gtts import gTTS
import io

app = Flask(__name__)

@app.route('/synthesize', methods=['POST'])
def synthesize_text():
    # Get the text from the POST request
    text = request.form.get('text', '')
    
    if not text:
        return {"error": "No text provided"}, 400
    
    # Generate TTS audio
    tts = gTTS(text=text, lang='en')
    audio = io.BytesIO()
    tts.write_to_fp(audio)
    audio.seek(0)  # Rewind the BytesIO object
    
    # Return the audio as an mp3 file
    return send_file(audio, mimetype='audio/mpeg', as_attachment=True, download_name='output.mp3')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
