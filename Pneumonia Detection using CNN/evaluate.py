import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix

IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# Load the model
model = tf.keras.models.load_model('pneumonia_cnn.h5')

# Create a data generator for the test set
test_gen = ImageDataGenerator(rescale=1./255)

test_data = test_gen.flow_from_directory(
    'dataset/test',
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    shuffle=False
)

# Get the true labels
y_true = test_data.classes

# Make predictions
y_pred_proba = model.predict(test_data)
y_pred = (y_pred_proba > 0.5).astype(int).reshape(-1)

# Print classification report
print("Classification Report:")
print(classification_report(y_true, y_pred, target_names=test_data.class_indices.keys()))

# Print confusion matrix
print("Confusion Matrix:")
print(confusion_matrix(y_true, y_pred))
