import os
import cv2
import random

# Constants
video_folder = 'videos'
annotation_folder = 'annotation'
output_folder = 'annotated_videos'
max_videos_to_process = 5  # Change this to the desired number of videos to process

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Function to parse YOLO-style annotation from a separate file
def parse_yolo_annotation(annotation_path):
    if os.path.exists(annotation_path):
        with open(annotation_path, 'r') as annotation_file:
            annotation_lines = annotation_file.readlines()

        annotations = []
        for annotation_line in annotation_lines:
            parts = annotation_line.strip().split()
            
            # Assuming the first element is the class name (string)
            class_name = parts[0]
            
            # Extracting the other values as floats
            center_x, center_y, width, height = map(float, parts[1:])
            
            annotations.append((class_name, center_x, center_y, width, height))

        return annotations
    else:
        return None

# List of video files in the folder
video_files = [video_file for video_file in os.listdir(video_folder) if video_file.endswith('.mp4')]

# Shuffle the list of video files
random.shuffle(video_files)

# Initialize a counter for processed videos
processed_videos = 0

# Iterate through video files and their annotations
for video_filename in video_files:
    if processed_videos == max_videos_to_process:
        break

    video_path = os.path.join(video_folder, video_filename)
    video_name = os.path.splitext(video_filename)[0]

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Initialize VideoWriter to save the annotated video
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter(os.path.join(output_folder, video_filename),
                        cv2.VideoWriter_fourcc(*'mp4v'), 30,
                        (frame_width, frame_height))

    frame_number = 1

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Get the annotation file for the current frame
        annotation_filename = f"{video_name}_{frame_number+1}.txt"
        annotation_path = os.path.join(annotation_folder, annotation_filename)

        # Parse YOLO annotation or handle the case of no detections
        annotations = parse_yolo_annotation(annotation_path)
        
        if annotations is not None:
            # Iterate through annotations and draw bounding boxes
            for annotation in annotations:
                class_id, center_x, center_y, width, height = annotation

                # Calculate bounding box coordinates
                x1 = int((center_x - width / 2) * frame.shape[1])
                y1 = int((center_y - height / 2) * frame.shape[0])
                x2 = int((center_x + width / 2) * frame.shape[1])
                y2 = int((center_y + height / 2) * frame.shape[0])

                # Draw the bounding box on the image
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                 # Display class ID above the bounding box
                cv2.putText(frame, f'{class_id}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        else:
            # If there are no detections, display a "No Detections" message in red
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottom_left_corner = (10, 30)
            font_scale = 1
            font_color = (0, 0, 255)  # Red
            line_type = 2
            cv2.putText(frame, "No Detections", bottom_left_corner, font, font_scale, font_color, line_type)

        # Write the frame to the output video
        out.write(frame)

        frame_number += 1

    # Release video objects
    cap.release()
    out.release()

    processed_videos += 1

print(f"{processed_videos} videos processed and saved to '{output_folder}' folder.")
