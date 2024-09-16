import os
from tqdm import tqdm

def remove_extra_images(image_folder, annotation_folder):
    """
    Remove extra image files that do not have corresponding annotation files.

    Args:
        image_folder (str): Path to the folder containing image files.
        annotation_folder (str): Path to the folder containing annotation files.
    """
    # Get list of image and annotation files
    image_files = os.listdir(image_folder)
    annotation_files = os.listdir(annotation_folder)

    # Extract the filenames without extensions
    image_names = {os.path.splitext(file)[0] for file in image_files if file.lower().endswith(('.png', '.jpg', '.jpeg'))}
    annotation_names = {os.path.splitext(file)[0] for file in annotation_files if file.lower().endswith('.txt')}

    # Find extra image files
    extra_images = image_names - annotation_names

    # Remove extra image files with tqdm progress bar
    with tqdm(total=len(extra_images), desc="Removing extra images") as pbar:
        for image in extra_images:
            for ext in ('.png', '.jpg', '.jpeg'):
                image_path = os.path.join(image_folder, image + ext)
                if os.path.exists(image_path):
                    os.remove(image_path)
                    # Update progress bar
                    pbar.update(1)
                    pbar.set_postfix({"File removed": image + ext})

# Example usage
# image_folder = 'Atheritia/Datasets/47_logos_dataset/all labels reviewd (89k)/images'
# annotation_folder = 'Atheritia/Datasets/47_logos_dataset/all labels reviewd (89k)/all labels'
# remove_extra_images(image_folder, annotation_folder)
