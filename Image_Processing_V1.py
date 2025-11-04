import os; os.system("cls")
from PIL import Image

count = 57

# Set your folder path
folder_path = r"C:\Users\ronan\OneDrive\Desktop\Science Fair 2025-2026\Image Processor\Unprocessed Images"

# Loop through each file in the folder
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    # Check if it's a file (not a subfolder)
    if os.path.isfile(file_path):

        # Check if it is a png
        if os.path.splitext(file_path)[1].lower() == ".png" or os.path.splitext(file_path)[1].lower() == ".jpeg" or\
                os.path.splitext(file_path)[1].lower() == ".jpg" or os.path.splitext(file_path)[1].lower() == ".heic":

            # Open file to edit.
            with open(file_path, 'r', encoding='utf-8') as file:

                for n in range(4):
                    # Rotates it in intervals of 90 degrees to create more images, decreases image resolution.
                    img = Image.open(f"Unprocessed Images/{filename}")

                    if n == 0: pass
                    elif n == 1: img = img.transpose(Image.ROTATE_90)
                    elif n == 2: img = img.transpose(Image.ROTATE_180)
                    elif n == 3: img = img.transpose(Image.ROTATE_270)
                    img = img.resize((960, 720))

                    # Saves the image to the Processed Images folder
                    img.save(f"Processed Images/{count}.png")
                    count += 1