import cv2
import os
import random

# Constants
frame_folder = '14th_Mar_visua_downloaded_data/frames'
annotation_folder = '14th_Mar_visua_downloaded_data/annotation'
output_folder = '14th_Mar_visua_downloaded_data/annotated_images'
num_images_to_process = 100  # Change this to the desired number of images to process

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Function to parse YOLO-style annotation or return None if it doesn't exist
def parse_yolo_annotation(annotation_path):
    if os.path.exists(annotation_path):
        with open(annotation_path, 'r') as annotation_file:
            annotation_lines = annotation_file.readlines()

        annotations = []
        for annotation_line in annotation_lines:
            class_id, center_x, center_y, width, height = map(float, annotation_line.strip().split())
            annotations.append((class_id, center_x, center_y, width, height))

        return annotations
    else:
        return None

images = os.listdir(frame_folder)
random.shuffle(images)
count = 0
font = cv2.FONT_HERSHEY_SIMPLEX
bottom_left_corner = (10, 30)
font_scale = 1
font_color = (0, 0, 255)  # Red
line_type = 2

classes_file = "14th_Mar_visua_downloaded_data/classes.txt"  # Replace with your classes.txt file if available, otherwise set to None
labels = {}
if classes_file:
    with open(classes_file, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            label_name = line.strip()
            labels[i] = label_name

# print(labels)

# Iterate through images and their annotations
for image_filename in images:
    if count == num_images_to_process:
        break

    count += 1

    if image_filename.lower().endswith(('.png','.jpg')):
        image_path = os.path.join(frame_folder, image_filename)

        # Load the image
        image = cv2.imread(image_path)

        # Get the corresponding annotation filename
        annotation_filename = os.path.splitext(image_filename)[0] + '.txt'
        annotation_path = os.path.join(annotation_folder, annotation_filename)

        # Parse YOLO annotations or handle the case of no detections
        annotations = parse_yolo_annotation(annotation_path)
        # print(image_path, annotations)
        if annotations is not None:
            # Iterate through annotations and draw bounding boxes
            for annotation in annotations:
                class_id, center_x, center_y, width, height = annotation
                label = labels.get(class_id, str(class_id))

                # Calculate bounding box coordinates
                x1 = int((center_x - width / 2) * image.shape[1])
                y1 = int((center_y - height / 2) * image.shape[0])
                x2 = int((center_x + width / 2) * image.shape[1])
                y2 = int((center_y + height / 2) * image.shape[0])

                # Draw the bounding box on the image
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(image, label, (x1, y1), font, font_scale, (0, 255, 0), line_type)
        else:
            # If there are no detections, display a "No Detections" message in red
            
            cv2.putText(image, "No Detections", bottom_left_corner, font, font_scale, font_color, line_type)

        # Save the annotated image to the output folder
        output_path = os.path.join(output_folder, image_filename)
        cv2.imwrite(output_path, image)

# Print a message when done
print(f"Annotations drawn on {num_images_to_process} images and saved to '{output_folder}' folder.")








