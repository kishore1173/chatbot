from flask import Flask, render_template, request, jsonify
import json
import random
import nltk
import numpy as np
import chatbot as chatbot 

app = Flask(__name__)

# Instantiate your chatbot

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_question', methods=['POST'])
def process_question():
    data = request.json
    question = data['question']

    # Generate response using the chatbot
    response = chatbot.get_output(question)
    
    return jsonify({'result': response})



if __name__ == '__main__':
    app.run(debug=True)
