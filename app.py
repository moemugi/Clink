from flask import Flask, request, render_template
from featureExtractor import featureExtraction
from pycaret.classification import load_model, predict_model

app = Flask(__name__)

model = load_model('model/phishingdetection')

feature_descriptions = {
    "url_length": "Length of the URL string",
    "url_depth": "Depth of URL path",
    "tinyurl": "Whether the URL is a tiny/shortened URL",
    "prefix_suffix": "Whether the domain contains '-' (prefix or suffix)",
    "no_of_dots": "Number of dots (.) in the URL",
    "sensitive_words": "Presence of suspicious words in URL",
    "domain_age": "Age of the domain in days",
    "domain_end": "Whether the domain is newly registered or ending soon",
    "have_symbol": "Presence of special symbols like '@'",
    "domain_att": "Domain attribute score (a calculated feature)",
}


def normalize_key(key):
    return key.lower().replace(" ", "_").replace("-", "_").replace("/", "_")


def make_prediction(url):
    extracted_features = featureExtraction(url)
    prediction_output = predict_model(model, data=extracted_features)

    score = prediction_output['prediction_score'][0]
    label = prediction_output['prediction_label'][0]

    # Convert the features row to a dict
    feature_dict = extracted_features.iloc[0].to_dict()

    # Normalize keys to match your feature_descriptions keys
    normalized_features = {normalize_key(k): v for k, v in feature_dict.items()}

    return {
        'prediction_label': label,
        'prediction_score': score * 100,
        'features': normalized_features  # pass normalized keys here
    }


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        prediction = make_prediction(url)
        return render_template(
            'index.html',
            url=url,
            data=prediction,
            feature_descriptions=feature_descriptions  # pass descriptions here
        )
    return render_template('index.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

if __name__ == "__main__":
    app.run()
