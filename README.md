# Lector

Lector is a Python-based project that transforms text into audio and video formats, providing a unique way to experience ebooks. With Lector, you can process large text files into chapter-wise videos with background music, making it an excellent tool for audiobook and video content creation.

---

## Features

- **Text-to-Audio Conversion**: Converts text from an input file to audio using a text-to-speech (TTS) engine.
- **Audio-to-Video Creation**: Combines the generated audio with an image to create a video.
- **Chapter Splitting**: Automatically splits large text files (`full.txt`) into chapters based on headings (`CHAPTER X` format).
- **Background Music**: Adds looping background music to the audio with fade-in and fade-out effects.
- **Video Upload Support**: Integration-ready for uploading videos to YouTube.
- **Customizable Options**: Supports custom input files, background music, and output configurations.

---

## Installation

### Prerequisites
- **Python 3.7 or later**
- **Pip** (Python package manager)
- **ffmpeg** (for audio and video processing)

### Setting Up the Environment
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/lector.git
   cd lector
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # On Windows, use: myenv\Scripts\activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Ensure `ffmpeg` is installed on your system:
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

---

## Usage

### 1. Prepare Input Files
- Place your full text file (e.g., `full.txt`) in the `input/` directory.
- Add a background music file (e.g., `background.mp3`) to the same directory (optional).

### 2. Process Chapters
Run the `chapter.py` script to process each chapter:
```bash
python chapter.py
```
- The script will prompt you to enter the number of chapters to skip (e.g., for the index page).
- Each chapter will be saved as `input.txt`, processed into audio and video, and saved as `chapterX.mp4`.

### 3. Text-to-Audio-Video Workflow
The project follows these steps automatically:
- **Text File Processing (`text.py`)**: Converts the content of `input.txt` into an audio file (`output.mp3`).
- **Audio Processing (`audio.py`)**: Adds background music to the generated audio and saves it as `final_output.mp3`.
- **Video Creation (`video.py`)**: Combines the audio with an image and saves it as `vout.mp4`.

### 4. Customization
- **Image**: Replace the default image (`image.png`) in the project directory to use a custom image.
- **Background Music**: Replace `background.mp3` in the `input/` directory with your preferred background music.

---

## File Structure

```
lector/
│
├── input/
│   ├── full.txt           # Full text file containing the entire book
│   ├── background.mp3     # Background music (optional)
│   └── image.png          # Default image for video
│
├── text.py                # Converts text to audio
├── audio.py               # Adds background music to audio
├── video.py               # Creates video from audio and image
├── chapter.py             # Splits the text into chapters and processes each one
├── loop.py                # Executes text.py, audio.py, and video.py in sequence
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── .gitignore             # Ignored files
```

---

## Future Features

- **YouTube Upload**: Automate the upload of generated videos to YouTube.
- **Enhanced Chapter Detection**: Support more diverse formats for chapter headings.
- **Multilingual Support**: Extend TTS support for multiple languages.

---

## Contributing

Contributions are welcome! To contribute:
1. Fork this repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push the branch:
   ```bash
   git push origin feature-name
   ```
4. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [gTTS](https://pypi.org/project/gTTS/) for text-to-speech conversion.
- [Pydub](https://pypi.org/project/pydub/) for audio processing.
- [MoviePy](https://zulko.github.io/moviepy/) for video creation.
- Special thanks to the open-source community for their amazing tools and resources.
