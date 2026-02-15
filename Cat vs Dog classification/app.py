import sys
import subprocess

def install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

try:
    from flask import Flask, request, render_template
except:
    install("flask")
    from flask import Flask, request, render_template

try:
    import cv2
except:
    install("opencv-python")
    import cv2

try:
    import numpy as np
except:
    install("numpy")
    import numpy as np

try:
    import pickle
except:
    install("pickle")

app = Flask(__name__)

# -------- LOAD MODELS --------
with open("svm.pkl", "rb") as f:
    svm = pickle.load(f)

with open("rf.pkl", "rb") as f:
    rf = pickle.load(f)

with open("lr.pkl", "rb") as f:
    lr = pickle.load(f)

with open("knn.pkl", "rb") as f:
    knn = pickle.load(f)

models = {
    "svm": svm,
    "rf": rf,
    "lr": lr,
    "knn": knn
}

# -------- IMAGE PREPROCESSING --------
def preprocess_img(file):
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    img = cv2.resize(img, (64, 64))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img.flatten()

# -------- ROUTES --------
@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        img = request.files["image"]
        model_name = request.form["model"]

        model = models[model_name]
        data = preprocess_img(img)

        pred = model.predict([data])[0]
        result = "Dog 🐶" if pred == 1 else "Cat 🐱"

    return render_template("index.html", result=result)

# -------- RUN --------
if __name__ == "__main__":
    app.run(debug=True)
