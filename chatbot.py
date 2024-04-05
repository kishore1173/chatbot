import numpy as np
import json
import pickle
import random
import nltk
import numpy
import keras
from nltk.stem import WordNetLemmatizer
from keras.models import Sequential
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, LSTM, Dense
from keras.layers import Dense, Dropout
from keras.models import Sequential

data_file=open("D:\VS CODE\Flask\chat1\dataset1.json").read()
data=json.loads(data_file)

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

words = [] # words are used in the dataset
classes = [] # add tag only in it 
documents = [] # Make list of words or patterns with the tag (['Hello'], 'greeting'), (['Hey'], 'greeting')

# Extract words and classes from the dataset
for intent in data['intents']:
    for pattern in intent['patterns']:
        words.extend(nltk.word_tokenize(pattern))
        documents.append((nltk.word_tokenize(pattern), intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lemmatize words and remove ignore characters
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ['?', '!', ',', "'s"]] #remove the special character and es
words = sorted(list(set(words)))    # remove the duplicate
classes = sorted(list(set(classes)))  #remove the duplicate tag

# Prepare training data
training = []
output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in doc[0]]
    #print(pattern_words)
    for word in words:
        bag.append(1) if word in pattern_words else bag.append(0)
    
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])
    #bag is the input array of 0,1. 0 reps 

random.shuffle(training)


# Split features and labels
X_train = np.array([bag for bag, _ in training])
y_train = np.array([output_row for _, output_row in training])

print("Training data shape:", X_train.shape)
print("Label data shape:", y_train.shape)

"""
model = Sequential()
model.add(Dense(128, activation='relu', input_shape=(len(X_train[0]),)))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(y_train[0]), activation='softmax'))
# accuracy = 100%
"""

LSTM Model
model = Sequential()
model.add(Embedding(input_dim=len(X_train[0]), output_dim=128))
model.add(LSTM(110, return_sequences = True, input_shape=(X_train.shape[1], 1)))
model.add(LSTM(110))
model.add(Dense(208, activation = 'relu'))
model.add(Dense(len(y_train[0]), activation='softmax'))
# accuracy = 98%


# Compile model
adam = keras.optimizers.Adam(0.001)
model.compile(optimizer=adam, loss='categorical_crossentropy', metrics=['accuracy'])


# Train model
weights = model.fit(np.array(X_train), np.array(y_train), epochs=100, batch_size=10, verbose=1)

# Evaluate model
loss, accuracy = model.evaluate(X_train, y_train)
print(f"Training Accuracy: {accuracy * 100:.2f}%")

print("Training completed!")



while True:
    input_text = input("You: ")
    if input_text.lower() == 'quit':
        break
    else:
        input_words = nltk.word_tokenize(input_text)
        input_bow = [0] * len(words)
        for w in input_words:
            if w.lower() in words:
                input_bow[words.index(w.lower())] = 1

        input_bow = np.array(input_bow).reshape(1, -1)
        predicted_probabilities = model.predict(input_bow)
        predicted_class_index = np.argmax(predicted_probabilities)
        
        
        def get_response(predicted_tag):
            for intent in data['intents']:
                if intent['tag'] == predicted_tag:
                    return random.choice(intent['responses'])
            return "Sorry, I don't understand that."
            
        predicted_tag = classes[predicted_class_index] # Replace with the predicted tag from your model

        

        
        response = get_response(predicted_tag)   
        print("Bot:",response)
       

def get_output(input_text):
    if input_text.lower() == 'quit':
        return
    else:
        input_words = nltk.word_tokenize(input_text)
        input_bow = [0] * len(words)
        for w in input_words:
            if w.lower() in words:
                input_bow[words.index(w.lower())] = 1

        input_bow = np.array(input_bow).reshape(1, -1)
        predicted_probabilities = model.predict(input_bow)
        predicted_class_index = np.argmax(predicted_probabilities)
        
        
        def get_response(predicted_tag):
            for intent in data['intents']:
                if intent['tag'] == predicted_tag:
                    return random.choice(intent['responses'])
            return "Sorry, I don't understand that."
            
        predicted_tag = classes[predicted_class_index] # Replace with the predicted tag from your model

        

        
        response = get_response(predicted_tag)   
        return response
        
