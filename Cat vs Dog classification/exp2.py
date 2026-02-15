import sys
import subprocess

# -------- AUTO INSTALL REQUIRED PACKAGES --------
def install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

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
    from sklearn.model_selection import train_test_split
    from sklearn.svm import SVC
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.cluster import KMeans
    from sklearn.neighbors import KNeighborsClassifier
except:
    install("scikit-learn")
    from sklearn.model_selection import train_test_split
    from sklearn.svm import SVC
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.cluster import KMeans
    from sklearn.neighbors import KNeighborsClassifier

import os
import pickle

# -------- DATA PATH --------
BASE_PATH = r"C:\Study\Coding\Lab work\AD Lab\Experiment 2\PetImages"

# -------- LOAD DATA --------
X, y = [], []

def preprocess(path):
    img = cv2.imread(path)
    if img is None:
        return None
    img = cv2.resize(img, (64, 64))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img.flatten()

for label, folder in enumerate(["Cat", "Dog"]):
    folder_path = os.path.join(BASE_PATH, folder)
    for file in os.listdir(folder_path)[:500]:
        data = preprocess(os.path.join(folder_path, file))
        if data is not None:
            X.append(data)
            y.append(label)

X = np.array(X)
y = np.array(y)

print("Data loaded:", X.shape)

# -------- TRAIN TEST SPLIT --------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------- TRAIN MODELS --------
svm = SVC()
svm.fit(X_train, y_train)

rf = RandomForestClassifier()
rf.fit(X_train, y_train)

lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, y_train)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

kmeans = KMeans(n_clusters=2, random_state=42)
kmeans.fit(X_train)

print("Models trained")

# -------- SAVE MODELS --------
with open("svm.pkl", "wb") as f:
    pickle.dump(svm, f)

with open("rf.pkl", "wb") as f:
    pickle.dump(rf, f)

with open("lr.pkl", "wb") as f:
    pickle.dump(lr, f)

with open("knn.pkl", "wb") as f:
    pickle.dump(knn, f)

with open("kmeans.pkl", "wb") as f:
    pickle.dump(kmeans, f)

print("Models saved")
