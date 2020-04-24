from flask import Flask
import requests
import os
app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Deployed to Wherever! </h1>'
    #Environment variables: os.environ['varName']

#@app.route('/', methods=['GET'])