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

        pd.DataFrame: A DataFrame with two columns: 'unique' and 'others'.
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

    # Initialize a dictionary to hold unique and other counts
    unique_labels = defaultdict(lambda: {'unique': 0, 'others': 0})

    # Analyze labels
    for label, files in label_to_files.items():
        # Count occurrences of the label in files where it's the only label
        unique_count = sum(1 for f in files if len(file_to_labels[f]) == 1)
        
        # Count occurrences of the label in files where it's not the only label
        others_count = sum(1 for f in files if len(file_to_labels[f]) > 1)

        # Update unique_labels dictionary
        unique_labels[label]['unique'] = unique_count
        unique_labels[label]['others'] = others_count

    # Convert the results to a DataFrame
    df = pd.DataFrame.from_dict(unique_labels, orient='index').reset_index()
    df.columns = ['label', 'unique', 'others']

    return df

def main():
    labels_folder = "Datasets/3heads_merged_dataset/47_37_logos_dataset/labels"  # Update with your path
    df = analyze_labels(labels_folder)
    print(df)
    
    # Save DataFrame to CSV (Optional)
    # output_csv = "path_to_output_csv_file.csv"  # Update with your path
    # df.to_csv(output_csv, index=False)
    # print(f"Analysis complete. Results saved to {output_csv}")

if __name__ == "__main__":
    main()
