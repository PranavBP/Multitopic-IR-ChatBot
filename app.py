from chatterbot import ChatBot
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import urllib
import json
import logging
import tensorflow as tf
import tensorflow_text as text
import numpy as np
from sentence_transformers import SentenceTransformer, util

CB = ChatBot('ChatBot')
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

logging.getLogger('flask_cors').level = logging.DEBUG
model_simi = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
model = tf.keras.models.load_model("/home/bellam_pranav/classmodelnew")

def getIndexing(query):
    coreidnp = model.predict([query])
    coreidnp = np.where(coreidnp > 0.25, 1, 0)
    coreid = coreidnp[0][0]
    if coreid == 0:
        core = 'chitchat'
    else:
        core = 'reddit'

    return core

@app.route("/")
def helloWorld():
  return "Hello, Please naviagte to /chatbot ... Thanks!"

@app.route("/chatbot")
@cross_origin()
def home():
    return render_template("index.html")

@app.route('/inputQuery', methods=['POST'])
@cross_origin()
def getInput():
    try:
        data = request.get_json()
        index = getIndexing(data["query"])
        topic_list = data["list_of_topics"]
        if index == 'reddit':
            base_url = 'http://34.130.215.206:8983/solr/P4/select?q=body:(' + data["query"]
            for t in topic_list:
                base_url = base_url + '%20or%20topic:' + t
            search_url = base_url + '&rows=20&wt=json'
            search_url = search_url.replace(" ", "%20")
            d = urllib.request.urlopen(search_url)
            docs = json.load(d)['response']['docs']
            retrieved = []
            for doc in docs:
                retrieved.append(doc['body'])
            query_embedding = model_simi.encode(data["query"])
            ret_embedding = model_simi.encode(retrieved)
            similarity = util.dot_score(query_embedding, ret_embedding)
            simi = similarity.numpy()
            max_sim_index = np.argmax(simi)
            max_sim = np.amax(simi)
            top_reply = retrieved[max_sim_index]
            result = top_reply
        else:
            search_url = 'http://34.130.215.206:8983/solr/chit-chat/select?q=query:(' + data["query"] + ')&rows=20&wt=json'
            search_url = search_url.replace(" ", "%20")
            print(search_url)
            d = urllib.request.urlopen(search_url)
            docs = json.load(d)['response']['docs']
            retrieved = []
            for doc in docs:
                retrieved.append(doc['reply'])
            ret = []
            for doc in retrieved:
                ret.append(doc[0])
            print(ret)
            query_embedding = model_simi.encode(data["query"])
            ret_embedding = model_simi.encode(ret)
            similarity = util.dot_score(query_embedding, ret_embedding)
            print(similarity)
            simi = similarity.numpy()
            max_sim_index = np.argmax(simi)
            max_sim = np.amax(simi)
            top_reply = retrieved[max_sim_index]
            result = top_reply
        return result
    except Exception as e:
        print(e)
        return "Sorry I did not understand!"

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(CB.get_response(userText))

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False,port=9999)
