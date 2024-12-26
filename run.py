import pygame
import os
import shutil
import subprocess
from tkinter import Tk, filedialog
import pyperclip  # Import pyperclip to access clipboard

# Initialize Pygame
pygame.init()

# Window setup
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("File Upload and Submit")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (50, 50, 50)
GREY = (200, 200, 200)
HOVER_COLOR = (100, 100, 100)  # Button hover color

# Fonts
font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)

# Padding
padding_top = 20
padding_left = 50
button_height = 50
button_width = 200
input_box_width = 500
input_box_height = 40

# Create the input folder if not exists
input_folder = './input'
if not os.path.exists(input_folder):
    os.makedirs(input_folder)

# Function to display text
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Function to browse file
def browse_file(file_type):
    try:
        # Define file type filters
        filters = {
            "image": "*.png",
            "music": "*.mp3",
            "ebook": "*.txt"
        }
        # Get the appropriate filter
        file_filter = filters.get(file_type, "*")
        
        # Use kdialog to browse files
        result = subprocess.run(
            ["kdialog", "--getopenfilename", f"{file_filter}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Check if user canceled
        if result.returncode == 0:  # Success
            return result.stdout.strip()  # Return the selected file path
        else:
            return None  # User canceled or error occurred

    except Exception as e:
        print(f"Error during file browsing: {e}")
        return None

# Main function
def main():
    title = ""
    description = ""
    image_file = None
    music_file = None
    ebook_file = None

    active_field = None  # Tracks the active input field ('title' or 'description')

    running = True
    while running:
        screen.fill(BLACK)  # Set the background to black
        
        # Get mouse position for interaction
        mouse_pos = pygame.mouse.get_pos()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle mouse click to switch focus
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if mouse click is inside the title field
                if pygame.Rect(padding_left, padding_top, input_box_width, input_box_height).collidepoint(mouse_pos):
                    active_field = 'title'
                # Check if mouse click is inside the description field
                elif pygame.Rect(padding_left, padding_top + input_box_height + 20, input_box_width, 100).collidepoint(mouse_pos):
                    active_field = 'description'
                else:
                    active_field = None  # Clicked outside, deactivate input fields

            # Handle keyboard input
            if event.type == pygame.KEYDOWN and active_field:
                if event.key == pygame.K_BACKSPACE:
                    if active_field == 'title':
                        title = title[:-1]  # Remove last character from title
                    elif active_field == 'description':
                        description = description[:-1]  # Remove last character from description
                elif event.key == pygame.K_RETURN:
                    pass  # Handle Enter key if needed
                elif event.key == pygame.K_v and (pygame.key.get_mods() & pygame.KMOD_CTRL):  # Check for Ctrl+V (paste)
                    clipboard_content = pyperclip.paste()  # Get clipboard content
                    if active_field == 'title':
                        title += clipboard_content  # Paste into title
                    elif active_field == 'description':
                        description += clipboard_content  # Paste into description
                else:
                    if active_field == 'title' and len(title) < 50:
                        title += event.unicode  # Add character to title
                    elif active_field == 'description' and len(description) < 200:
                        description += event.unicode  # Add character to description

        # Draw text input for title with padding
        pygame.draw.rect(screen, DARK_GREY, pygame.Rect(padding_left, padding_top, input_box_width, input_box_height))
        draw_text("Title: " + title, font, WHITE, screen, padding_left + 10, padding_top + 5)
        
        # Draw text input for description with padding
        description_box_top = padding_top + input_box_height + 20  # Added padding between text fields
        pygame.draw.rect(screen, DARK_GREY, pygame.Rect(padding_left, description_box_top, input_box_width, 100))
        draw_text("Description: " + description, font, WHITE, screen, padding_left + 10, description_box_top + 5)
        
        # Buttons
        image_button = pygame.Rect(padding_left, description_box_top + 120, button_width, button_height)
        music_button = pygame.Rect(padding_left, description_box_top + 190, button_width, button_height)
        ebook_button = pygame.Rect(padding_left, description_box_top + 260, button_width, button_height)
        
        # Right align the submit and resume buttons
        submit_button = pygame.Rect(600 - button_width - padding_left, description_box_top + 400, button_width, button_height)
        resume_button = pygame.Rect(padding_left, description_box_top + 400, button_width, button_height)

        # Draw buttons with hover effect
        if image_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, HOVER_COLOR, image_button)
        else:
            pygame.draw.rect(screen, GREY, image_button)

        if music_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, HOVER_COLOR, music_button)
        else:
            pygame.draw.rect(screen, GREY, music_button)

        if ebook_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, HOVER_COLOR, ebook_button)
        else:
            pygame.draw.rect(screen, GREY, ebook_button)

        # Draw submit and resume buttons
        if submit_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, HOVER_COLOR, submit_button)
        else:
            pygame.draw.rect(screen, DARK_GREY, submit_button)

        if resume_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, HOVER_COLOR, resume_button)
        else:
            pygame.draw.rect(screen, DARK_GREY, resume_button)

        # Button labels
        draw_text("Select Image (.png)", small_font, BLACK, screen, padding_left + 10, description_box_top + 150)
        draw_text("Select Music (.mp3)", small_font, BLACK, screen, padding_left + 10, description_box_top + 220)
        draw_text("Select Ebook (.txt)", small_font, BLACK, screen, padding_left + 10, description_box_top + 290)
        draw_text("Submit", small_font, BLACK, screen, 600 - button_width - padding_left + 10, description_box_top + 410)
        draw_text("Resume", small_font, BLACK, screen, padding_left + 10, description_box_top + 410)

        pygame.display.update()

        # Check for button clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if image_button.collidepoint(event.pos):
                image_file = browse_file("image")
            if music_button.collidepoint(event.pos):
                music_file = browse_file("music")
            if ebook_button.collidepoint(event.pos):
                ebook_file = browse_file("ebook")
            if submit_button.collidepoint(event.pos):
                # Submission logic
                os.makedirs(input_folder, exist_ok=True)

                # Save title and description
                with open(os.path.join(input_folder, 'description.txt'), 'w') as f:
                    f.write(f"{title}\n")
                    f.write(f"{description}")

                # Handle image file
                if image_file:
                    shutil.copy(image_file, os.path.join(input_folder, 'image.png'))
                elif not os.path.exists(os.path.join(input_folder, 'image.png')):
                    print("Image file not provided. Skipping...")
                    image_file = None

                # Handle music file
                if music_file:
                    shutil.copy(music_file, os.path.join(input_folder, 'background.mp3'))
                elif not os.path.exists(os.path.join(input_folder, 'background.mp3')):
                    print("Music file not provided. Skipping...")
                    music_file = None

                # Handle ebook file
                if ebook_file:
                    shutil.copy(ebook_file, os.path.join(input_folder, 'full.txt'))
                elif not os.path.exists(os.path.join(input_folder, 'full.txt')):
                    print("Error: Ebook file not provided. Please upload the ebook file to proceed.")
                    continue  # Wait for ebook input

                # If we reach here, it means all required files are either uploaded or already exist
                # Proceed to run chapter.py
                pygame.quit()
                subprocess.run(['python', 'reset_progress.py'], check=True)
                subprocess.run(['python', 'delete.py'], check=True)
                subprocess.run(['python', 'chapter.py'], check=True)
                print("start merging..")
                subprocess.run(['python', 'merge.py'], check=True)
                subprocess.run(['python', 'details.py'], check=True)

            if resume_button.collidepoint(event.pos):
                # Resume logic, similar to submit but skipping delete.py
                os.makedirs(input_folder, exist_ok=True)

                # Save title and description
                with open(os.path.join(input_folder, 'description.txt'), 'w') as f:
                    f.write(f"{title}\n")
                    f.write(f"{description}")

                # Handle image file
                if image_file:
                    shutil.copy(image_file, os.path.join(input_folder, 'image.png'))
                elif not os.path.exists(os.path.join(input_folder, 'image.png')):
                    print("Image file not provided. Skipping...")
                    image_file = None

                # Handle music file
                if music_file:
                    shutil.copy(music_file, os.path.join(input_folder, 'background.mp3'))
                elif not os.path.exists(os.path.join(input_folder, 'background.mp3')):
                    print("Music file not provided. Skipping...")
                    music_file = None

                # Handle ebook file
                if ebook_file:
                    shutil.copy(ebook_file, os.path.join(input_folder, 'full.txt'))
                elif not os.path.exists(os.path.join(input_folder, 'full.txt')):
                    print("Error: Ebook file not provided. Please upload the ebook file to proceed.")
                    continue  # Wait for ebook input

                # If we reach here, it means all required files are either uploaded or already exist
                # Proceed to run chapter.py
                pygame.quit()
                subprocess.run(['python', 'chapter.py'], check=True)
                print("start merging..")
                subprocess.run(['python', 'merge.py'], check=True)
                subprocess.run(['python', 'details.py'], check=True)
                

# Run the main loop
if __name__ == "__main__":
    main()

