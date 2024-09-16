import os
from tqdm import tqdm

def remove_extra_annotations(image_folder, annotation_folder):
    """
    Remove extra annotation files that do not have corresponding image files.

    Args:
        image_folder (str): Path to the folder containing image files.
        annotation_folder (str): Path to the folder containing annotation files.
    """
    # Get list of image and annotation files
    image_files = os.listdir(image_folder)
    annotation_files = os.listdir(annotation_folder)

    # Extract the filenames without extensions
    image_names = {os.path.splitext(file)[0] for file in image_files}
    annotation_names = {os.path.splitext(file)[0] for file in annotation_files}

    # Find extra annotation files
    extra_annotations = annotation_names - image_names

    # Remove extra annotation files with tqdm progress bar
    with tqdm(total=len(extra_annotations), desc="Removing extra annotations") as pbar:
        for annotation in extra_annotations:
            annotation_path = os.path.join(annotation_folder, annotation + '.txt')
            os.remove(annotation_path)
            # Update progress bar
            pbar.update(1)
            pbar.set_postfix({"File removed": annotation + '.txt'})

# Example usage
# image_folder = 'frames'
# annotation_folder = 'annotation_64_classes'
# remove_extra_annotations(image_folder, annotation_folder)
