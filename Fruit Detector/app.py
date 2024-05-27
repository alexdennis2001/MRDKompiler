from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import io

# Load the model
model_path = 'fruit_detector_model.h5'
model = load_model(model_path)

# Function to preprocess the image
def preprocess_image(image_file):
    image = Image.open(image_file)
    image = image.resize((224, 224))
    image = np.array(image)
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    return image

# Function to make a prediction
def predict(image_file):
    image = preprocess_image(image_file)
    prediction = model.predict(image)
    predicted_class = np.argmax(prediction[0])
    return int(predicted_class)  # Convert to a standard Python int

# Initialize FastAPI
app = FastAPI()

@app.post("/predict")
async def classify_image(file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        image = io.BytesIO(image_data)
        predicted_class = predict(image)
        return JSONResponse(content={"predicted_class": predicted_class})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
