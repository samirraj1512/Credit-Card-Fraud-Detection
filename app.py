
# === Your Flask App Starts Here ===
from flask import Flask, request
from pyngrok import ngrok
import joblib
import numpy as np

# Load your model
model = joblib.load("rf_credit_fraud_pipeline.pkl")

app = Flask(__name__)

@app.route('/')
def home():
    input_fields = ''
    for i, feature_name in enumerate(['Time'] + [f'V{j}' for j in range(1, 29)] + ['Amount']):
        if i % 2 == 0:
            input_fields += '<div class="form-row">'
        input_fields += f'''
            <div class="form-group col-md-6">
                <input type="text" class="form-control" name="f{i}" placeholder="{feature_name}" required>
            </div>
        '''
        if i % 2 == 1:
            input_fields += '</div>'
    if len(['Time'] + [f'V{j}' for j in range(1, 29)] + ['Amount']) % 2 != 0:
        input_fields += '</div>'

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Credit Card Fraud Detection</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <style>
            body {{
                background-color: #f8f9fa;
            }}
            .container {{
                max-width: 700px;
                margin-top: 40px;
                padding: 30px;
                background-color: #ffffff;
                border-radius: 15px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            .btn-block {{
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2 class="text-center mb-4">🔐 Credit Card Fraud Detection</h2>
            <form action="/predict" method="post">
                {input_fields}
                <button type="submit" class="btn btn-primary btn-block">Predict</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/predict', methods=['POST'])
def predict():
    feature_names = ['Time'] + [f'V{j}' for j in range(1, 29)] + ['Amount']
    features = [float(request.form[f"f{i}"]) for i in range(30)]
    
    try:
        pred = model.predict([features])[0]
        result = 'Fraudulent Transaction' if pred == 1 else 'Legit Transaction'
        color = 'red' if pred == 1 else 'green'

        input_summary = ''
        for name, value in zip(feature_names, features):
            input_summary += f'<tr><td>{name}</td><td>{value}</td></tr>'

        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Prediction Result</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        </head>
        <body>
            <div class="container">
                <h2 style="text-align:center;margin-top:30px;">Prediction: <span style="color:{color};">{result}</span></h2>
                <h4>Entered Inputs:</h4>
                <table class="table table-bordered">
                    <thead><tr><th>Feature</th><th>Input Value</th></tr></thead>
                    <tbody>
                        {input_summary}
                    </tbody>
                </table>
                <div class="text-center">
                    <a href="/" class="btn btn-secondary">Try Again</a>
                </div>
            </div>
        </body>
        </html>
        '''
    except Exception as e:
        return f"<h3>Error: {e}</h3>"

if __name__ == "__main__":
    app.run(port=5000)
