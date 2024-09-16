import os
import pandas as pd
import random

def delete_files(images_folder, labels_folder, excel_file, class_label, num_images_to_delete):
    """
    Deletes a specified number of images and their corresponding label files based on a class label.

    Args:
        images_folder (str): Path to the folder containing images.
        labels_folder (str): Path to the folder containing YOLO format label files.
        excel_file (str): Path to the Excel file containing unique label information.
        class_label (str): The class label to target for deletion.
        num_images_to_delete (int): The number of images to delete.

    Returns:
        None
    """
    # Load the Excel file
    df = pd.read_excel(excel_file)

    # Filter the DataFrame for the given class label
    filtered_df = df[df['label'] == class_label]

    # Get the list of file names (without extensions) for the given class label
    file_names = filtered_df['file_name'].str.replace('.txt', '').tolist()

    # Shuffle the file names randomly
    random.shuffle(file_names)

    # Select the specified number of files to delete
    files_to_delete = file_names[:num_images_to_delete]

    # Delete the corresponding images and label files
    for file_name in files_to_delete:
        label_path = os.path.join(labels_folder, file_name + '.txt')
        image_path = os.path.join(images_folder, file_name + '.jpg')  # Assuming images are in .jpg format

        if os.path.exists(label_path):
            os.remove(label_path)
            print(f"Deleted label file: {label_path}")
        
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"Deleted image file: {image_path}")

    print(f"Successfully deleted {num_images_to_delete} images and their corresponding label files.")

if __name__ == "__main__":
    # Example usage
    images_folder = 'Datasets/47_logos_dataset/10_classes_final/images'
    labels_folder = 'Datasets/47_logos_dataset/10_classes_final/labels'
    excel_file = 'Datasets/47_logos_dataset/10_classes_final/unique_labels_and_files.xlsx'
    class_label = 36  # Specify the class label you want to target
    num_images_to_delete = 1000  # Specify the number of images to delete

    delete_files(images_folder, labels_folder, excel_file, class_label, num_images_to_delete)
4