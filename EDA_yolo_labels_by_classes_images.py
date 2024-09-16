import os
import matplotlib.pyplot as plt
from glob import glob
from collections import defaultdict
import matplotlib.cm as cm

def count_bounding_boxes(label_files):
    """
    Count the number of bounding boxes per class from YOLO label files and the number of files each label appears in.

    Args:
        label_files (list): List of paths to YOLO label files.

    Returns:
        tuple: Two dictionaries - one with class IDs as keys and bounding box counts as values,
               and another with class IDs as keys and file counts as values.
    """
    bbox_counts = defaultdict(int)
    file_counts = defaultdict(int)
    
    for label_file in label_files:
        with open(label_file, 'r') as file:
            lines = file.readlines()
            unique_classes_in_file = set()
            for line in lines:
                class_id = line.split()[0]
                bbox_counts[class_id] += 1
                unique_classes_in_file.add(class_id)
            for class_id in unique_classes_in_file:
                file_counts[class_id] += 1
    
    return bbox_counts, file_counts

def plot_bbox_counts(bbox_counts, file_counts, output_path):
    """
    Plot the bounding box counts and file counts as a bar graph in descending order.

    Args:
        bbox_counts (dict): Dictionary with class IDs as keys and bounding box counts as values.
        file_counts (dict): Dictionary with class IDs as keys and file counts as values.
        output_path (str): Path to save the output plot image.

    Returns:
        None
    """
    # Sort the dictionary by values in descending order
    sorted_file_counts = {k: v for k, v in sorted(file_counts.items(), key=lambda item: item[1], reverse=True)}
    
    class_ids = list(sorted_file_counts.keys())
    counts = [file_counts[class_id] for class_id in class_ids]
    instances = [bbox_counts[class_id] for class_id in class_ids]

    plt.figure(figsize=(20, 10))
    bars = plt.bar(class_ids, counts, color=cm.tab20.colors[:len(class_ids)])

    plt.xlabel('Class ID')
    plt.ylabel('File Count')
    plt.title('File Count per Class with Instances on Top')

    # Adding instance count labels on top of each bar
    for bar, instance in zip(bars, instances):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'Instan: {instance}',
                 ha='center', va='bottom', rotation='vertical')

    plt.xticks(rotation=90)
    plt.tight_layout()
    
    # Save the plot as an image
    plt.savefig(output_path)
    print(f"Plot saved as {output_path}")

def process_labels(labels_folder, output_image_path):
    """
    Process YOLO label files to count bounding boxes, file counts, and plot the results.

    Args:
        labels_folder (str): Path to the folder containing YOLO label files.
        output_image_path (str): Path to save the output plot image.

    Returns:
        None
    """
    label_files = glob(os.path.join(labels_folder, '*.txt'))
    bbox_counts, file_counts = count_bounding_boxes(label_files)
    plot_bbox_counts(bbox_counts, file_counts, output_image_path)
    print(f"Successfully completed the process. Find the file at {output_image_path}")

if __name__ == "__main__":
    # Example usage
    labels_folder = 'Datasets/47_logos_dataset/10_classes_final/final/split/train/combined_aug_org/labels'
    output_image_path = 'Datasets/47_logos_dataset/10_classes_final/final/split/train/combined_aug_org/total_images_instances.png'
    process_labels(labels_folder, output_image_path)
