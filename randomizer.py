import os
import random
import shutil

def pick_random_samples(image_dir, label_dir, output_image_dir, output_label_dir, sample_count):
    # Get list of all img and lab
    image_files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
    label_files = [f for f in os.listdir(label_dir) if os.path.isfile(os.path.join(label_dir, f))]

    # Check if sample count exceeds available images
    if sample_count > len(image_files):
        print("Sample count exceeds the number of available images.")
        return

    # Shuffle image files
    random.shuffle(image_files)

    
    os.makedirs(output_image_dir, exist_ok=True)
    os.makedirs(output_label_dir, exist_ok=True)

    copied_samples = 0

    # Copy 
    for image_name in image_files:
        if copied_samples >= sample_count:
            break

        base_name = os.path.splitext(image_name)[0]
        label_name = base_name + ".txt"  

        if label_name not in label_files:
            print(f"Warning: Label file for {image_name} not found. Skipping.")
            continue

        shutil.copy(os.path.join(image_dir, image_name), os.path.join(output_image_dir, image_name))
        shutil.copy(os.path.join(label_dir, label_name), os.path.join(output_label_dir, label_name))

        copied_samples += 1

    print(f"Copied {copied_samples} random samples to {output_image_dir} and {output_label_dir}")

# Directories
image_directory = 'E:/TestForRotating/Dataset640/OLDimages'
label_directory = 'E:/TestForRotating/Dataset640/OLDlabels'
output_image_directory = 'E:/TestForRotating/Dataset640/br'
output_label_directory = 'E:/TestForRotating/Dataset640/brl'
samples_to_pick = 1175 # Your preffered sample count

pick_random_samples(image_directory, label_directory, output_image_directory, output_label_directory, samples_to_pick)
