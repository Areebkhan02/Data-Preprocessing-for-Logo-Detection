import os
import pandas as pd

# Folder containing logo files
logos_folder = '10_logos_data/icons'

# Initialize a list to store logo filenames (without extension)
logo_filenames = []

# Iterate through logo files in the folder
for logo_filename in os.listdir(logos_folder):
    if logo_filename.endswith(('.png', '.jpg')):
        # Extract the filename (without extension) 
        logo_id = os.path.splitext(logo_filename)[0]  # .replace(' ', '_')  replace spaces with underscores
        logo_filenames.append(logo_id)

# Create a dictionary that maps filenames to sequential numeric values
logo_mapping = {logo: idx for idx, logo in enumerate(logo_filenames)}

# Create a Pandas DataFrame from the logo mapping dictionary
df = pd.DataFrame({'Brand': list(logo_mapping.keys()), 'ID': list(logo_mapping.values())})

# Specify the output Excel file name
output_excel_file = '10_logos_data/logo_assignment.xlsx'

# Save the DataFrame to an Excel file
df.to_excel(output_excel_file, index=False)

print(f"Logo assignments saved to '{output_excel_file}'")
