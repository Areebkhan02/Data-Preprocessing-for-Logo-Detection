import os
from glob import glob

def extract_unique_labels(label_files):
    """
    Extract unique class labels from YOLO format label files.

    Args:
        label_files (list): List of paths to YOLO label files.

    Returns:
        list: Sorted list of unique class labels in ascending order.
    """
    unique_labels = set()

    for label_file in label_files:
        with open(label_file, 'r') as file:
            for line in file:
                class_id = int(line.split()[0])
                unique_labels.add(class_id)

    # Return sorted list of unique class labels in ascending order
    return sorted(unique_labels)

def find_unique_labels(labels_folder):
    """
    Find unique class labels in a folder containing YOLO label files.

    Args:
        labels_folder (str): Path to the folder containing YOLO label files.

    Returns:
        list: Sorted list of unique class labels in ascending order.
    """
    label_files = glob(os.path.join(labels_folder, '*.txt'))
    unique_labels = extract_unique_labels(label_files)
    
    return unique_labels

if __name__ == "__main__":
    # Example usage
    labels_folder = 'Datasets/47_logos_dataset/10_classes_final/final/split/train/combined_aug_org/labels'
    unique_labels = find_unique_labels(labels_folder)
    print(f"Unique labels in ascending order: {unique_labels}")
