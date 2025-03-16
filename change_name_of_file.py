import os

def rename_images_in_folder(folder_path):
    if not os.path.isdir(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    # Extract folder name and sanitize it
    folder_name = os.path.basename(os.path.normpath(folder_path))
    folder_name = folder_name.replace(',', '_').replace('%', '')  # Replace special characters

    # List of common image extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']

    # Get list of files and sort them
    files = sorted([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])

    for index, filename in enumerate(files):
        old_path = os.path.join(folder_path, filename)
        ext = os.path.splitext(filename)[1].lower()  # Get file extension in lowercase

        if ext in image_extensions:  # Check if the file is an image
            new_name = f"{folder_name}_{index + 1}{ext}"
            new_path = os.path.join(folder_path, new_name)

            os.rename(old_path, new_path)
            print(f"Renamed '{filename}' to '{new_name}'")

# Example usage
folder_path = 'data/frames_with_binary_mask/7,5%'
rename_images_in_folder(folder_path)