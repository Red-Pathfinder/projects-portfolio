import yfinance as yf
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout

# Ensure directory exists
os.makedirs('models', exist_ok=True)

# 1. Get Data
ticker = 'AAPL'
df = yf.download(ticker, start='2020-01-01', end='2024-12-31')
# Flatten columns if they are multi-indexed
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

data = df[['Close']].values

# 2. Scaling
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# 3. Linear Regression
X_lr = np.array(range(len(data))).reshape(-1, 1)
y_lr = data.flatten()
lr_model = LinearRegression().fit(X_lr, y_lr)

# 4. LSTM Prep (60-day window)
x_train, y_train = [], []
for i in range(60, len(scaled_data)):
    x_train.append(scaled_data[i-60:i, 0])
    y_train.append(scaled_data[i, 0])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# 5. LSTM Model
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)),
    Dropout(0.2),
    LSTM(50, return_sequences=False),
    Dropout(0.2),
    Dense(1)
])
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train, y_train, epochs=5, batch_size=32)

# 6. Save Everything
with open('models/lr_model.pkl', 'wb') as f:
    pickle.dump(lr_model, f)
with open('models/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
model.save('models/lstm_model.keras')

print("Models saved successfully in backend/models/")