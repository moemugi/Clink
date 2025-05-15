from featureExtractor import featureExtraction
from pycaret.classification import load_model, predict_model
import os

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'model')
MODEL_PATH = os.path.join(MODEL_DIR, 'phishingdetection')

model = load_model(MODEL_PATH)


def make_prediction(url):
    features = featureExtraction(url)
    prediction_result = predict_model(model, data=features)

    score = prediction_result['prediction_score'][0]
    label = prediction_result['prediction_label'][0]

    return {
        'prediction_label': label,
        'prediction_score': score * 100,
    }

if __name__ == "__main__":
    test_urls = [
        'https://bafybeifqd2yktzvwjw5g42l2ghvxsxn76khhsgqpkaqfdhnqf3kiuiegw4.ipfs.dweb.link/',
        'http://about-ads-microsoft-com.o365.frc.skyfencenet.com',
        'https://chat.openai.com',
        'https://www.facebook.com/bysc.shai'
    ]

    for url in test_urls:
        print(make_prediction(url))
