import os
from tqdm import tqdm

def check_duplicate_bboxes(labels_folder):
    """
    Check for label files with exact duplicate bounding boxes (bbox).

    Args:
        labels_folder (str): Path to the folder containing label files.

    Returns:
        dict: Dictionary with filenames as keys and lists of duplicate bbox indices as values.
    """
    duplicate_bboxes = {}
    label_files = os.listdir(labels_folder)
    for label_file in tqdm(label_files, desc="Checking duplicate bboxes"):
        bbox_set = set()
        duplicates = []
        with open(os.path.join(labels_folder, label_file), "r") as file:
            for i, line in enumerate(file):
                parts = line.strip()
                if parts in bbox_set:
                    duplicates.append(i)
                else:
                    bbox_set.add(parts)
        if duplicates:
            duplicate_bboxes[label_file] = duplicates
    return duplicate_bboxes

def delete_duplicate_bboxes(labels_folder, duplicate_bboxes):
    """
    Delete duplicate bounding boxes from label files.

    Args:
        labels_folder (str): Path to the folder containing label files.
        duplicate_bboxes (dict): Dictionary with filenames as keys and lists of duplicate bbox indices as values.
    """
    for label_file, indices in duplicate_bboxes.items():
        with open(os.path.join(labels_folder, label_file), "r") as file:
            lines = file.readlines()
        with open(os.path.join(labels_folder, label_file), "w") as file:
            for i, line in enumerate(lines):
                if i not in indices:
                    file.write(line)

def check_images_with_no_labels(images_folder, labels_folder):
    """
    Check for images without corresponding labels.

    Args:
        images_folder (str): Path to the folder containing image files.
        labels_folder (str): Path to the folder containing label files.

    Returns:
        list: List of image filenames without corresponding label files.
    """
    images_with_no_labels = []
    image_files = os.listdir(images_folder)
    for image_file in tqdm(image_files, desc="Checking images for labels"):
        label_file = os.path.splitext(image_file)[0] + ".txt"
        if not os.path.exists(os.path.join(labels_folder, label_file)):
            images_with_no_labels.append(image_file)
    return images_with_no_labels

def check_labels_with_no_images(images_folder, labels_folder):
    """
    Check for labels without corresponding images.

    Args:
        images_folder (str): Path to the folder containing image files.
        labels_folder (str): Path to the folder containing label files.

    Returns:
        list: List of label filenames without corresponding image files.
    """
    labels_with_no_images = []
    label_files = os.listdir(labels_folder)
    for label_file in tqdm(label_files, desc="Checking labels for images"):
        image_file_jpg = os.path.splitext(label_file)[0] + ".jpg"
        image_file_png = os.path.splitext(label_file)[0] + ".png"
        image_file_jpeg = os.path.splitext(label_file)[0] + ".jpeg"
        if not (os.path.exists(os.path.join(images_folder, image_file_jpg)) or
                os.path.exists(os.path.join(images_folder, image_file_png)) or
                os.path.exists(os.path.join(images_folder, image_file_jpeg))):
            labels_with_no_images.append(label_file)
    return labels_with_no_images

def check_non_yolo_format_labels(labels_folder):
    """
    Check for non-YOLO format label files.

    Args:
        labels_folder (str): Path to the folder containing label files.

    Returns:
        list: List of label filenames that are not in YOLO format.
    """
    non_yolo_format_labels = []
    label_files = os.listdir(labels_folder)
    for label_file in tqdm(label_files, desc="Checking YOLO format"):
        with open(os.path.join(labels_folder, label_file), "r") as file:
            for line in file:
                parts = line.split()
                if len(parts) != 5:
                    non_yolo_format_labels.append(label_file)
                    break  # Exit early since the file is already marked non-YOLO format
    return non_yolo_format_labels

def check_labels_without_detections(labels_folder):
    """
    Check for label files without detections.

    Args:
        labels_folder (str): Path to the folder containing label files.

    Returns:
        list: List of label filenames without any detections.
    """
    labels_without_detection = []
    label_files = os.listdir(labels_folder)
    for label_file in tqdm(label_files, desc="Checking labels for detections"):
        with open(os.path.join(labels_folder, label_file), "r") as file:
            contains_detection = False
            for line in file:
                parts = line.split()
                if len(parts) == 5:
                    contains_detection = True
                    break
            if not contains_detection:
                labels_without_detection.append(label_file)
    return labels_without_detection

def check_incorrect_class_labels(labels_folder, valid_classes):
    """
    Check for label files with incorrect class indices.

    Args:
        labels_folder (str): Path to the folder containing label files.
        valid_classes (set): Set of valid class indices.

    Returns:
        list: List of label filenames with incorrect class indices.
    """
    incorrect_class_labels = []
    label_files = os.listdir(labels_folder)
    for label_file in tqdm(label_files, desc="Checking class labels"):
        with open(os.path.join(labels_folder, label_file), "r") as file:
            for line in file:
                parts = line.split()
                if len(parts) == 5:
                    class_index = int(parts[0])
                    if class_index not in valid_classes:
                        incorrect_class_labels.append(label_file)
                        break
    return incorrect_class_labels

def prompt_deletion(file_list, file_type, delete_func=None, folder_path=None, labels_folder=None):
    """
    Prompt the user to delete files and perform the deletion if confirmed.

    Args:
        file_list (list or dict): List or dictionary of files to potentially delete.
        file_type (str): Type of files being checked (for display purposes).
        delete_func (function, optional): Function to handle specific deletion logic if needed.
        folder_path (str, optional): Path to the folder containing the files to delete. Needed for images.
        labels_folder (str, optional): Path to the labels folder.
    """
    if not file_list:
        print(f"No {file_type} found.")
        return

    print(f"{len(file_list)} {file_type} found.")
    user_input = input(f"Do you want to delete these {file_type}? (yes/no): ").strip().lower()
    if user_input == 'yes':
        if delete_func:
            delete_func(labels_folder, file_list)
        elif folder_path:
            for file in file_list:
                os.remove(os.path.join(folder_path, file))
        else:
            for file in file_list:
                os.remove(os.path.join(labels_folder, file))
        print(f"{file_type.capitalize()} deleted.")
    else:
        print(f"{file_type.capitalize()} not deleted.")

def run_all_checks(images_folder, labels_folder, valid_classes):
    """
    Run all data validation checks and handle deletions.

    Args:
        images_folder (str): Path to the folder containing image files.
        labels_folder (str): Path to the folder containing label files.
        valid_classes (set): Set of valid class indices.
    """
    # Check for duplicate bounding boxes
    duplicate_bboxes = check_duplicate_bboxes(labels_folder)
    prompt_deletion(duplicate_bboxes, "duplicate bounding boxes", delete_func=delete_duplicate_bboxes, labels_folder=labels_folder)

    # Check for images without corresponding labels
    images_with_no_labels = check_images_with_no_labels(images_folder, labels_folder)
    prompt_deletion(images_with_no_labels, "images without labels", folder_path=images_folder)

    # Check for labels without corresponding images
    labels_with_no_images = check_labels_with_no_images(images_folder, labels_folder)
    prompt_deletion(labels_with_no_images, "labels without images", labels_folder=labels_folder)

    # Check for non-YOLO format label files
    non_yolo_format_labels = check_non_yolo_format_labels(labels_folder)
    prompt_deletion(non_yolo_format_labels, "non-YOLO format labels", labels_folder=labels_folder)

    # Check for label files without detections
    labels_without_detection = check_labels_without_detections(labels_folder)
    prompt_deletion(labels_without_detection, "labels without detections", labels_folder=labels_folder)

    # Check for label files with incorrect class indices
    incorrect_class_labels = check_incorrect_class_labels(labels_folder, valid_classes)
    prompt_deletion(incorrect_class_labels, "incorrect class labels", labels_folder=labels_folder)

    print("The validation on YOLO labels is done.")

# The module can now be imported and used in other scripts without running the main function
if __name__ == "__main__":
    # Example usage
    valid_classes = set(range(0, 47))
    images_folder = "Visua_Data/augmentation_test/images"
    labels_folder = "Visua_Data/augmentation_test/labels"
    run_all_checks(images_folder, labels_folder, valid_classes)
