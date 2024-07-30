import os
import shutil

# Images from folders
source_image_folder = 'E:/TestForRotating/Rlables/imgR'
source_label_folder = 'E:/TestForRotating/Rlables/imgRL'

# Path where to save
destination_image_folder = 'E:/TestForRotating/Rlables/imgForCode/'
destination_label_folder = 'E:/TestForRotating/Rlables/imgForCodeL/'

# Create the destination folders if needed (TODO: Can be removed)
os.makedirs(destination_image_folder, exist_ok=True)
os.makedirs(destination_label_folder, exist_ok=True)

# List all files in the source image and label folders
image_files = os.listdir(source_image_folder)
label_files = os.listdir(source_label_folder)

# Extract the base names (without extensions) of the label files
label_basenames = {os.path.splitext(label)[0] for label in label_files}

# Tracking images
total_images = len(image_files)
processed_count = 0

# Iterate through image files
for image_file in image_files:
    try:
        image_basename = os.path.splitext(image_file)[0]
        label_file = f"{image_basename}.txt"

        if image_basename in label_basenames:
            # main function to move
            shutil.move(os.path.join(source_image_folder, image_file), 
                        os.path.join(destination_image_folder, image_file))
            shutil.move(os.path.join(source_label_folder, label_file), 
                        os.path.join(destination_label_folder, label_file))
            print(f"Moved {image_file} and {label_file}")
        else:
            # deleting images which doesnt contain labels
            os.remove(os.path.join(source_image_folder, image_file))
            print(f"Deleted {image_file} (no matching label)")
        
        # just ui for terminal
        processed_count += 1
        progress_percent = (processed_count / total_images) * 100
        print(f"Progress: {progress_percent:.2f}% complete")
    
    except Exception as e:
        print(f"Error processing file {image_file}: {e}")

print("Processing complete.")