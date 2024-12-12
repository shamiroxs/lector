from moviepy.editor import ImageClip, AudioFileClip
from moviepy.video.fx.all import fadein, fadeout  # Import the correct fadein and fadeout functions
from PIL import Image
import numpy as np

def create_video_from_audio(image_file='./input/image.png', audio_file='final_output.mp3', output_file='vout.mp4'):
    try:
        # Load the image and reduce opacity
        image = Image.open(image_file).convert("RGBA")
        image = np.array(image)
        image[..., 3] = (image[..., 3] * 0.6).astype(np.uint8)  # Reduce opacity (0.6 is 60% opacity)
        image = Image.fromarray(image, "RGBA")

        # Set the video resolution to 1920x1080
        video_width, video_height = 1920, 1080
        
        # Resize the image to match the video resolution (1920x1080)
        image = image.resize((video_width, video_height), Image.Resampling.LANCZOS)

        # Convert the image to an ImageClip for the video
        video_clip = ImageClip(np.array(image))
        video_clip = video_clip.set_duration(AudioFileClip(audio_file).duration)
        
        # Load the audio file
        audio_clip = AudioFileClip(audio_file)

        # Set the audio to the video clip
        video_clip = video_clip.set_audio(audio_clip)

        # Add 2 seconds fade-in effect (fade from black to the image)
        video_clip = fadein(video_clip, 2)  # 2 seconds fade-in

        # Add 2 seconds fade-out effect (fade from the image to black)
        video_clip = fadeout(video_clip, 2)  # 2 seconds fade-out at the end of the video

        # Write the video file
        video_clip.write_videofile(output_file, fps=24)

        print(f"Video created successfully: {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_video_from_audio()
