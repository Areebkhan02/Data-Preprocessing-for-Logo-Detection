import os
from tqdm import tqdm

def delete_specific_files(folder_path, filenames):
    """
    Delete specific files in the specified folder.

    Parameters:
    folder_path (str): The path to the directory.
    filenames (list): A list of filenames to delete.

    Returns:
    None
    """
    for filename in filenames:
        file_path = os.path.join(folder_path, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted {file_path}")

def filter_label_files(labels_folder, classes_to_keep):
    """
    Filter label files in the specified folder, keeping only bounding boxes
    with classes in the provided set.

    Parameters:
    labels_folder (str): The path to the directory containing label files.
    classes_to_keep (set): A set containing the classes to keep.

    Returns:
    None
    """
    # Get the list of files in the labels folder
    label_files = [file for file in os.listdir(labels_folder) if file.endswith('.txt')]

    # Iterate over each file in the labels folder with a progress bar
    for label_file in tqdm(label_files, desc="Processing label files"):
        label_file_path = os.path.join(labels_folder, label_file)
        keep_lines = []

        # Read the label file
        with open(label_file_path, 'r') as file:
            lines = file.readlines()

        # Check each line to see if it contains a bounding box with a class in the classes_to_keep set
        for line in lines:
            # The class is the first number on each line
            class_id = int(line.split()[0])
            if class_id in classes_to_keep:
                keep_lines.append(line)

        # If there are lines to keep, overwrite the file with the filtered content
        if keep_lines:
            with open(label_file_path, 'w') as file:
                file.writelines(keep_lines)
        else:
            # If no lines to keep, delete the file
            os.remove(label_file_path)

def remove_empty_files(folder_path):
    """
    Remove empty text files in the specified folder.

    Parameters:
    folder_path (str): The path to the directory to check for empty files.

    Returns:
    None
    """
    # Get the list of text files in the folder
    text_files = [file for file in os.listdir(folder_path) if file.endswith('.txt')]

    # Iterate over each file to check if it is empty and delete if it is
    for text_file in tqdm(text_files, desc="Removing empty files"):
        file_path = os.path.join(folder_path, text_file)
        
        # Check if the file is empty
        if os.path.getsize(file_path) == 0:
            os.remove(file_path)

# Define the path to the labels folder
# labels_folder_path = 'Atheritia/Datasets/47_logos_dataset/all labels reviewd (89k)/all labels'

# # Define the classes to keep
# classes_to_keep = {17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64}

# # Define the specific files to delete
# files_to_delete = ['classes.txt', 'class.txt']

# # Step 1: Delete specific files
# delete_specific_files(labels_folder_path, files_to_delete)

# # Step 2: Filter label files
# filter_label_files(labels_folder_path, classes_to_keep)

# # Step 3: Remove empty files
# remove_empty_files(labels_folder_path)
