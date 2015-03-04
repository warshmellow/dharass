from flask import Flask, request, render_template, jsonify, Response
import json
from build_model import load_model, ClassificationModel
import requests
import socket
import time
import tweet_processing as tp
import ipdb


app = Flask(__name__)
PORT = 5353


@app.route('/unlabeled_tweets', methods=['POST'])
def label_tweets():
    "Takes Tweet dump from POST data and returns a Tweet dump with labels"
    # Get Tweet Dump out of request
    tweets_dump = request.json

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
