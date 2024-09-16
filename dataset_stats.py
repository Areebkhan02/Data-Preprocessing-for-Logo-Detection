import os
from collections import defaultdict
import re
import pandas as pd

def generate_statistics_report(train_label_dir, val_label_dir, summary_output_file, detailed_output_file):
    """
    Generate statistics report for logos in training and validation datasets and save to Excel files.

    Parameters:
    train_label_dir (str): Path to the training label directory.
    val_label_dir (str): Path to the validation label directory.
    summary_output_file (str): Path to the summary output Excel file.
    detailed_output_file (str): Path to the detailed output Excel file.
    """
    def get_video_name(filename):
        """
        Extract the video name from the filename.
        """
        #match = re.match(r'(.+)_\d+', filename) #for 47_64_logos file
        match = re.match(r'(.+?)_.*', filename)  # for 5_logo_dataset
        return match.group(1) if match else None

    def calculate_stats(label_dir):
        """
        Calculate logo statistics for the given label directory.
        """
        video_logo_stats = defaultdict(lambda: defaultdict(int))
        total_logo_counts = defaultdict(int)

        for label_file in os.listdir(label_dir):
            video_name = get_video_name(label_file)
            if not video_name:
                continue

            label_path = os.path.join(label_dir, label_file)
            with open(label_path, 'r') as f:
                for line in f:
                    logo_class = line.split()[0]
                    video_logo_stats[video_name][logo_class] += 1
                    total_logo_counts[logo_class] += 1

        return video_logo_stats, total_logo_counts

    def calculate_percentage(counts, totals):
        """
        Calculate the percentage of total instances.
        """
        return {logo: (count / totals[logo]) * 100 for logo, count in counts.items()}

    def prepare_data_for_main_sheet(total_instances, train_logo_counts, val_logo_counts):
        """
        Prepare data for the main sheet.
        """
        data = {
            'Logo': [],
            'Train Count': [],
            'Validation Count': [],
            'Total Count': [],
            'Train Percentage': [],
            'Validation Percentage': []
        }

        for logo in total_instances.keys():
            data['Logo'].append(logo)
            data['Train Count'].append(train_logo_counts.get(logo, 0))
            data['Validation Count'].append(val_logo_counts.get(logo, 0))
            data['Total Count'].append(total_instances[logo])
            data['Train Percentage'].append(train_percentages.get(logo, 0))
            data['Validation Percentage'].append(val_percentages.get(logo, 0))

        return pd.DataFrame(data)

    def prepare_video_contribution(stats):
        """
        Prepare video contribution data.
        """
        video_data = {
            'Logo': [],
            'Video': [],
            'Count': []
        }
        for video, logos in stats.items():
            for logo, count in logos.items():
                video_data['Logo'].append(logo)
                video_data['Video'].append(video)
                video_data['Count'].append(count)
        return pd.DataFrame(video_data)

    def save_summary_to_excel(df_main, summary_output_file):
        """
        Save summary data to an Excel file.
        """
        df_main.to_excel(summary_output_file, sheet_name='Summary', index=False)
        print(f"Summary statistics saved to {summary_output_file}")

    def save_detailed_to_excel(df_train_videos, df_val_videos, detailed_output_file):
        """
        Save detailed video contribution data to an Excel file.
        """
        with pd.ExcelWriter(detailed_output_file) as writer:
            df_train_videos.to_excel(writer, sheet_name='Train Videos', index=False)
            df_val_videos.to_excel(writer, sheet_name='Validation Videos', index=False)
        print(f"Detailed statistics saved to {detailed_output_file}")

    # Calculate stats for training and validation sets
    train_stats, train_logo_counts = calculate_stats(train_label_dir)
    val_stats, val_logo_counts = calculate_stats(val_label_dir)

    # Calculate total instances for all logos
    total_instances = defaultdict(int)
    for logo, count in train_logo_counts.items():
        total_instances[logo] += count
    for logo, count in val_logo_counts.items():
        total_instances[logo] += count

    # Calculate percentage of total instances in training and validation
    train_percentages = calculate_percentage(train_logo_counts, total_instances)
    val_percentages = calculate_percentage(val_logo_counts, total_instances)

    # Prepare data for the main sheet
    df_main = prepare_data_for_main_sheet(total_instances, train_logo_counts, val_logo_counts)

    # Prepare data for the video contribution sheet
    df_train_videos = prepare_video_contribution(train_stats)
    df_val_videos = prepare_video_contribution(val_stats)

    # Save summary to one Excel file
    save_summary_to_excel(df_main, summary_output_file)

    # Save detailed video contributions to another Excel file
    save_detailed_to_excel(df_train_videos, df_val_videos, detailed_output_file)

    print("The statistics report has been generated.")

# Example usage
if __name__ == "__main__":
    generate_statistics_report(
        train_label_dir='Atheritia/Datasets/47_logos_dataset/final_47_logos_dataset/train/labels',
        val_label_dir='Atheritia/Datasets/47_logos_dataset/final_47_logos_dataset/valid/labels',
        summary_output_file='Atheritia/Datasets/47_logos_dataset/final_47_logos_dataset/logo_summary_stats.xlsx',
        detailed_output_file='Atheritia/Datasets/47_logos_dataset/final_47_logos_dataset/logo_detailed_stats.xlsx'
    )
