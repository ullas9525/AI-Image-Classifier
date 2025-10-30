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
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'breed_classifier_model.h5') # Path to save/load the trained model

# Global variable to store the loaded or trained model
model = None

# Define strict confidence thresholds for classification to identify "Other" categories
STRICT_CONFIDENCE_THRESHOLD_HIGH = 0.75 # Lowered for multi-class classification
STRICT_CONFIDENCE_THRESHOLD_LOW = 0.05

# Function to train and save the image classification model
def train_and_save_model():
    global model # Declare model as global to modify the global variable
    from tensorflow.keras.preprocessing.image import ImageDataGenerator # Import for image data augmentation and preprocessing
    from tensorflow.keras.optimizers import Adam # Import Adam optimizer for transfer learning
    from tensorflow.keras.applications import MobileNetV2 # Import MobileNetV2 for transfer learning
    from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout # Import additional layers

    # Determine the number of classes (breeds)
    num_classes = len(os.listdir(TRAINING_DIR))
    app.logger.info(f"Number of classes (breeds): {num_classes}")

    # Configure ImageDataGenerators for data preprocessing and augmentation
    # MobileNetV2 expects input images to be preprocessed with its own function
    train_datagen = ImageDataGenerator(
        preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    test_datagen = ImageDataGenerator(
        preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input
    )

    # Create a data generator for the training set
    train_generator = train_datagen.flow_from_directory(
        TRAINING_DIR,
        batch_size=32, # Number of images to yield from the generator per batch
        class_mode='categorical', # Categorical classification for multiple breeds
        target_size=(224, 224) # MobileNetV2 expects 224x224 input size
    )

    # Create a data generator for the validation set
    validation_generator = test_datagen.flow_from_directory(
        TESTING_DIR,
        batch_size=32,
        class_mode='categorical',
        target_size=(224, 224) # MobileNetV2 expects 224x224 input size
    )

    # Load the pre-trained MobileNetV2 model
    base_model = MobileNetV2(input_shape=(224, 224, 3),
                             include_top=False, # Do not include the top classification layer
                             weights='imagenet') # Load weights pre-trained on ImageNet

    # Freeze the base model layers
    base_model.trainable = False

    # Add custom classification layers on top of the pre-trained model
    model = tf.keras.Sequential([
        base_model,
        GlobalAveragePooling2D(), # Global average pooling layer
        Dense(512, activation='relu'), # Dense hidden layer
        Dropout(0.5), # Dropout for regularization
        Dense(num_classes, activation='softmax') # Output layer with softmax for multi-class classification
    ])

    # Compile the model
    model.compile(optimizer=Adam(learning_rate=0.0001),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    app.logger.info("Starting initial training (head layers only)...")
    # Train the head of the model (newly added layers)
    history = model.fit(
        train_generator,
        epochs=20, # Increased initial training to 20 epochs
        validation_data=validation_generator,
        verbose=1
    )

    # Unfreeze some layers of the base model for fine-tuning
    base_model.trainable = True
    # Fine-tune from this layer onwards
    fine_tune_at = 100 # Unfreeze layers from index 100 onwards (adjust as needed)

    # Freeze all layers before the `fine_tune_at` layer
    for layer in base_model.layers[:fine_tune_at]:
        layer.trainable = False

    # Recompile the model for fine-tuning
    model.compile(optimizer=Adam(learning_rate=0.00001), # Use a very small learning rate for fine-tuning
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    app.logger.info("Starting fine-tuning (unfrozen layers of base model + head layers)...")
    # Continue training the model with fine-tuning
    history = model.fit(
        train_generator,
        epochs=20, # Additional 20 epochs for fine-tuning
        validation_data=validation_generator,
        verbose=1,
        initial_epoch=history.epoch[-1] + 1 # Start from where the previous training left off
    )

    # Save the trained model to the specified path
    model.save(MODEL_PATH)
    app.logger.info(f"Model trained and saved to {MODEL_PATH}")

    # Save class indices for later use in prediction
    with open('class_indices.json', 'w') as f:
        json.dump(train_generator.class_indices, f)
    app.logger.info("Class indices saved to class_indices.json")

# Global variable to store class indices
class_indices = None

# Function to load an existing model or train a new one if it doesn't exist
def load_model_if_exists():
    global model, class_indices # Declare model and class_indices as global
    if os.path.exists(MODEL_PATH): # Check if a pre-trained model file exists
        model = tf.keras.models.load_model(MODEL_PATH) # Load the model
        app.logger.info(f"Model loaded from {MODEL_PATH}")
        # Load class indices
        if os.path.exists('class_indices.json'):
            with open('class_indices.json', 'r') as f:
                class_indices = json.load(f)
            app.logger.info("Class indices loaded from class_indices.json")
        else:
            app.logger.error("class_indices.json not found. Model might not predict correctly.")
            # Attempt to train a new model to generate class_indices.json
            train_and_save_model()
            if os.path.exists('class_indices.json'):
                with open('class_indices.json', 'r') as f:
                    class_indices = json.load(f)
                app.logger.info("Class indices loaded after re-training.")
            else:
                return jsonify({'error': 'Class indices file not found after training.'}), 500
    else:
        app.logger.info("No pre-trained model found. Training a new model...") # Log if no model is found
        train_and_save_model() # Train and save a new model
        # After training, class_indices should be available
        if os.path.exists('class_indices.json'):
            with open('class_indices.json', 'r') as f:
                class_indices = json.load(f)
            app.logger.info("Class indices loaded after training.")
        else:
            return jsonify({'error': 'Class indices file not found after training.'}), 500


# Define the API endpoint for image classification
@app.route('/classify', methods=['POST'])
def classify_image():
    # Check if an image file is present in the request
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400 # Return error if no image

    file = request.files['image'] # Get the image file from the request
    if file.filename == '':
        return jsonify({'error': 'No selected image file'}), 400 # Return error if filename is empty

    # Ensure the model and class_indices are loaded before attempting classification
    if model is None or class_indices is None:
        return jsonify({'error': 'Model or class indices not loaded. Please restart the server or ensure model training/loading is successful.'}), 500

    try:
        # Read the image file content into bytes
        img_bytes = file.read()
        # Load and preprocess the image for model prediction
        img = image.load_img(io.BytesIO(img_bytes), target_size=(150, 150)) # Load image and resize
        x = image.img_to_array(img) # Convert image to a NumPy array
        x = np.expand_dims(x, axis=0) # Add batch dimension
        x = x / 255.0 # Normalize pixel values

        predictions = model.predict(x)[0] # Get the prediction probabilities from the model
        app.logger.info(f"Prediction probabilities: {predictions}") # Log the prediction probabilities

        # Get the predicted class index and its confidence
        predicted_class_index = np.argmax(predictions)
        confidence = float(predictions[predicted_class_index])

        # Map the predicted class index back to the breed name
        # Invert class_indices to get name from index
        idx_to_class = {v: k for k, v in class_indices.items()}
        predicted_breed = idx_to_class.get(predicted_class_index, "Unknown Breed")

        # Determine the classification result based on confidence threshold
        if confidence > STRICT_CONFIDENCE_THRESHOLD_HIGH:
            result = predicted_breed
        else:
            result = "Other/Uncertain ❓"

        # Return the prediction result and confidence as a JSON response
        return jsonify({
            'prediction': result,
            'confidence': confidence,
            'all_confidences': {idx_to_class[i]: float(p) for i, p in enumerate(predictions)}
        })

    except Exception as e:
        app.logger.error(f"Error during image classification: {e}") # Log any errors during classification
        return jsonify({'error': str(e)}), 500 # Return an error response

# Entry point for the Flask application
if __name__ == '__main__':
    load_model_if_exists() # Load the model when the application starts
    app.run(debug=True, host='0.0.0.0', port=5000) # Run the Flask app in debug mode
