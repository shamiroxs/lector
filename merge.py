import os
import re
from moviepy.editor import VideoFileClip, concatenate_videoclips

def merge_videos(input_dir, output_file):
    # Get a sorted list of all files matching the pattern 'chapterX.mp4' or 'chapterX.Y.mp4'
    chapter_files = sorted(
        [f for f in os.listdir(input_dir) if f.startswith("chapter") and f.endswith(".mp4")],
        key=lambda x: (
            int(re.search(r'chapter(\d+)', x).group(1)),  # Sort by X
            float(re.search(r'chapter(\d+(?:\.\d+)?)', x).group(1))  # Then by X.Y
        )
    )

    # Check if there are any files to process
    if not chapter_files:
        print("No chapters found in the directory.")
        return

    print(f"Found chapters and subchapters: {chapter_files}")

    # Create a list of VideoFileClip objects
    video_clips = []
    for chapter_file in chapter_files:
        full_path = os.path.join(input_dir, chapter_file)
        video_clips.append(VideoFileClip(full_path))
    
    # Concatenate all video clips
    final_clip = concatenate_videoclips(video_clips, method="compose")
    
    # Write the output to the file
    final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")
    
    print(f"Videos merged successfully into {output_file}")

# Define the input directory and output file
input_directory = "./chapters"
output_filename = "./chapters/full_chapter.mp4"

# Merge the videos
merge_videos(input_directory, output_filename)

