import os
import pandas as pd
from collections import defaultdict

def analyze_labels(labels_folder):
    """
    Analyzes the YOLO format label files in the given folder to identify unique labels and their occurrences 
    in other text files.

    Args:
        labels_folder (str): Path to the folder containing the YOLO format label files.
    
    Returns:
        pd.DataFrame: A DataFrame with two columns: 'label' and 'file_name' for unique labels.
    """
    # Initialize data structures
    label_to_files = defaultdict(set)
    file_to_labels = {}

    # Iterate over label files and extract labels
    for label_file in os.listdir(labels_folder):
        if label_file.endswith(".txt"):
            file_path = os.path.join(labels_folder, label_file)
            with open(file_path, 'r') as file:
                labels = set()
                for line in file:
                    parts = line.strip().split()
                    if parts:
                        labels.add(parts[0])
                file_to_labels[label_file] = labels
                for label in labels:
                    label_to_files[label].add(label_file)

    # Initialize a list to hold the unique labels and file names
    unique_data = []

    # Analyze labels
    for label, files in label_to_files.items():
        # Identify files where the label is unique
        unique_files = [f for f in files if len(file_to_labels[f]) == 1]
        
        # Add unique labels and file names to the list
        for file_name in unique_files:
            unique_data.append({'label': label, 'file_name': file_name})

    # Convert the results to a DataFrame
    df_unique = pd.DataFrame(unique_data)

    return df_unique

def main():
    labels_folder = "Datasets/47_logos_dataset/10_classes_final/labels"  # Update with your path
    df_unique = analyze_labels(labels_folder)
    print(df_unique)
    
    # Save DataFrame to Excel
    output_excel = "Datasets/47_logos_dataset/10_classes_final/unique_labels_and_files.xlsx"  # Update with your desired output path
    df_unique.to_excel(output_excel, index=False)
    print(f"Unique labels and their corresponding text files have been saved to {output_excel}")

if __name__ == "__main__":
    main()
