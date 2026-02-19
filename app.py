import pickle
from flask import Flask, request, jsonify,app,url_for,render_template
import numpy as np
# from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
# Load the trained model
regmodel = pickle.load(open('regmodel.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api', methods=['POST'])
def predict_api():
    data = request.json['data']
    print(np.array(list(data.values())).reshape(1, -1))
    data_scaled = scaler.transform(np.array(list(data.values())).reshape(1, -1))
    prediction = regmodel.predict(data_scaled)
    print(prediction[0])
    return jsonify({'prediction': float(prediction[0])})

@app.route('/predict',methods=['POST'])
def predict():
    data = [float(x) for x in request.form.values()]
    print(data)
    final_input = scaler.transform(np.array(data).reshape(1,-1))
    # print(final_input)
    output = regmodel.predict(final_input)
    return render_template("home.html",prediction_text=f"The House Price Prediction is ${output[0].round(4)}")


if __name__ == "__main__":
    app.run(debug=True)