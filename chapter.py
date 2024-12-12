import re
import os
import shutil

# Function to read the full.txt and split it into chapters based on the specified pattern
def extract_chapters(input_file='input/full.txt'):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # Regular expression to match "Chapter X" headings
    chapter_pattern = r'(Chapter \d+)'  # Adjust this regex based on your actual chapter heading pattern

    # Find all chapter headings (we assume they follow "Chapter X" format)
    chapter_heads = re.finditer(chapter_pattern, text)
    
    chapters = []
    start_idx = 0

    # Collecting each chapter between its headings
    for idx, match in enumerate(chapter_heads):
        # For the first chapter, take everything from the start of the file
        if idx == 0:
            start_idx = match.end()
        else:
            chapters.append(text[start_idx:match.start()].strip())
            start_idx = match.end()

    # Last chapter
    last_chapter = text[start_idx:].strip()
    chapters.append(last_chapter)

    return chapters


# Function to extract and write chapters to ebook.txt
def write_chapter_to_ebook(chapter_number, chapters):
    # Write the selected chapter to ebook.txt
    chapter_text = chapters[chapter_number - 1]
    with open('ebook.txt', 'w', encoding='utf-8') as ebook_file:
        ebook_file.write(chapter_text)
    print(f"Chapter {chapter_number} written to ebook.txt")

# Function to execute the loop.py process (text, audio, and video creation)
def execute_loop():
    # Assuming loop.py is the script that processes text to audio and video
    os.system('python3 loop.py')

# Function to rename vout.mp4 after each chapter
def rename_video(chapter_number):
    # Check if the vout.mp4 exists
    if os.path.exists('vout.mp4'):
        new_video_name = f'chapter{chapter_number}.mp4'
        os.rename('vout.mp4', new_video_name)
        print(f"Renamed vout.mp4 to {new_video_name}")
    else:
        print("Error: vout.mp4 not found!")

# Function to process all chapters
def process_chapters():
    chapters = extract_chapters()

    # Process each chapter and rename the output video
    for chapter_number in range(1, len(chapters) + 1):
        write_chapter_to_ebook(chapter_number, chapters)
        execute_loop()
        rename_video(chapter_number)

# Main function to start the process
if __name__ == "__main__":
    process_chapters()
