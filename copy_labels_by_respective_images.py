import os
import shutil
from tqdm import tqdm

def copy_annotations_with_matching_images(images_folder, annotations_folder, destination_folder):
    """
    Copy annotation files from the annotations folder to the destination folder for images that have matching annotation files.

    Args:
        images_folder (str): Path to the folder containing images.
        annotations_folder (str): Path to the folder containing annotation files.
        destination_folder (str): Path to the desired destination folder for annotations.
    """
    # Create destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # List image files
    image_files = os.listdir(images_folder)
    

    # Get base names of image files
    image_base_names = [os.path.splitext(image_file)[0] for image_file in image_files]

    # Initialize tqdm progress bar
    progress_bar = tqdm(total=len(image_files), desc="Copying Annotations", unit="annotation")

    # Iterate over annotation files
    for annotation_file in os.listdir(annotations_folder):
        # Check if annotation base name matches any image base name
        annotation_base_name, annotation_extension = os.path.splitext(annotation_file)
        if annotation_base_name in image_base_names:
            # Copy annotation file to destination folder
            shutil.copy(os.path.join(annotations_folder, annotation_file), destination_folder)
            # Update progress bar
            progress_bar.update(1)

    # Close progress bar
    progress_bar.close()

if __name__ == '__main__':
    # Example usage
    images_folder = '/home/jansher/Athletia/1_logo_detection/dataset/val/images'  # Path to folder containing images
    annotations_folder = '/home/jansher/Athletia/17_logo_detection/iteration_2/ec2_training/dataset/val/labels'  # Path to folder containing annotations
    destination_folder = '/home/jansher/Athletia/1_logo_detection/dataset/val/labels'  # Path to desired destination folder for annotations
    copy_annotations_with_matching_images(images_folder, annotations_folder, destination_folder)
