from flask import Flask, request, render_template, jsonify, Response
import json
from build_model import load_model, ClassificationModel
import requests
import socket
import time
import tweet_processing as tp
from werkzeug import secure_filename
import ipdb


app = Flask(__name__)
PORT = 5353
ALLOWED_EXTENSIONS = set(['json'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET'])
def show_upload_page():
    return render_template('upload.html')


@app.route('/unlabeled_tweets', methods=['POST'])
def label_tweets():
    "Takes Tweet dump from POST data and returns a Tweet dump with labels"
    # Get Tweet Dump out of request
    uploaded_file_name_value = 'file'
    if request.headers['Content-Type'] == 'application/json':
        tweets_dump = request.json

    elif uploaded_file_name_value in request.files:
        uploaded_file = request.files[uploaded_file_name_value]
        if uploaded_file and allowed_file(uploaded_file.filename):
            tweets_dump = json.loads(uploaded_file.stream.read())

    # Predict using classification model
    labeled_tweets_dump = tp.predict_and_append_to_twitter_api_dump_json(
        tweets_dump, 'label', classification_model.predict)

    # Get JSON dump and return the response
    resp = jsonify(labeled_tweets_dump)
    resp.status_code = 200
    return resp


if __name__ == '__main__':
    # Load model
    classification_model = load_model('model.pkl')
    # Start Flask app
    app.run(host='0.0.0.0', port=PORT, debug=True)