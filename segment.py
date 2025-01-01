import os
import re
import subprocess
import json
import shutil
from pydub import AudioSegment

# Function to load progress
def load_progress(progress_file="progress.json"):
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as file:
            progress = json.load(file)
        return progress.get("last_completed_chapter", 0)
    return 0

# Function to save progress
def save_progress(chapter_number, progress_file="progress.json"):
    progress = {"last_completed_chapter": chapter_number}
    with open(progress_file, 'w') as file:
        json.dump(progress, file)
    print(f"Progress saved: Chapter {chapter_number}")

# Function to split audio into 2-hour segments
def split_audio(file_path, segment_length=2 * 60 * 60 * 1000):  # 2 hours in milliseconds
    audio = AudioSegment.from_file(file_path)
    total_length = len(audio)
    segments = []
    
    for i in range(0, total_length, segment_length):
        segment = audio[i:i + segment_length]
        segment_file = f"segment{i // segment_length + 1}.mp3"
        segment.export(segment_file, format="mp3")
        segments.append(segment_file)

    return segments

def main():
    input_file = "output.mp3"
    segment_length_ms = 2 * 60 * 60 * 1000  # 2 hours in milliseconds

    # Check if the input file exists
    if not os.path.exists(input_file):
        print(f"Error: {input_file} does not exist.")
        return

    # Check the duration of the input file
    audio = AudioSegment.from_file(input_file)
    total_duration = len(audio)  # Duration in milliseconds

    if total_duration <= segment_length_ms:
        print(f"{input_file} is less than or equal to 2 hours. No splitting required.")
        return

    # Rename the original file to full.mp3
    os.rename(input_file, "full.mp3")
    print("Renamed output.mp3 to full.mp3")

    # Split the audio into 2-hour segments
    segments = split_audio("full.mp3", segment_length=segment_length_ms)
    print(f"Audio split into {len(segments)} segments: {segments}")

    # Load the last completed chapter from progress.json
    last_completed_chapter = load_progress()
    current_chapter_number = last_completed_chapter + 1

    # Process each segment
    for i, segment in enumerate(segments[:-1]):
    
        # Rename the current segment to output.mp3
        os.rename(segment, "output.mp3")
        print(f"Processing segment {i + 1}: Renamed {segment} to output.mp3")

        # Execute audio.py and video.py
        subprocess.run(["python", "audio.py"], check=True)
        subprocess.run(["python", "video.py"], check=True)

        # Rename the resulting vout.mp4 to chapterY.X.mp4
        chapter_file = f"chapter{current_chapter_number -1}.{i + 1}.mp4"
        
        if os.path.exists(f"./chapters/{chapter_file}"):
            os.remove(f"./chapters/{chapter_file}")
            print(f"Deleted existing file: {chapter_file}")
            
        if os.path.exists("vout.mp4"):
            os.rename("vout.mp4", chapter_file)
            shutil.move(chapter_file, "./chapters")
            print(f"Renamed vout.mp4 to {chapter_file} and moved to chapters directory")
        else:
            print(f"Error: vout.mp4 not found after processing segment {i + 1}")

    # Rename the last segment back to output.mp3
    os.rename(segments[-1], "output.mp3")
    print(f"Renamed the last segment {segments[-1]} to output.mp3")

if __name__ == "__main__":
    main()

