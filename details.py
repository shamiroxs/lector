import os
from moviepy.editor import VideoFileClip

def seconds_to_hms(seconds):
    """Convert seconds to hours:minutes:seconds format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def generate_chapter_details(input_dir, output_file):
    # Get a sorted list of all files matching the pattern 'chapterX.mp4'
    chapter_files = sorted(
        [f for f in os.listdir(input_dir) if f.startswith("chapter") and f.endswith(".mp4")],
        key=lambda x: int(x.replace("chapter", "").replace(".mp4", "")),
    )
    
    # Check if there are any files to process
    if not chapter_files:
        print("No chapters found in the directory.")
        return

    print(f"Found chapters: {chapter_files}")

    # Initialize the starting time and a list to hold chapter details
    start_time = 0
    chapter_details = []

    # Process each chapter file
    for chapter_file in chapter_files:
        full_path = os.path.join(input_dir, chapter_file)
        with VideoFileClip(full_path) as video_clip:
            duration = video_clip.duration  # Get the duration of the video
            start_time_hms = seconds_to_hms(start_time)  # Convert start time to H:M:S format
            chapter_number = chapter_file.replace("chapter", "").replace(".mp4", "")  # Extract chapter number
            chapter_details.append(f"chapter {chapter_number} - {start_time_hms}")
            start_time += duration  # Update the starting time for the next chapter

    # Write the details to a text file
    output_path = os.path.join(input_dir, output_file)
    with open(output_path, "w") as file:
        file.write("\n".join(chapter_details))
    
    print(f"Chapter details saved to {output_path}")

# Define the input directory and output file name
input_directory = "./chapters"
output_filename = "chapter details.txt"

# Generate chapter details
generate_chapter_details(input_directory, output_filename)

