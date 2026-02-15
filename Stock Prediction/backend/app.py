from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
import numpy as np
import pickle
from tensorflow.keras.models import load_model

app = Flask(__name__)
CORS(app)

# Load saved models
lr_model = pickle.load(open('models/lr_model.pkl', 'rb'))
scaler = pickle.load(open('models/scaler.pkl', 'rb'))
lstm_model = load_model('models/lstm_model.keras')

@app.route('/predict/<ticker>')
def predict(ticker):
    # Get recent data for prediction
    df = yf.download(ticker, period='65d', interval='1d')
    prices = df['Close'].values.reshape(-1, 1)
    
    # Linear Regression Prediction (next day)
    lr_pred = lr_model.predict([[len(prices) + 1]])[0]
    
    # LSTM Prediction (next day)
    last_60_days = scaler.transform(prices[-60:])
    x_input = np.reshape(last_60_days, (1, 60, 1))
    lstm_pred_scaled = lstm_model.predict(x_input)
    lstm_pred = scaler.inverse_transform(lstm_pred_scaled)[0][0]

    return jsonify({
        "ticker": ticker,
        "linear_regression": float(lr_pred),
        "lstm": float(lstm_pred),
        "actual_last": float(prices[-1])
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)