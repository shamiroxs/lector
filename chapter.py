import re
import os

# Function to read the full.txt and split it into chapters based on the specified pattern
def extract_chapters(input_file='input/full.txt', skip_chapters=0):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # Regular expression to match "CHAPTER X" headings (e.g., CHAPTER I, CHAPTER II, ...)
    chapter_pattern = r'(CHAPTER [IVXLCDM]+)'  # Roman numeral chapters (e.g., CHAPTER I, CHAPTER II, ...)

    # Find all chapter headings
    chapter_heads = list(re.finditer(chapter_pattern, text))
    
    chapters = []
    start_idx = 0

    # Skip the first 'skip_chapters' occurrences (index page), process from the next chapter heading
    for idx, match in enumerate(chapter_heads[skip_chapters:], start=skip_chapters + 1):
        # For the first chapter (second heading), take everything from the start of the text
        if idx == skip_chapters + 1:
            start_idx = match.end()
        else:
            chapters.append(text[start_idx:match.start()].strip())
            start_idx = match.end()

    # Last chapter: from the last found chapter to *** END OF THE
    end_of_last_chapter = "*** END OF THE"
    end_idx = text.find(end_of_last_chapter)
    
    # Extract last chapter text
    if end_idx != -1:
        last_chapter = text[start_idx:end_idx].strip()
    else:
        # If no "END OF THE" is found, just take the remainder
        last_chapter = text[start_idx:].strip()

    chapters.append(last_chapter)

    return chapters


# Function to extract and write chapters to input.txt
def write_chapter_to_input(chapter_number, chapters):
    # Write the selected chapter to input.txt
    chapter_text = chapters[chapter_number - 1]
    with open('input.txt', 'w', encoding='utf-8') as input_file:
        input_file.write(chapter_text)
    print(f"Chapter {chapter_number} written to input.txt")


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
def process_chapters(skip_chapters):
    chapters = extract_chapters(skip_chapters=skip_chapters)

    # Process each chapter and rename the output video
    for chapter_number in range(1, len(chapters) + 1):
        write_chapter_to_input(chapter_number, chapters)
        execute_loop()
        rename_video(chapter_number)


# Main function to start the process
def main():
    # Ask user for the number of chapters to skip
    try:
        skip_chapters = int(input("Enter the number of chapters to skip (based on CHAPTER headings): "))
        process_chapters(skip_chapters)
    except ValueError:
        print("Invalid input! Please enter an integer for the number of chapters to skip.")


if __name__ == "__main__":
    main()
