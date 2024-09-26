# ============== without using threads to process videos and images =================

import os
import json
import cv2
import pandas as pd
from tqdm import tqdm


# Define the folder paths
video_folder = '/home/areebadnan/Areeb_code/work/Visua_Data/videos/videos_test'
image_folder = '/home/areebadnan/Areeb_code/work/Visua_Data/videos/images_test'

# Create the annotation folder if it doesn't exist
annotation_folder = '/home/areebadnan/Areeb_code/work/Atheritia/Scripts/Data-Preprocessing-for-Logo-Detection/visua_annotations/annotation_folder'


json_folder = '/home/areebadnan/Areeb_code/work/Atheritia/Scripts/Data-Preprocessing-for-Logo-Detection/visua_annotations/jsons'

# Dictionary to store the logo to class mapping
logo_to_class_mapping = {}

skip_intervals = [2, 3, 4, 5, 6] # Skip every 2nd, 3rd, 4th, 5th, and 6th frame
logo_ids = ['210608','32409']

# skip_intervals = [i for i in range(1, 6)]

# Function to convert time to frame number
def time_to_frame(time, fps):
    return int(time * fps)

def convert_to_yolo(annotation, image_width, image_height, class_id=0):
    # Extract 4-point annotation coordinates
    x1, y1, x2, y2, x3, y3, x4, y4 = annotation

    # Calculate the minimum and maximum x and y coordinates
    min_x = min(x1, x2, x3, x4)
    max_x = max(x1, x2, x3, x4)
    min_y = min(y1, y2, y3, y4)
    max_y = max(y1, y2, y3, y4)

    # Calculate the center coordinates of the bounding box
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2

    # Calculate the width and height of the bounding box
    width = max_x - min_x
    height = max_y - min_y

    # Normalize coordinates and dimensions to be between 0 and 1
    center_x = max(0, min(center_x / image_width, 1))
    center_y = max(0, min(center_y / image_height, 1))
    width = max(0, min(width / image_width, 1))
    height = max(0, min(height / image_height, 1))

    # Format the result as YOLO-style annotation
    yolo_annotation = f"{class_id} {center_x:.6f} {center_y:.6f} {width:.6f} {height:.6f}\n"
    return yolo_annotation

def process_video(video_file, json_data):
    # print(f"Processing video {video_file}\n")
    video_path = os.path.join(video_folder, video_file)
    video_capture = cv2.VideoCapture(video_path)

    if not video_capture.isOpened():
        print(f"Error: Could not open video file: {video_path}")
        return

    fps = video_capture.get(cv2.CAP_PROP_FPS)
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT)) # Get the total number of frames
    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video_name = video_file.split('.')[0]

    print('Total Frames:', total_frames)
    cout_bbox = 0

    for json_file in json_data:
        data = json_data[json_file]
        for idx, item in enumerate(data):
            medium = item.get('medium')
            start_time = item.get("start")
            end_time = item.get("end")
            logo_part1 = item.get('brandName')
            logo_part2 = str(item.get('logoId'))
            logo = logo_part1 + "_" + logo_part2

            if logo_part2 in logo_ids:
            
                if video_name == medium:
                    start_frame = time_to_frame(start_time, fps)
                    end_frame = time_to_frame(end_time, fps)
                    coordinates = item.get("coordinates")
                    cout_bbox += len(coordinates)

                    # Assign a unique class number if the logo hasn't been encountered yet
                    if logo not in logo_to_class_mapping:
                        logo_to_class_mapping[logo] = len(logo_to_class_mapping)

                    class_id = logo_to_class_mapping[logo]

                    for frame_number in range(start_frame, end_frame):


                        #             # Check if the current frame number should be skipped
                        # skip = any(frame_number % interval == 0 for interval in skip_intervals)

                        # if skip:
                        #     continue  # Skip this frame

                        # # Skip every 5th frame (you can customize the condition as needed)
                        # if frame_number % 2 == 0:
                        #     continue  # Skip this frame

                        annotation_filename = f"{video_name}_{frame_number}.txt"
                        annotation_filepath = os.path.join(annotation_folder, annotation_filename)
                        yolo_coordinates = convert_to_yolo(coordinates[frame_number - start_frame], width, height, class_id)
                        with open(annotation_filepath, 'a') as annotation_file:
                            annotation_file.write(yolo_coordinates)

    print("Video processing finished")
    print('Total Bounding Boxes:', cout_bbox)

# def process_image(image_file, json_data):
#     print(f"Processing image {image_file}\n")
#     image_path = os.path.join(image_folder, image_file)
#     image = cv2.imread(image_path)
#     height, width, _ = image.shape
#     image_name = image_file.split('.')[0]
    
#     for json_file in json_data:
#         data = json_data[json_file]
#         for idx, item in enumerate(data):
#             medium = item.get('medium')
#             logo = item.get('brandName')

#             if medium == image_name:
#                 coordinates = item.get("coordinates")

#                 # Assign a unique class number if the logo hasn't been encountered yet
#                 if logo not in logo_to_class_mapping:
#                     logo_to_class_mapping[logo] = len(logo_to_class_mapping)

#                 class_id = logo_to_class_mapping[logo]

#                 yolo_coordinates = convert_to_yolo(coordinates[0], width, height, class_id)
#                 annotation_filename = f"{image_name}.txt"
#                 annotation_filepath = os.path.join(annotation_folder, annotation_filename)
                
#                 with open(annotation_filepath, 'a') as annotation_file:
#                     annotation_file.write(yolo_coordinates)

#     print("Image processing finished")

# Create the annotation folder if it doesn't exist
os.makedirs(annotation_folder, exist_ok=True)

# Get a list of video and image files
video_files = [video_file for video_file in os.listdir(video_folder) if video_file.endswith('.mp4')]
# image_files = [image_file for image_file in os.listdir(image_folder) if image_file.endswith(('.jpg', '.png'))]

# Load JSON data for all videos into a dictionary
json_data = {}
for json_file in os.listdir(json_folder):
    with open(os.path.join(json_folder, json_file), 'r') as file:
        data = json.load(file)
        json_data[json_file] = data

# Process video files with tqdm progress bar
print("Processing video files...")
for video_file in tqdm(video_files, desc="Videos", unit="video"):
    process_video(video_file, json_data)

print("Video annotations generated successfully.")

# Process image files with tqdm progress bar
# print("Processing image files...")
# for image_file in tqdm(image_files, desc="Images", unit="image"):
#     process_image(image_file, json_data)

# print("Image annotations generated successfully.")

# Save the logo to class mapping to a JSON file
mapping_file = 'logo_to_class_mapping.json'
with open(mapping_file, 'w') as file:
    json.dump(logo_to_class_mapping, file, indent=4)
print(f"Logo to class mapping saved to {mapping_file}.")




#================== using threads to process videos and images ===================

# import os
# import json
# import cv2
# import concurrent.futures
# import threading

# # Function to convert time to frame number
# def time_to_frame(time, fps):
#     return int(time * fps)

# def convert_to_yolo(annotation, image_width, image_height, class_id=0):
#     # Extract 4-point annotation coordinates
#     x1, y1, x2, y2, x3, y3, x4, y4 = annotation

#     # Calculate the minimum and maximum x and y coordinates
#     min_x = min(x1, x2, x3, x4)
#     max_x = max(x1, x2, x3, x4)
#     min_y = min(y1, y2, y3, y4)
#     max_y = max(y1, y2, y3, y4)

#     # Calculate the center coordinates of the bounding box
#     center_x = (min_x + max_x) / 2
#     center_y = (min_y + max_y) / 2

#     # Calculate the width and height of the bounding box
#     width = max_x - min_x
#     height = max_y - min_y

#     # Normalize coordinates and dimensions to be between 0 and 1
#     center_x = max(0, min(center_x / image_width, 1))
#     center_y = max(0, min(center_y / image_height, 1))
#     width = max(0, min(width / image_width, 1))
#     height = max(0, min(height / image_height, 1))

#     # Format the result as YOLO-style annotation
#     yolo_annotation = f"{class_id} {center_x:.6f} {center_y:.6f} {width:.6f} {height:.6f}\n"
#     return yolo_annotation

# # Define the folder paths
# video_folder = '10_logos_data/videos'
# image_folder = '10_logos_data/images'
# annotation_folder = '10_logos_data/annotation_with_classes'
# json_folder = 'json_files(batch_1)'

# video_processing_count = 0
# image_processing_count = 0
# count_lock = threading.Lock()
# import pandas as pd

# # Specify the path to the Excel file
# excel_file = '10_logos_data/logo_assignment.xlsx'

# # Read the Excel file into a Pandas DataFrame
# df = pd.read_excel(excel_file)

# # Create a dictionary that maps logos to their corresponding numeric values
# logo_to_mapping = {row['Brand']: row['ID'] for _, row in df.iterrows()}

# print(logo_to_mapping)

# def process_video_thread(video_file, json_data):
#     global video_processing_count
#     with count_lock:
#         video_processing_count += 1
#     print(f"Started Thread {video_processing_count} {video_file}\n")
#     video_path = os.path.join(video_folder, video_file)
#     video_capture = cv2.VideoCapture(video_path)

#     if not video_capture.isOpened():
#         print(f"Error: Could not open video file: {video_path}")
#         return

#     fps = video_capture.get(cv2.CAP_PROP_FPS)
#     width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     video_name = video_file.split('.')[0]

#     for json_file in json_data:
#         data = json_data[json_file]
#         for idx, item in enumerate(data):
#             medium = item.get('medium')
#             start_time = item.get("start")
#             duration = item.get("duration")
#             end_time = item.get("end")
#             logo = item.get('brandName')
            
#             if video_name == medium:
#                 start_frame = time_to_frame(start_time, fps)
#                 end_frame = time_to_frame(end_time, fps)
#                 coordinates = item.get("coordinates")
#                 #print(f"MEDIUM: {medium}, FPS: {fps}, Number of Coordinates: {len(coordinates)}, Start Frame: {start_frame}, End Frame: {end_frame}, Duration: {duration}")

#                 for frame_number in range(start_frame, end_frame):
#                     annotation_filename = f"{video_name}_{frame_number}.txt"
#                     annotation_filepath = os.path.join(annotation_folder, annotation_filename)
#                     if logo in logo_to_mapping:
#                         yolo_coordinates = convert_to_yolo(coordinates[frame_number - start_frame], width, height, logo_to_mapping[logo])
#                         with open(annotation_filepath, 'a') as annotation_file:
#                             annotation_file.write(yolo_coordinates)
#                     # else:
#                     #     print(f"Warning: Logo '{logo}' not found in logo_to_mapping dictionary.")
#     print("Thread Finished")

# def process_image_thread(image_file, json_data):
#     global image_processing_count
#     with count_lock:
#         image_processing_count += 1
#     print(f"Started Thread {image_processing_count} {image_file}\n")
#     image_path = os.path.join(image_folder, image_file)
#     image = cv2.imread(image_path)
#     height, width, _ = image.shape
#     image_name = image_file.split('.')[0]
#     count = 0
#     for json_file in json_data:
#         data = json_data[json_file]
#         for idx, item in enumerate(data):
#             medium = item.get('medium')
#             logo = item.get('brandName')

#             if medium == image_name:
#                 count+=1
#                 print(count)
#                 coordinates = item.get("coordinates")
#                 if logo in logo_to_mapping:
#                     yolo_coordinates = convert_to_yolo(coordinates[0], width, height,  logo_to_mapping[logo])
#                     annotation_filename = f"{image_name}.txt"
#                     annotation_filepath = os.path.join(annotation_folder, annotation_filename)
                
#                     with open(annotation_filepath, 'a') as annotation_file:
#                         annotation_file.write(yolo_coordinates)

#     print("Thread Finished")
# # Create the annotation folder if it doesn't exist
# os.makedirs(annotation_folder, exist_ok=True)

# # Get a list of video files
# video_files = [video_file for video_file in os.listdir(video_folder) if video_file.endswith('.mp4')]
# image_files = [image_file for image_file in os.listdir(image_folder) if image_file.endswith(('.jpg', '.png'))]
# # Load JSON data for all videos into a dictionary
# json_data = {}
# for json_file in os.listdir(json_folder):
#     with open(os.path.join(json_folder, json_file), 'r') as file:
#         data = json.load(file)
#         json_data[json_file] = data


# # Limit the number of concurrent threads
# max_threads = 10  # Set the maximum number of concurrent threads
# with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
#     futures = {executor.submit(process_video_thread, video_file, json_data): video_file for video_file in video_files}

#     for future in concurrent.futures.as_completed(futures):
#         video_file = futures[future]
#         try:
#             future.result()
#         except Exception as e:
#             print(f"An error occurred while processing {video_file}: {str(e)}")

# print("Video Annotations generated successfully.")

# with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
#     futures = {executor.submit(process_image_thread, image_file, json_data): image_file for image_file in image_files}

#     for future in concurrent.futures.as_completed(futures):
#         image_file = futures[future]
#         try:
#             future.result()
#         except Exception as e:
#             print(f"An error occurred while processing {image_file}: {str(e)}")
# print("Image Annotations generated successfully.")


