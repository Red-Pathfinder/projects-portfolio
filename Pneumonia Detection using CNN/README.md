# Pneumonia Detection using CNN

This project is a web application that uses a Convolutional Neural Network (CNN) to detect pneumonia from chest X-ray images.

## Features

-   **Pneumonia/Normal Prediction:** Upload a chest X-ray and the model will predict whether it shows signs of pneumonia.
-   **Grad-CAM Visualization:** For images predicted as having pneumonia, a heatmap is generated to show the areas of the image that most influenced the model's decision.

## Files

-   `app.py`: The Flask backend that handles image uploads, predictions, and Grad-CAM generation.
-   `index.html`: The frontend for uploading images and viewing results.
-   `train.py`: The script used to train the CNN model.
-   `evaluate.py`: A script to evaluate the model's performance on the test set.
-   `pneumonia_cnn.h5`: The trained and saved Keras model.
-   `dataset/`: Directory containing the image dataset, split into `train`, `test`, and `val` sets.

## How to Run

1.  **Install Dependencies:**
    This project requires Python and several packages. It appears you are using Python 3.14, for which TensorFlow does not seem to have a compatible version available at the moment. It is recommended to use a Python version for which TensorFlow is available (e.g., Python 3.9, 3.10, or 3.11).

    Once you have a compatible Python version, install the necessary packages:
    ```bash
    pip install tensorflow scikit-learn opencv-python flask
    ```

2.  **Run the Evaluation Script (Optional):**
    To evaluate the model's performance on the test set, run the following command:
    ```bash
    python "Lab work/AD Lab/Experiment 3/evaluate.py"
    ```

3.  **Run the Web Application:**
    To start the Flask web server, run:
    ```bash
    python "Lab work/AD Lab/Experiment 3/app.py"
    ```
    Then, open your web browser and go to `http://127.0.0.1:5000`.

## Summary of Changes

-   **Added Grad-CAM:** The application now includes visual highlighting of affected regions in X-ray images diagnosed with pneumonia. This is implemented using Grad-CAM, and the heatmap is displayed next to the original image.
-   **Added Evaluation Script:** An `evaluate.py` script has been created to provide a more formal evaluation of the model's performance using the test dataset.
-   **Updated Frontend:** The user interface has been updated to display the Grad-CAM heatmap.
