import os
import shutil
from tqdm import tqdm

def copy_images_with_matching_annotations(images_folder, annotations_folder, destination_folder):
    """
    Copy images from the images folder to the destination folder for annotations that have matching labels files.

    Args:
        images_folder (str): Path to the folder containing images.
        annotations_folder (str): Path to the folder containing annotation files.
        destination_folder (str): Path to the desired destination folder for images.
    """
    # Create destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # List image files
    valid_extensions = ('.png', '.jpeg', '.jpg')
    image_files = [f for f in os.listdir(images_folder) if f.lower().endswith(valid_extensions)]

    # Get base names of annotation files
    annotation_base_names = [os.path.splitext(annotation_file)[0] for annotation_file in os.listdir(annotations_folder)]

    # Initialize tqdm progress bar
    progress_bar = tqdm(total=len(image_files), desc="Copying Images", unit="image")

    # Iterate over image files
    for image_file in image_files:
        # Check if image base name matches any annotation base name
        image_base_name, image_extension = os.path.splitext(image_file)
        if image_base_name in annotation_base_names:
            # Copy image file to destination folder
            shutil.copy(os.path.join(images_folder, image_file), destination_folder)
        # Update progress bar
        progress_bar.update(1)

    # Close progress bar
    progress_bar.close()

if __name__ == '__main__':
    # Example usage
    images_folder = '/home/areebadnan/Areeb_code/work/Atheritia/Datasets/47_logos_dataset/64_logos_images/frames'  # Path to folder containing images
    annotations_folder = '/home/areebadnan/Areeb_code/work/Atheritia/Datasets/47_logos_dataset/all labels reviewd (89k)/all labels'  # Path to folder containing annotations
    destination_folder = '/home/areebadnan/Areeb_code/work/Atheritia/Datasets/47_logos_dataset/all labels reviewd (89k)/images'  # Path to desired destination folder for images
    copy_images_with_matching_annotations(images_folder, annotations_folder, destination_folder)