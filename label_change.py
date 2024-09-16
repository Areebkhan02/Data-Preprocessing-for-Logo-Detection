import os

# Define the class name mapping
class_name_mapping = {21:0, 24:1, 29:2, 30:3, 35:4, 36:5, 38:6, 40:7, 44:8, 54:9}
print(class_name_mapping)

def update_class_names_in_file(file_path, mapping):
    """
    Update class names in a text file based on the provided mapping.

    Args:
        file_path (str): Path to the text file.
        mapping (dict): Dictionary mapping old class names to new class names.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) > 0:
            class_name = int(parts[0])
            if class_name in mapping:
                parts[0] = str(mapping[class_name])
            updated_lines.append(' '.join(parts) + '\n')

    with open(file_path, 'w') as file:
        file.writelines(updated_lines)

def process_labels_folder(folder_path, mapping):
    """
    Process all text files in the specified folder and update class names.

    Args:
        folder_path (str): Path to the folder containing text files.
        mapping (dict): Dictionary mapping old class names to new class names.
    """
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            update_class_names_in_file(file_path, mapping)
            print(f"Updated class names in {file_name}")

if __name__ == "__main__":
    # Replace 'path_to_labels_folder' with the actual path to the labels folder
    labels_folder_path = '/home/areebadnan/Areeb_code/work/Atheritia/Datasets/47_logos_dataset/10_classes_final/final/split/test/labels'
    process_labels_folder(labels_folder_path, class_name_mapping)
    print("All files processed successfully.")
