import os
from tqdm import tqdm

def get_unique_labels_and_mapping(label_files):
    """
    Get unique labels from YOLO label files and map them if not starting from 0.

    Args:
        label_files (list): List of paths to YOLO label files.

    Returns:
        dict: Mapping of original labels to new labels.
    """
    unique_labels = set()
    
    # Collect unique labels
    for file in label_files:
        with open(file, 'r') as f:
            for line in f:
                class_label = int(line.split()[0])
                unique_labels.add(class_label)
    
    # Sort and create mapping if labels don't start from 0
    sorted_labels = sorted(unique_labels)
    label_mapping = {old_label: new_label for new_label, old_label in enumerate(sorted_labels)}

    return label_mapping

def apply_label_mapping(label_files, label_mapping):
    """
    Apply the label mapping to the YOLO label files and replace them.

    Args:
        label_files (list): List of paths to YOLO label files.
        label_mapping (dict): Mapping of original labels to new labels.

    Returns:
        None
    """
    for file in tqdm(label_files, desc="Processing files"):
        new_lines = []
        with open(file, 'r') as f:
            for line in f:
                parts = line.split()
                original_label = int(parts[0])
                new_label = label_mapping[original_label]
                parts[0] = str(new_label)
                new_lines.append(' '.join(parts))
        
        # Replace the original file with the updated labels
        with open(file, 'w') as f:
            f.write('\n'.join(new_lines) + '\n')

def remap_labels_in_yolo_files(labels_dir):
    """
    Main function to remap labels in YOLO files and replace them in the same directory.

    Args:
        labels_dir (str): Path to the directory containing YOLO label files.

    Returns:
        None
    """
    label_files = [os.path.join(labels_dir, f) for f in os.listdir(labels_dir) if f.endswith('.txt')]
    
    # Get the unique labels and their mapping
    label_mapping = get_unique_labels_and_mapping(label_files)
    
    # Apply the mapping to the label files
    apply_label_mapping(label_files, label_mapping)
    
    print(f"Label remapping completed successfully.")


if __name__ == '__main__':

#Example usage
    labels_dir = 'Datasets/47_logos_dataset/10_classes_final/final/split/train/combined_aug_org/labels'  # Replace with your labels directory path
    remap_labels_in_yolo_files(labels_dir)
