import re
import os
import subprocess

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

        print(f"Extracted Chapter {chapter_number} to {output_file}")
    except Exception as e:
        print(f"Error extracting chapter {chapter_number}: {e}")


def main():
    full_file = "input/full.txt"
    output_file = "input.txt"

    # Ask user for the total number of chapters
    total_chapters = int(input("Enter the total number of chapters to process: "))

    for chapter_number in range(1, total_chapters + 1):
        extract_chapter(full_file, chapter_number, output_file)

        # Run loop.py to process the current chapter
        subprocess.run(["python", "loop.py"])

        # Rename the output video
        output_video = f"chapter{chapter_number}.mp4"
        if os.path.exists("vout.mp4"):
            os.rename("vout.mp4", output_video)
            print(f"Renamed vout.mp4 to {output_video}")
        else:
            print(f"Error: vout.mp4 not found after processing Chapter {chapter_number}")

if __name__ == "__main__":
    main()
