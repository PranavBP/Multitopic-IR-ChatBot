from chatterbot import ChatBot
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
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
print('start model_simi')
model_simi = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
print('start model..done simi')
model = tf.keras.models.load_model("/home/bellam_pranav/classmodelnew")
print("done model")
print(model.summary())

def execute(query):
    coreidnp = model.predict([query])

    print(query,coreidnp)
    coreidnp = np.where(coreidnp > 0.25, 1, 0)
    coreid = coreidnp[0][0]
    print(coreid)
    if coreid == 0:
        core = 'chitchat'
    else:
        core = 'reddit'

    search_url = ''


    retrieved = ['third wave of covid?','vaccine for covid are back is stock?']
    query_embedding = model_simi.encode(query)
    
    ret_embedding = model_simi.encode(retrieved)
    similarity = util.dot_score(query_embedding, ret_embedding)

    simi = similarity.numpy()
    max_sim_index = np.argmax(simi)
    max_sim = np.amax(simi)
    print("Similarity:", similarity, max_sim,max_sim_index)

    top_reply = retrieved[max_sim_index]
    return top_reply

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
        result = execute(data["query"])
        print(result)
        return result
    except Exception as e:
        print(e)
        return "Bhai kya kar rha hai thu? :/"

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(CB.get_response(userText))

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False,port=9999)
