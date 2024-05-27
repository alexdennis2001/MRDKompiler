import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np

# Load the model
model_path = 'fruit_detector_model.h5'
model = load_model(model_path)

# Function to preprocess the image
def preprocess_image(image_path):
    image = Image.open(image_path)
    image = image.resize((224, 224))
    image = np.array(image)
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    return image

# Function to make a prediction
def predict(image_path):
    image = preprocess_image(image_path)
    prediction = model.predict(image)
    predicted_class = np.argmax(prediction[0])
    return predicted_class

# Test the model with an image
image_path = 'avocado2.jpg'
predicted_class = predict(image_path)
print(f'Predicted class: {predicted_class}')
