from moviepy.editor import *
from moviepy.video.fx import fadein
from PIL import Image
import numpy as np

def create_video_from_audio(image_file='image.png', audio_file='final_output.mp3', output_file='vout.mp4'):
    try:
        # Load the image and reduce opacity
        image = Image.open(image_file).convert("RGBA")
        image = np.array(image)
        image[..., 3] = (image[..., 3] * 0.6).astype(np.uint8)  # Reduce opacity (0.6 is 60% opacity)
        image = Image.fromarray(image, "RGBA")

        # Get the image size
        img_width, img_height = image.size
        
        # Define the target video size (1920x1080)
        video_width, video_height = 1920, 1080
        
        # If the image is smaller than the video resolution, pad it with black
        if img_width < video_width or img_height < video_height:
            # Create a new black image with the target resolution
            new_image = Image.new("RGBA", (video_width, video_height), (0, 0, 0, 255))
            
            # Position the original image in the center
            new_image.paste(image, ((video_width - img_width) // 2, (video_height - img_height) // 2))
            image = new_image
        
        # If the image is larger than the video resolution, resize it to fit within the video frame
        elif img_width > video_width or img_height > video_height:
            image = image.resize((video_width, video_height), Image.ANTIALIAS)

        # Convert the image to an ImageClip for the video
        video_clip = ImageClip(np.array(image)).set_duration(AudioFileClip(audio_file).duration)

        # Load the audio file
        audio_clip = AudioFileClip(audio_file)

        # Set the audio to the video clip
        video_clip = video_clip.set_audio(audio_clip)

        # Optionally add fade-in effect (fade from black to the image)
        video_clip = fadein(video_clip, 2)  # 2 seconds fade-in

        # Write the video file
        video_clip.write_videofile(output_file, fps=24)

        print(f"Video created successfully: {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_video_from_audio()