from pydub import AudioSegment

def add_background_music(speech_file='output.mp3', music_file='./input/background.mp3', output_file='final_output.mp3'):
    try:
        # Load the audio files
        speech = AudioSegment.from_file(speech_file)
        background_music = AudioSegment.from_file(music_file)

        # Case 1: Background music is longer than speech
        if len(background_music) > len(speech):
            # Fade out background music at the end
            fade_duration = 5000  # Fade out over 5 seconds
            background_music = background_music[:len(speech)].fade_out(fade_duration)
        
        # Case 2: Speech is longer than background music
        elif len(speech) > len(background_music):
            # Loop the background music to match speech length
            loops_needed = (len(speech) // len(background_music)) + 1
            background_music = background_music * loops_needed
            background_music = background_music[:len(speech)]  # Cut off excess

            # Fade out at the end of the background music
            fade_duration = 5000  # Fade out over 5 seconds
            background_music = background_music.fade_out(fade_duration)

        # Case 3: Both are of the same length (ideal scenario)
        else:
            # Simply overlay with no adjustments
            pass

        # Overlay the speech audio with the background music
        mixed_audio = background_music.overlay(speech)

        # Export the final audio file
        mixed_audio.export(output_file, format="mp3")
        print(f"Final audio saved as {output_file}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    add_background_music()
