from chatterbot import ChatBot
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import logging

CB = ChatBot('ChatBot')
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

logging.getLogger('flask_cors').level = logging.DEBUG

@app.route("/")
def helloWorld():
  return "Hello, Please naviagte to /chatbot ... Thanks!"

@app.route("/chatbot")
@cross_origin()
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(CB.get_response(userText))

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=9999)