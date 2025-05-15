from flask import Flask, request, render_template
from featureExtractor import featureExtraction
from pycaret.classification import load_model, predict_model

app = Flask(__name__)

model = load_model('model/phishingdetection')

def make_prediction(url):
    extracted_features = featureExtraction(url)
    prediction_output = predict_model(model, data=extracted_features)
    score = prediction_output['prediction_score'][0]
    label = prediction_output['prediction_label'][0]

    return {
        'prediction_label': label,
        'prediction_score': score * 100,
    }

@app.route("/", methods=["GET", "POST"])
def index():
    result_data = None
    if request.method == "POST":
        url_input = request.form.get("url")
        result_data = make_prediction(url_input)
        return render_template('index.html', url=url_input, data=result_data)
    return render_template('index.html', data=result_data)

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

if __name__ == "__main__":
    app.run()
