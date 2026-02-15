from flask import Flask, render_template, request
import tensorflow as tf
import numpy as np
import cv2
import os

# -----------------------------
# Flask app setup
# -----------------------------
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static")
MODEL_PATH = os.path.join(BASE_DIR, "pneumonia_cnn.h5")  # change to .keras if you switched

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -----------------------------
# Load trained model
# -----------------------------
model = tf.keras.models.load_model(MODEL_PATH)

# -----------------------------
# Image preprocessing function
# -----------------------------
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# -----------------------------
# Routes
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    image_path = None

    if request.method == "POST":
        file = request.files.get("file")

        if file:
            image_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(image_path)

            img = preprocess_image(image_path)
            pred = model.predict(img)[0][0]

            prediction = "PNEUMONIA DETECTED" if pred > 0.5 else "NORMAL"

    return render_template(
        "index.html",
        prediction=prediction,
        image_path=image_path
    )

# -----------------------------
# Run app
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
