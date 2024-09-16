import shutil
import os

def copy_images(source_folder, destination_folder):
    """
    Copy all contents of the source folder to the destination folder for images.

    Args:
        source_folder (str): Path to the folder containing the images.
        destination_folder (str): Path to the folder where images will be copied.
    """
    # Create destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    # Copy all contents of the source folder to the destination folder
    shutil.copytree(source_folder, destination_folder, dirs_exist_ok=True)
    print(f"Images copied from {source_folder} to {destination_folder}")

def copy_labels(source_folder, destination_folder):
    """
    Copy all contents of the source folder to the destination folder for labels.

    Args:
        source_folder (str): Path to the folder containing the labels.
        destination_folder (str): Path to the folder where labels will be copied.
    """
    # Create destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    # Copy all contents of the source folder to the destination folder
    shutil.copytree(source_folder, destination_folder, dirs_exist_ok=True)
    print(f"Labels copied from {source_folder} to {destination_folder}")

# Example usage:
#copy_images('Visua_Data/augmentation_test/images', 'Visua_Data/augmentation_test/aug_images')
#copy_labels('Visua_Data/augmentation_test/labels', 'Visua_Data/augmentation_test/aug_labels')
