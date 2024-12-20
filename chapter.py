import re
import os
import subprocess
import shutil
import json

# Declare `total_chapters` as a global variable
total_chapters = 0
progress_file = "progress.json"
total_chapters_file = "total_chapters.txt"

def extract_chapter(full_file, chapter_number, output_file):
    try:
        with open(full_file, 'r') as file:
            content = file.read()

        # Define chapter heading regex
        chapter_regex = re.compile(r"CHAPTER ([IVXLCDM]+)")
        chapters = list(chapter_regex.finditer(content))

        # Validate the chapter number
        if chapter_number > len(chapters):
            raise ValueError(f"Chapter {chapter_number} does not exist in {full_file}")

        start = chapters[chapter_number - 1].start()
        end = chapters[chapter_number].start() if chapter_number < len(chapters) else content.find("*** END OF THE")

        # Extract and save the chapter
        chapter_content = content[start:end].strip()
        with open(output_file, 'w') as output:
            output.write(chapter_content)

        print(f"Extracted Chapter {chapter_number - total_chapters} to {output_file}")
    except Exception as e:
        print(f"Error extracting chapter {chapter_number - total_chapters}: {e}")

def save_progress(chapter_number):
    """Save the last completed chapter to the progress file."""
    progress = {"last_completed_chapter": chapter_number - total_chapters - 1}
    with open(progress_file, 'w') as file:
        json.dump(progress, file)
    print(f"Progress saved: Chapter {chapter_number - total_chapters}")

def load_progress():
    """Load the last completed chapter from the progress file."""
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as file:
            progress = json.load(file)
        return progress.get("last_completed_chapter", 0)
    return 0

def save_total_chapters(total_chapters):
    """Save the total chapters to a file."""
    with open(total_chapters_file, 'w') as file:
        file.write(str(total_chapters))
    print(f"Total chapters saved: {total_chapters}")

def load_total_chapters():
    """Load the total chapters from a file."""
    if os.path.exists(total_chapters_file):
        with open(total_chapters_file, 'r') as file:
            return int(file.read().strip())
    return 0

def main():
    global total_chapters

    full_file = "input/full.txt"
    output_file = "input.txt"

    # Load progress
    last_completed_chapter = load_progress()

    # If last_completed_chapter is 0, ask user for total chapters and save it
    if last_completed_chapter == 0:
        total_chapters = int(input("Enter the total number of chapters to process: "))
        save_total_chapters(total_chapters)
    else:
        total_chapters = load_total_chapters()

    # Determine where to resume
    start_chapter = total_chapters + last_completed_chapter + 1
    print(f"Resuming from Chapter {start_chapter - total_chapters}")

    for chapter_number in range(start_chapter, 2 * total_chapters + 1):
        extract_chapter(full_file, chapter_number, output_file)

        # Run loop.py to process the current chapter
        subprocess.run(["python", "loop.py"], check=True)

        # Rename the output video
        output_video = f"chapter{chapter_number - total_chapters}.mp4"
        destination_path = f"./chapters/{output_video}"

        # Check if the file exists and remove it if necessary
        if os.path.exists(destination_path):
            os.remove(destination_path)
            print(f"Deleted existing file: {destination_path}")

        if os.path.exists("vout.mp4"):
            os.rename("vout.mp4", output_video)
            shutil.move(output_video, "./chapters")
            print(f"Renamed vout.mp4 to {output_video}")

            # Save progress after successful processing
            save_progress(chapter_number)
        else:
            print(f"Error: vout.mp4 not found after processing Chapter {chapter_number - total_chapters}")

if __name__ == "__main__":
    main()

