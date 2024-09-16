import os
import shutil
from collections import defaultdict
import re
from tqdm import tqdm

def get_video_name(filename):
    """
    Extracts the video name from the filename using regex.

    Args:
        filename (str): The filename to extract the video name from.

    Returns:
        str: The extracted video name if found, otherwise None.
    """
    match = re.match(r'(.+)_\d+', filename) # for 47_&_64 logos dataset
    #match = re.match(r'(.+?)_.*', filename) # for 5_logo_dataset

    return match.group(1) if match else None

def can_add_video_to_set(video, current_counts, target_counts, video_logo_stats):
    """
    Checks if a video can be added to a set (validation or test).

    Args:
        video (str): The video name to check.
        current_counts (dict): The current logo counts in the set.
        target_counts (dict): The target logo counts for the set.

    Returns:
        bool: True if the video can be added to the set, False otherwise.
    """
    for logo, count in video_logo_stats[video].items():
        if current_counts[logo] + count > target_counts[logo]:
            return False
    return True

def copy_files(video, src_image_dir, src_label_dir, dest_image_dir, dest_label_dir):
    """
    Moves image and label files for a given video to their respective directories.

    Args:
        video (str): The video name.
        src_image_dir (str): Source directory for images.
        src_label_dir (str): Source directory for labels.
        dest_image_dir (str): Destination directory for images.
        dest_label_dir (str): Destination directory for labels.
    """
    for filename in os.listdir(src_image_dir):
        if get_video_name(filename) == video:
            src_image_path = os.path.join(src_image_dir, filename)
            label_filename = os.path.splitext(filename)[0] + '.txt'
            src_label_path = os.path.join(src_label_dir, label_filename)
            
            if not os.path.exists(src_label_path):
                continue
            
            dest_image_path = os.path.join(dest_image_dir, filename)
            dest_label_path = os.path.join(dest_label_dir, label_filename)
            
            shutil.copy(src_image_path, dest_image_path)
            shutil.copy(src_label_path, dest_label_path)

def split_dataset(base_dir, image_dir, label_dir, val_percent=20, test_percent=10):
    """
    Splits the dataset into training, validation, and test sets.

    Args:
        base_dir (str): Base directory where the train, valid, and test folders will be created.
        image_dir (str): Path to the images directory.
        label_dir (str): Path to the labels directory.
        val_percent (int): Percentage of data to be used for validation. Default is 20%.
        test_percent (int): Percentage of data to be used for testing. Default is 10%.
    """
    # Count total images and labels before the split
    total_images = len(os.listdir(image_dir))
    total_labels = len(os.listdir(label_dir))

    # Define the directories for training, validation, and test sets
    train_image_dir = os.path.join(base_dir, 'train/images')
    train_label_dir = os.path.join(base_dir, 'train/labels')
    val_image_dir = os.path.join(base_dir, 'valid/images')
    val_label_dir = os.path.join(base_dir, 'valid/labels')
    test_image_dir = os.path.join(base_dir, 'test/images')
    test_label_dir = os.path.join(base_dir, 'test/labels')

    # Create directories for training, validation, and test sets if they don't exist
    os.makedirs(train_image_dir, exist_ok=True)
    os.makedirs(train_label_dir, exist_ok=True)
    os.makedirs(val_image_dir, exist_ok=True)
    os.makedirs(val_label_dir, exist_ok=True)
    os.makedirs(test_image_dir, exist_ok=True)
    os.makedirs(test_label_dir, exist_ok=True)

    # Dictionary to store logo information per video
    video_logo_stats = defaultdict(lambda: defaultdict(int))

    # Process each label file in the label directory
    for label_file in tqdm(os.listdir(label_dir), desc="Processing label files"):
        video_name = get_video_name(label_file)
        #print(video_name)
        if not video_name:
            continue

        label_path = os.path.join(label_dir, label_file)
        with open(label_path, 'r') as f:
            for line in f:
                logo_class = line.split()[0]
                video_logo_stats[video_name][logo_class] += 1

    # Calculate total counts of each logo class across all videos
    total_logo_counts = defaultdict(int)
    for video, logos in video_logo_stats.items():
        for logo, count in logos.items():
            total_logo_counts[logo] += count

    # Determine target validation and test counts for each logo class
    target_validation_counts = {logo: int(val_percent / 100 * count) for logo, count in total_logo_counts.items()}
    target_test_counts = {logo: int(test_percent / 100 * count) for logo, count in total_logo_counts.items()}

    # Initialize counters for validation and test logo counts and sets for validation and test videos
    validation_logo_counts = defaultdict(int)
    test_logo_counts = defaultdict(int)
    validation_videos = set()
    test_videos = set()

    # Select videos to be included in the test set first, then validation set
    for video in tqdm(video_logo_stats, desc="Selecting test videos"):
        if can_add_video_to_set(video, test_logo_counts, target_test_counts, video_logo_stats):
            test_videos.add(video)
            for logo, count in video_logo_stats[video].items():
                test_logo_counts[logo] += count

    for video in tqdm(video_logo_stats, desc="Selecting validation videos"):
        if video not in test_videos and can_add_video_to_set(video, validation_logo_counts, target_validation_counts, video_logo_stats):
            validation_videos.add(video)
            for logo, count in video_logo_stats[video].items():
                validation_logo_counts[logo] += count

    # Move files to training, validation, and test directories based on the selected videos
    for video in tqdm(video_logo_stats, desc="Copying files to respective directories"):
        if video in test_videos:
            copy_files(video, image_dir, label_dir, test_image_dir, test_label_dir)
        elif video in validation_videos:
            copy_files(video, image_dir, label_dir, val_image_dir, val_label_dir)
        else:
            copy_files(video, image_dir, label_dir, train_image_dir, train_label_dir)

    # Print the summary of the split
    train_images = len(os.listdir(train_image_dir))
    train_labels = len(os.listdir(train_label_dir))
    val_images = len(os.listdir(val_image_dir))
    val_labels = len(os.listdir(val_label_dir))
    test_images = len(os.listdir(test_image_dir))
    test_labels = len(os.listdir(test_label_dir))

    print(f"Total images before split: {total_images}")
    print(f"Total labels before split: {total_labels}")
    print(f"Total images in training set: {train_images}")
    print(f"Total labels in training set: {train_labels}")
    print(f"Total images in validation set: {val_images}")
    print(f"Total labels in validation set: {val_labels}")
    print(f"Total images in test set: {test_images}")
    print(f"Total labels in test set: {test_labels}")
    print("Data split and organized into training, validation, and test sets.")

if __name__ == '__main__':
    base_dir = 'Visua_Data/augmentation_test'
    image_dir = 'Visua_Data/augmentation_test/images'
    label_dir = 'Visua_Data/augmentation_test/labels'
    val_percent = 50  # You can change this as needed
    test_percent = 30  # You can change this as needed

    split_dataset(base_dir, image_dir, label_dir, val_percent, test_percent)
