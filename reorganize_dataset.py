import os
import shutil
import random
from collections import defaultdict
from sklearn.model_selection import train_test_split

# Define paths
BASE_DIR = 'dataset'
SOURCE_IMAGES_DIR = os.path.join(BASE_DIR, 'images')
TRAINING_DIR = os.path.join(BASE_DIR, 'training_set')
TESTING_DIR = os.path.join(BASE_DIR, 'test_set')

# Create base training and testing directories if they don't exist
os.makedirs(TRAINING_DIR, exist_ok=True)
os.makedirs(TESTING_DIR, exist_ok=True)

# Collect all image files and group them by breed
breed_images = defaultdict(list)
for filename in os.listdir(SOURCE_IMAGES_DIR):
    if filename.endswith('.jpg'):
        # Extract breed name (e.g., "Abyssinian" from "Abyssinian_1.jpg")
        breed_name = filename.split('_')[0]
        breed_images[breed_name].append(filename)

print(f"Found {len(breed_images)} unique breeds.")

# Split images for each breed into training and testing sets
for breed, images in breed_images.items():
    # Create breed-specific directories
    os.makedirs(os.path.join(TRAINING_DIR, breed), exist_ok=True)
    os.makedirs(os.path.join(TESTING_DIR, breed), exist_ok=True)

    # Split images into training and testing (80% train, 20% test)
    if len(images) > 1: # Ensure there's more than one image to split
        train_files, test_files = train_test_split(images, test_size=0.2, random_state=42)
    else: # If only one image, put it in training
        train_files = images
        test_files = []

    print(f"Breed: {breed}, Training images: {len(train_files)}, Testing images: {len(test_files)}")

    # Move training files
    for file in train_files:
        src_path = os.path.join(SOURCE_IMAGES_DIR, file)
        dst_path = os.path.join(TRAINING_DIR, breed, file)
        shutil.copy(src_path, dst_path) # Use copy to keep original dataset intact

    # Move testing files
    for file in test_files:
        src_path = os.path.join(SOURCE_IMAGES_DIR, file)
        dst_path = os.path.join(TESTING_DIR, breed, file)
        shutil.copy(src_path, dst_path) # Use copy to keep original dataset intact

print("Dataset reorganization complete.")
