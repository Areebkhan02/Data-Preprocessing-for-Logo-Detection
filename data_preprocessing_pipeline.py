"""
Data Preprocessing Pipeline Script

Description:
This script preprocesses a dataset by ensuring that images and annotations are correctly matched,
unwanted classes are removed, and issues in images are detected. It also splits the dataset into 
training, validation, and test sets, validates the YOLO format, generates statistics, performs EDA,
and remaps the class labels to start from zero.

Input Arguments:
- images_folder (str): Path to the folder containing images.
- annotations_folder (str): Path to the folder containing annotation files.
- destination_folder_images (str): Path to the desired destination folder for images.
- destination_folder_labels (str): Path to the desired destination folder for labels.
- base_directory_train_test_valid (str): Path to the base directory for train/valid/test split.
- val_percent (int): Percentage of data to be used for validation.
- test_percent (int): Percentage of data to be used for testing.
- classes_to_keep (set): A set containing the classes to keep.
- files_to_delete (list): A list of filenames to delete.
- save_image_issues_path (str): Path to save the image issues detected by cleanvision.
- summary_output_excel_file (str): Path to save the summary statistics report.
- detailed_output_excel_file (str): Path to save the detailed statistics report.
- train_output_image_path (str): Path to save the EDA bar chart image.

Expected Outcomes:
- Images and labels are correctly matched and saved to the destination folders.
- Unwanted classes are removed, and empty label files are deleted.
- Issues in images are detected and reported.
- Dataset is split into train, validation, and test sets.
- YOLO format is validated, and statistics reports are generated.
- EDA is performed, and class labels are remapped to start from zero.
"""

# Import necessary functions from your scripts
import os
from copy_images_by_respective_labels import copy_images_with_matching_annotations
from copy_labels_by_respective_images import copy_annotations_with_matching_images
from delete_bbox_of_specific_classes import delete_specific_files, filter_label_files, remove_empty_files
from copy_images_labels import copy_images, copy_labels
from delete_extra_images import remove_extra_images
from delete_extra_labels import remove_extra_annotations
from find_issue_in_images import find_issues_in_images  # Import your custom script for cleanvision
from dataset_splitter_in_train_val_test import split_dataset
from yolo_dataset_validation import run_all_checks
from dataset_stats import generate_statistics_report
from EDA_yolo_labels_by_classses_no import process_labels
from unique_labels_replace import remap_labels_in_yolo_files

def preprocess_data(images_folder, annotations_folder, destination_folder_images, destination_folder_labels, base_directory_train_test_valid, val_percent, test_percent, classes_to_keep, files_to_delete, save_image_issues_path, summary_output_excel_file, detailed_output_excel_file, train_output_image_path):
    """
    Preprocess the data by ensuring images and annotations are matched, and unwanted classes are removed.

    Args:
        images_folder (str): Path to the folder containing images.
        annotations_folder (str): Path to the folder containing annotation files.
        destination_folder_images (str): Path to the desired destination folder for images.
        destination_folder_labels (str): Path to the desired destination folder for labels.
        classes_to_keep (set): A set containing the classes to keep.
        files_to_delete (list): A list of filenames to delete.

    
    """

    # Step 1: Ensure the number of images and annotations are the same
    num_images = len(os.listdir(images_folder))
    num_annotations = len(os.listdir(annotations_folder))
    
    if num_images > num_annotations:
        copy_images_with_matching_annotations(images_folder, annotations_folder, destination_folder_images)
        copy_labels(annotations_folder, destination_folder_labels)
    elif num_annotations > num_images:
        copy_annotations_with_matching_images(images_folder, annotations_folder, destination_folder_labels)
        copy_images(images_folder, destination_folder_images)
    
    print("******************** Step 1 Completed: Images and Annotations Matched ********************")

    # Step 2: Remove unwanted classes/labels
    delete_specific_files(destination_folder_labels, files_to_delete)
    filter_label_files(destination_folder_labels, classes_to_keep)
    remove_empty_files(destination_folder_labels)
    print("******************** Step 2 Completed: Unwanted Classes Removed ********************")
    
    # Step 2.1: Ensure the final number of images and annotations are equal
    final_num_images = len(os.listdir(destination_folder_images))
    final_num_annotations = len(os.listdir(destination_folder_labels))
    
    if final_num_images > final_num_annotations:
        remove_extra_images(destination_folder_images, destination_folder_labels)
    elif final_num_annotations > final_num_images:
        remove_extra_annotations(destination_folder_images, destination_folder_labels)

    print("******************** Step 2.1 Completed: Final Check of Images and Annotations ********************")

    # Step 3: Check for issues in images using the script
    #find_issues_in_images(destination_folder_images, save_image_issues_path)
    print("******************** Step 3 Completed: Image Issues Checked ********************")

    # Step 4: Split the dataset into train, test and valid  
    # change the match logic or see this if its correct or not 
    split_dataset(base_directory_train_test_valid, destination_folder_images, destination_folder_labels, val_percent, test_percent)
    print("******************** Step 4 Completed: Dataset Split ********************")

    # Step 5: Validation for the YOLO format script
    train_image_dir = os.path.join(base_directory_train_test_valid, 'train/images')
    train_label_dir = os.path.join(base_directory_train_test_valid, 'train/labels')
    run_all_checks(train_image_dir, train_label_dir, classes_to_keep)

    val_image_dir = os.path.join(base_directory_train_test_valid, 'valid/images')
    val_label_dir = os.path.join(base_directory_train_test_valid, 'valid/labels')
    run_all_checks(val_image_dir, val_label_dir, classes_to_keep)

    test_image_dir = os.path.join(base_directory_train_test_valid, 'test/images')
    test_label_dir = os.path.join(base_directory_train_test_valid, 'test/labels')
    run_all_checks(test_image_dir, test_label_dir, classes_to_keep)

    print("******************** Step 5 Completed: YOLO Format Validated ********************")

    # Step 6: Generate statistics report for the dataset
    # see the match logic as in the splitting part 
    generate_statistics_report(train_label_dir, val_label_dir, summary_output_excel_file, detailed_output_excel_file)
    print("******************** Step 6 Completed: Statistics Report Generated ********************")

    # Step 7: EDA for seeing the number of classes performed on ONLY the training data
    process_labels(train_label_dir, train_output_image_path)
    print("******************** Step 7 Completed: EDA Completed ********************")

    # # Step 8: Map the label files starting from 0 
    # remap_labels_in_yolo_files(train_label_dir)
    # remap_labels_in_yolo_files(val_label_dir)
    # remap_labels_in_yolo_files(test_label_dir)
    # print("******************** Step 8 Completed: Labels Remapped ********************")

if __name__ == '__main__':
    # Define your paths and parameters
    images_folder = 'Datasets/47_logos_dataset/10_classes_final/images'
    annotations_folder = 'Datasets/47_logos_dataset/10_classes_final/labels'
    destination_folder_images = 'Datasets/47_logos_dataset/10_classes_final/final/images'
    destination_folder_labels = 'Datasets/47_logos_dataset/10_classes_final/final/labels'
    save_image_issues_path = 'Datasets/47_logos_dataset/10_classes_final/final'
    base_directory_train_test_valid = 'Datasets/47_logos_dataset/10_classes_final/final/split'
    val_percent = 10  # You can change this as needed
    test_percent = 10  # You can change this as needed
    classes_to_keep = {36,29,24,40,35,44,38,21,54,30}
    files_to_delete = ['classes.txt', 'class.txt']
    summary_output_excel_file = 'Datasets/47_logos_dataset/10_classes_final/final/summary.xlsx'  # Make sure to include file name with xlsx extension
    detailed_output_excel_file = 'Datasets/47_logos_dataset/10_classes_final/final/detailed.xlsx'  # Make sure to include file name with xlsx extension
    train_output_image_path = 'Datasets/47_logos_dataset/10_classes_final/split/final/bbox_train.png'  # Make sure you specify the file name with png format 

    # Run the preprocessing pipeline
    preprocess_data(images_folder, annotations_folder, destination_folder_images, destination_folder_labels, base_directory_train_test_valid, val_percent, test_percent, classes_to_keep, files_to_delete, save_image_issues_path, summary_output_excel_file, detailed_output_excel_file, train_output_image_path)
