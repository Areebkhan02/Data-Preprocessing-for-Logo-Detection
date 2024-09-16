from cleanvision import Imagelab

def find_issues_in_images(data_path, save_path):
    """
    Use CleanVision to find and report issues in images.

    Args:
        data_path (str): Path to the folder containing the image files in your dataset.
        save_path (str): Path where the report should be saved.
    """
    # Initialize Imagelab with the specified data path
    imagelab = Imagelab(data_path=data_path)
    
    # Automatically check for a predefined list of issues within your dataset
    imagelab.find_issues()
    
    # Produce a neat report of the issues found in your dataset
    imagelab.report()
    
    # Save the report to the specified save path
    imagelab.save(save_path)

# Example usage:
# find_issues_in_images(data_path="/path/to/images", save_path="/path/to/save/results")
