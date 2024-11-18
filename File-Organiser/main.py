import os
import shutil

# Path to the messy directory
folder_path = "Messy_Folder"

# Step 1: List all files in the folder
files = os.listdir(folder_path)

# Step 2: Categorize files by their extensions
file_types = {}
for file in files:
    if os.path.isfile(os.path.join(folder_path, file)):  # Ensure it's a file
        ext = os.path.splitext(file)[1]  # Get file extension
        if ext not in file_types:
            file_types[ext] = []  # Create a new list for this extension
        file_types[ext].append(file)

# Step 3: Create subfolders for each file type
for ext in file_types:
    folder_name = ext[1:].capitalize() + "s"  # Remove dot and add 's' (e.g., "Jpgs")
    folder_type_path = os.path.join(folder_path, folder_name)
    if not os.path.exists(folder_type_path):
        os.makedirs(folder_type_path)  # Create the folder

# Step 4: Move files into their respective subfolders
for ext, files in file_types.items():
    folder_name = ext[1:].capitalize() + "s"
    folder_type_path = os.path.join(folder_path, folder_name)
    for file in files:
        shutil.move(
            os.path.join(folder_path, file),  # Source file path
            os.path.join(folder_type_path, file)  # Destination path
        )

print("Files have been organized successfully!")
