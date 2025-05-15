import whois
import httpx
import pickle as pk
import pandas as pd
from urllib.parse import urlparse
import extractorFunctions as ef
import os

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'model')
PCA_MODEL_PATH = os.path.join(MODEL_DIR, 'pca_model.pkl')

def featureExtraction(url):
    extracted_features = []

    extracted_features.append(ef.getLength(url))
    extracted_features.append(ef.getDepth(url))
    extracted_features.append(ef.tinyURL(url))
    extracted_features.append(ef.prefixSuffix(url))
    extracted_features.append(ef.no_of_dots(url))
    extracted_features.append(ef.sensitive_word(url))

    dns_error = False
    try:
        domain_info = whois.whois(urlparse(url).netloc)
    except:
        domain_info = ''
        dns_error = True

    extracted_features.append(1 if dns_error else ef.domainAge(domain_info))
    extracted_features.append(1 if dns_error else ef.domainEnd(domain_info))

    dom_features = []
    try:
        resp = httpx.get(url)
    except:
        resp = ""

    dom_features.append(ef.iframe(resp))
    dom_features.append(ef.mouseOver(resp))
    dom_features.append(ef.forwarding(resp))

    extracted_features.append(ef.has_unicode(url) + ef.haveAtSign(url) + ef.havingIP(url))

    with open('model/pca_model.pkl', 'rb') as model_file:
        pca_model = pk.load(model_file)

    feature_labels = [
        'URL_Length', 'URL_Depth', 'TinyURL', 'Prefix/Suffix', 'No_Of_Dots', 'Sensitive_Words',
        'Domain_Age', 'Domain_End', 'Have_Symbol', 'domain_att'
    ]

    dom_df = pd.DataFrame([dom_features], columns=['iFrame', 'Web_Forwards', 'Mouse_Over'])
    extracted_features.append(pca_model.transform(dom_df)[0][0])

    result_row = pd.DataFrame([extracted_features], columns=feature_labels)

    return result_row
