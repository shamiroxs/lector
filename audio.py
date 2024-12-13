from pydub import AudioSegment
import subprocess
import os

def apply_reverb(input_file, output_file):
    """
    Apply a reverb effect to the input file using sox and save as the output file.
    """
    try:
        subprocess.run([
            "sox", input_file, output_file, "reverb", "50", "50", "100", "0.5"
        ], check=True)
        print(f"Reverb applied to {input_file}, saved as {output_file}")
    except Exception as e:
        print(f"Error applying reverb: {e}")


def create_final_audio(audio_file, background_file, output_file):
    try:
        # Apply reverb effect to the background music
        reverb_file = "reverb_background.mp3"
        apply_reverb(background_file, reverb_file)

        # Load audio files
        main_audio = AudioSegment.from_file(audio_file)
        background = AudioSegment.from_file(reverb_file)

        # Loop background music if it's shorter than the main audio
        while len(background) < len(main_audio):
            background += background

        # Trim or fade out the background music to match the main audio length
        background = background[:len(main_audio)].fade_out(3000)  # 3-second fade-out

        # Mix the two audio files
        final_audio = main_audio.overlay(background)

        # Export the final audio
        final_audio.export(output_file, format="mp3")
        print(f"Final audio created: {output_file}")

        # Clean up the reverb file
        if os.path.exists(reverb_file):
            os.remove(reverb_file)

    except Exception as e:
        print(f"Error creating final audio: {e}")


if __name__ == "__main__":
    audio_file = "output.mp3"
    background_file = "./input/background.mp3"
    output_file = "final_output.mp3"
    create_final_audio(audio_file, background_file, output_file)
