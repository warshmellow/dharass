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
import twitter


app = Flask(__name__)
PORT = 5353
ALLOWED_EXTENSIONS = set(['json'])

# Connect to Twitter API (Application Level Auth)
with open('twitter_app_keys.txt') as f:
    keys = tuple([line.rstrip() for line in list(f)])
CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = keys

api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN,
                  access_token_secret=ACCESS_TOKEN_SECRET)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class TwitterScreeNameForm(Form):
    screen_name = StringField(u'Screen Name', [validators.required()])


class TweetTextForm(Form):
    text = StringField(
        u'Tweet Text',
        [validators.required(), validators.length(max=140)])


@app.route('/', methods=['GET'])
def show_index():
    screen_name_form = TwitterScreeNameForm(csrf_enabled=False)
    message_form = TweetTextForm(csrf_enabled=False)
    return render_template(
        'index.html',
        screen_name_form=screen_name_form,
        message_form=message_form)


@app.route('/unlabeled_tweets', methods=['POST'])
def label_tweets():
    "Takes Tweet dump from POST data and returns a Tweet dump with labels"
    # Get Tweet Dump out of request, via JSON in Request, Uploaded file,
    # Message Form or Screen Name Form
    uploaded_file_name_value = 'file'
    message_form_text_name = 'text'
    screen_name_form_name = 'screen_name'
    # JSON in Request
    if request.headers['Content-Type'] == 'application/json':
        tweets_dump = request.json
        # Predict using classification model
        labeled_tweets_dump = tp.predict_and_append_to_twitter_api_dump_json(
            tweets_dump, 'label', classification_model.predict)
        # JSONify and return
        resp = jsonify(labeled_tweets_dump)
        resp.status_code = 200
        return resp

    # Uploaded file
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

    # Message Form
    elif message_form_text_name in request.form:
        texts = [request.form[message_form_text_name]]
        data = classification_model.predict(texts)
        return render_template(
            'table.html',
            data=data,
            is_empty=(len(data) == 0),
            column_length=2)

    # Screen Name Form
    elif screen_name_form_name in request.form:
        if request.form[screen_name_form_name] == '':
            data = []
        else:
            # Construct query by '@' + inputed screen name
            term = '@' + request.form[screen_name_form_name]
            # Execute search and get results
            raw_screen_name_mentions = api.GetSearch(
                term=term,
                lang='en',
                result_type='recent',
                count=100)
            # Predict on search results and render template
            data = tp.apply_to_text_of_twitter_api_query(
                raw_screen_name_mentions,
                [classification_model.predict,
                    lambda lst: map(lambda x: x[1], lst)])
        return render_template(
            'table.html',
            data=data,
            is_empty=(len(data) == 0),
            column_length=3)


if __name__ == '__main__':
    # Load model
    classification_model = load_model('model.pkl')
    # Load Bootstrap
    Bootstrap(app)
    # Start Flask app
    app.run(host='0.0.0.0', port=PORT)
