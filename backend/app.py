# Import necessary libraries for the Flask application and machine learning model
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import json
import io # Import the io module for handling byte streams

# Initialize the Flask application
app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing (CORS) for all routes to allow frontend access

# Define dataset paths relative to the current working directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dataset')) # Base directory for datasets
TRAINING_DIR = os.path.join(BASE_DIR, "training_set") # Directory for training images
TESTING_DIR = os.path.join(BASE_DIR, "test_set") # Directory for testing images
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'cat_vs_dog_model.h5') # Path to save/load the trained model

# Global variable to store the loaded or trained model
model = None

# Function to train and save the image classification model
def train_and_save_model():
    global model # Declare model as global to modify the global variable
    from tensorflow.keras.preprocessing.image import ImageDataGenerator # Import for image data augmentation and preprocessing
    from tensorflow.keras.optimizers import RMSprop # Import RMSprop optimizer

    # Configure ImageDataGenerators for data preprocessing and augmentation
    train_datagen = ImageDataGenerator(rescale=1.0/255.) # Rescale pixel values to [0, 1] for training
    test_datagen = ImageDataGenerator(rescale=1.0/255.) # Rescale pixel values for testing/validation

    # Create a data generator for the training set
    train_generator = train_datagen.flow_from_directory(
        TRAINING_DIR,
        batch_size=32, # Number of images to yield from the generator per batch
        class_mode='binary', # Binary classification (e.g., cat or dog)
        target_size=(150, 150) # Resize images to 150x150 pixels
    )

    # Create a data generator for the validation set
    validation_generator = test_datagen.flow_from_directory(
        TESTING_DIR,
        batch_size=32,
        class_mode='binary',
        target_size=(150, 150)
    )

    # Define the Convolutional Neural Network (CNN) model architecture
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)), # First convolutional layer
        tf.keras.layers.MaxPooling2D(2, 2), # Max pooling layer to reduce spatial dimensions
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'), # Second convolutional layer
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'), # Third convolutional layer
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Dropout(0.5),  # Dropout layer to prevent overfitting
        tf.keras.layers.Flatten(), # Flatten the 3D output to 1D for the dense layers
        tf.keras.layers.Dense(512, activation='relu'), # Dense hidden layer with ReLU activation
        tf.keras.layers.Dense(1, activation='sigmoid') # Output layer with sigmoid activation for binary classification
    ])

    # Compile the model with binary crossentropy loss, RMSprop optimizer, and accuracy metric
    model.compile(
        loss='binary_crossentropy', # Loss function for binary classification
        optimizer=RMSprop(learning_rate=0.0003), # RMSprop optimizer with a specified learning rate
        metrics=['accuracy'] # Metric to monitor during training
    )

    # Train the model using the training and validation data generators
    history = model.fit(
        train_generator,
        epochs=10, # Number of epochs for training (can be increased for better accuracy)
        validation_data=validation_generator, # Data for validation during training
        verbose=1 # Display training progress
    )

    # Save the trained model to the specified path
    model.save(MODEL_PATH)
    app.logger.info(f"Model trained and saved to {MODEL_PATH}")

# Function to load an existing model or train a new one if it doesn't exist
def load_model_if_exists():
    global model # Declare model as global to modify the global variable
    if os.path.exists(MODEL_PATH): # Check if a pre-trained model file exists
        model = tf.keras.models.load_model(MODEL_PATH) # Load the model
        app.logger.info(f"Model loaded from {MODEL_PATH}")
    else:
        app.logger.info("No pre-trained model found. Training a new model...") # Log if no model is found
        train_and_save_model() # Train and save a new model

# Define the API endpoint for image classification
@app.route('/classify', methods=['POST'])
def classify_image():
    # Check if an image file is present in the request
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400 # Return error if no image

    file = request.files['image'] # Get the image file from the request
    if file.filename == '':
        return jsonify({'error': 'No selected image file'}), 400 # Return error if filename is empty

    # Ensure the model is loaded before attempting classification
    if model is None:
        return jsonify({'error': 'Model not loaded. Please restart the server or ensure model training/loading is successful.'}), 500

    try:
        # Read the image file content into bytes
        img_bytes = file.read()
        # Load and preprocess the image for model prediction
        img = image.load_img(io.BytesIO(img_bytes), target_size=(150, 150)) # Load image and resize
        x = image.img_to_array(img) # Convert image to a NumPy array
        x = np.expand_dims(x, axis=0) # Add batch dimension
        x = x / 255.0 # Normalize pixel values

        prediction = model.predict(x)[0][0] # Get the prediction from the model
        app.logger.info(f"Prediction Score: {prediction}") # Log the prediction score

        # Determine the classification result based on the prediction score
        if prediction > 0.5:
            result = "Dog 🐶" # If prediction is greater than 0.5, it's a dog
        else:
            result = "Cat 🐱" # Otherwise, it's a cat

        # Return the prediction result and confidence as a JSON response
        return jsonify({'prediction': result, 'confidence': float(prediction)})

    except Exception as e:
        app.logger.error(f"Error during image classification: {e}") # Log any errors during classification
        return jsonify({'error': str(e)}), 500 # Return an error response

# Entry point for the Flask application
if __name__ == '__main__':
    load_model_if_exists() # Load the model when the application starts
    app.run(debug=True, host='0.0.0.0', port=5000) # Run the Flask app in debug mode
