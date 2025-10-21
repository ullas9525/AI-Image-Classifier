import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import json
import io # Import the io module

app = Flask(__name__)
CORS(app) # Enable CORS for all origins

# Define dataset paths relative to the current working directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dataset'))
TRAINING_DIR = os.path.join(BASE_DIR, "training_set")
TESTING_DIR = os.path.join(BASE_DIR, "test_set")
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'cat_vs_dog_model.h5') # Path to save/load the model

# Global variable for the model
model = None

def train_and_save_model():
    global model
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from tensorflow.keras.optimizers import RMSprop

    # Preprocess the data using ImageDataGenerator
    train_datagen = ImageDataGenerator(rescale=1.0/255.)
    test_datagen = ImageDataGenerator(rescale=1.0/255.)

    train_generator = train_datagen.flow_from_directory(
        TRAINING_DIR,
        batch_size=32,
        class_mode='binary',
        target_size=(150, 150)
    )

    validation_generator = test_datagen.flow_from_directory(
        TESTING_DIR,
        batch_size=32,
        class_mode='binary',
        target_size=(150, 150)
    )

    # Define the CNN model
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Dropout(0.5),  # helps reduce overfitting
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    # Compile the model
    model.compile(
        loss='binary_crossentropy',
        optimizer=RMSprop(learning_rate=0.0003),
        metrics=['accuracy']
    )

    # Train the model
    history = model.fit(
        train_generator,
        epochs=10, # Reduced epochs for quicker demonstration, can be increased
        validation_data=validation_generator,
        verbose=1
    )

    # Save the trained model
    model.save(MODEL_PATH)
    app.logger.info(f"Model trained and saved to {MODEL_PATH}")

def load_model_if_exists():
    global model
    if os.path.exists(MODEL_PATH):
        model = tf.keras.models.load_model(MODEL_PATH)
        app.logger.info(f"Model loaded from {MODEL_PATH}")
    else:
        app.logger.info("No pre-trained model found. Training a new model...")
        train_and_save_model()

@app.route('/classify', methods=['POST'])
def classify_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected image file'}), 400

    if model is None:
        return jsonify({'error': 'Model not loaded. Please restart the server or ensure model training/loading is successful.'}), 500

    try:
        # Read the image file content
        img_bytes = file.read()
        img = image.load_img(io.BytesIO(img_bytes), target_size=(150, 150))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = x / 255.0

        prediction = model.predict(x)[0][0]
        app.logger.info(f"Prediction Score: {prediction}")

        if prediction > 0.5:
            result = "Dog 🐶"
        else:
            result = "Cat 🐱"

        return jsonify({'prediction': result, 'confidence': float(prediction)})

    except Exception as e:
        app.logger.error(f"Error during image classification: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    load_model_if_exists()
    app.run(debug=True, host='0.0.0.0', port=5000)
