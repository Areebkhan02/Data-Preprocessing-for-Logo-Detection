# ===================== Without using threads ==========================================


import os
import cv2
from tqdm import tqdm

# Folder containing your videos
video_folder = 'videos'

# Create a folder to save the images if it doesn't exist
frame_folder = 'frames'
annotation_folder = 'annotation_with_classes'
os.makedirs(frame_folder, exist_ok=True)

# Function to process a single video file
def process_video(video_file):
    if video_file.endswith('.mp4'):
        # Construct the full path to the video file
        video_path = os.path.join(video_folder, video_file)

        # Open the video file for reading
        cap = cv2.VideoCapture(video_path)

        # Get the base name of the video (without extension)
        video_name = os.path.splitext(video_file)[0]

        # Get the total number of frames in the video
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Initialize frame counter starting from 0
        frame_count = 0

        # Create a progress bar with tqdm
        with tqdm(total=total_frames, desc=f"Processing {video_file}", unit="frame") as pbar:
            while True:
                # Read a frame from the video
                ret, frame = cap.read()

                # Break the loop if we have reached the end of the video
                if not ret:
                    break

                # Construct the corresponding annotation (.txt) filename
                annotation_filename = f"{video_name}_{frame_count}.txt"
                annotation_filepath = os.path.join(annotation_folder, annotation_filename)

                # Check if the annotation file exists (only process the frame if it has a corresponding .txt)
                if os.path.isfile(annotation_filepath):
                    # Construct the output image file name
                    image_name = f"{video_name}_{frame_count}.jpg"
                    image_path = os.path.join(frame_folder, image_name)

                    # Save the frame as an image
                    cv2.imwrite(image_path, frame)
                    # print(f"Saved frame {image_name}")

                # Increment the frame counter and update the progress bar
                frame_count += 1
                pbar.update(1)

        # Release the video capture object
        cap.release()

# List of video files in the folder
video_files = [video_file for video_file in os.listdir(video_folder) if video_file.endswith('.mp4')]

# Process each video file
for video_file in video_files:
    process_video(video_file)

print("Frame extraction completed.")








'''

# ====================== using threads to extract frames from videos ======================

import os
import cv2
import shutil
from concurrent.futures import ThreadPoolExecutor

# Folder containing your videos
video_folder = '10_logos_data/videos'

# Create a folder to save the images if it doesn't exist
frame_folder = '10_logos_data/frames'
annotation_folder = '10_logos_data/annotation_with_classes'
os.makedirs(frame_folder, exist_ok=True)

# Function to process a single video file
def process_video(video_file):
    if video_file.endswith('.mp4'):
        # Construct the full path to the video file
        video_path = os.path.join(video_folder, video_file)

        # Open the video file for reading
        cap = cv2.VideoCapture(video_path)

        # Get the base name of the video (without extension)
        video_name = os.path.splitext(video_file)[0]

        # Initialize frame counter starting from 1
        frame_count = 0

        while True:
            # Read a frame from the video
            ret, frame = cap.read()

            # Break the loop if we have reached the end of the video
            if not ret:
                break

            # Construct the output image file name8
            image_name = f"{video_name}_{frame_count}.jpg"
            annotation_filename = f"{video_name}_{frame_count}.txt"
            annotation_filepath = os.path.join(annotation_folder, annotation_filename)
            if os.path.isfile(annotation_filepath):
                print(image_name)
                image_path = os.path.join(frame_folder, image_name)
    
                # Save the frame as an image
                cv2.imwrite(image_path, frame)

            # Increment the frame counter
            frame_count += 1

        # Release the video capture object
        cap.release()

# List of video files in the folder
video_files = [video_file for video_file in os.listdir(video_folder) if video_file.endswith('.mp4')]
# video_files = video_files[1000:1400]
# Limit the number of concurrent threads to 15





max_threads = 10

# Process video files in parallel using ThreadPoolExecutor
with ThreadPoolExecutor(max_threads) as executor:
    executor.map(process_video, video_files)

print("Frames extracted and saved successfully.")

# images_folder = '27th_sep/images'
# for image_file in os.listdir(images_folder):
#     src = os.path.join(images_folder, image_file)
#     dst = os.path.join(frame_folder, image_file)
    
#     # Use shutil.copy to copy the image
#     shutil.copy(src, dst)
 
# print("Images copied to the 'frames' folder.")
'''