from flask import Flask, request, render_template, jsonify, Response
from flask_wtf import Form
from flask_bootstrap import Bootstrap
from wtforms import StringField
from wtforms import validators
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


class TweetTextForm(Form):
    text = StringField(
        u'Tweet Text',
        [validators.required(), validators.length(max=140)])


@app.route('/', methods=['GET'])
def show_index():
    form = TweetTextForm(csrf_enabled=False)
    return render_template('index.html', form=form)


# @app.route('/upload', methods=['GET'])
# def show_upload_page():
#     return render_template('upload.html', form=form)


@app.route('/unlabeled_tweets', methods=['POST'])
def label_tweets():
    "Takes Tweet dump from POST data and returns a Tweet dump with labels"
    # Get Tweet Dump out of request, via JSON in Request, Uploaded file, or
    # Form
    uploaded_file_name_value = 'file'
    form_text_name = 'text'
    if request.headers['Content-Type'] == 'application/json':
        tweets_dump = request.json
        # Predict using classification model
        labeled_tweets_dump = tp.predict_and_append_to_twitter_api_dump_json(
            tweets_dump, 'label', classification_model.predict)
        # JSONify and return
        resp = jsonify(labeled_tweets_dump)
        resp.status_code = 200
        return resp

    elif uploaded_file_name_value in request.files:
        uploaded_file = request.files[uploaded_file_name_value]
        if uploaded_file and allowed_file(uploaded_file.filename):
            tweets_dump = json.loads(uploaded_file.stream.read())
            # Predict using classification model if JSON or Uploaded file
            labeled_tweets_dump = tp.predict_and_append_to_twitter_api_dump_json(
                tweets_dump, 'label', classification_model.predict)
            # Pass data to table template and render
            data = tp.get_info_from_twitter_api_dump_json(labeled_tweets_dump)
            return render_template(
                'table.html',
                data=data,
                is_empty=(len(data) == 0),
                column_length=3)

    # Return {text: label} JSON if Form
    elif form_text_name in request.form:
        texts = [request.form[form_text_name]]
        data = classification_model.predict(texts)
        return render_template(
            'table.html',
            data=data,
            is_empty=(len(data) == 0),
            column_length=2)


if __name__ == '__main__':
    # Load model
    classification_model = load_model('model.pkl')
    # Load Bootstrap
    Bootstrap(app)
    # Start Flask app
    app.run(host='0.0.0.0', port=PORT, debug=True)
