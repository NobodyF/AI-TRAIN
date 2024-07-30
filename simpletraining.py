import os
import torch
from ultralytics import YOLO

def main():
    # Ensure CUDA is available and set the device to GPU if possible
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f'Using device: {device}')

    # Define training parameters
    data_yaml = 'E:/TestForRotating/data.yaml'  # Full path to your dataset YAML file
    total_epochs = 200  # Total number of epochs to train in each repeat
    batch_size = 12  # Adjust based on GPU memory
    img_size = 640  # Image size for training
    Repeats = 4  # Number of times to repeat the training process

    for repeat in range(Repeats):
        print(f"Repeat {repeat+1}/{Repeats}")

        # Load the pre-trained YOLOv8m model
        model = YOLO('yolov8m.pt')  # Start fresh training with the YOLOv8m model

        # Start training
        results = model.train(
            data=data_yaml,
            epochs=total_epochs,  # Train for the total number of epochs
            batch=batch_size,
            imgsz=img_size,
            val=True,
            cache=False  # Disable caching to save memory
        )

        # Save the trained model for this repeat
        final_model_path = f'yolov8m_trained_final_repeat_{repeat+1}.pt'
        model.save(final_model_path)
        print(f"Model for repeat {repeat+1} saved: {final_model_path}")

        # Clean up GPU memory
        cleanup()

    # Print final training results
    print("Training complete for all repeats.")
    print(results)

def cleanup():
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        print("GPU memory cache cleared.")

if __name__ == '__main__':
    main()
