import pickle

import pandas as pd
from sklearn.model_selection import train_test_split
import re
from nltk.corpus import stopwords
import pymorphy2 as pm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

df = pd.read_csv('train.csv')
df = df.drop(columns=['Unnamed: 0'])
stopwords = stopwords.words('russian')

def remove_punctuation(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in (stopwords)])
    morph = pm.MorphAnalyzer()
    text = ' '.join([morph.parse(word)[0].normal_form for word in text.split()])
    return text
# apply remove_punctuation to df['stolbec']
df['stolbec'] = df['stolbec'].apply(remove_punctuation)
df

X_train, X_test, y_train, y_test = train_test_split(df['stolbec'], df['answer'], test_size=0.2, random_state=42)
CV = CountVectorizer()
X_train_counts = CV.fit_transform(X_train)
X_test_counts = CV.transform(X_test)
clf = LogisticRegression(max_iter=10000, solver='lbfgs', multi_class='multinomial')

clf.fit(X_train_counts, y_train)
clf.score(X_test_counts, y_test)

X_train_counts=X_train_counts.toarray()
X_test_counts=X_test_counts.toarray()
y_test=y_test.to_numpy()
y_train=y_train.to_numpy()

# import keras for CNN
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils



# make CNN model
model = Sequential()
model.add(Dense(512, input_shape=(X_train_counts.shape[1],)))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

# feed data to CNN model
model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
model.fit(X_train_counts, y_train, batch_size=32, epochs=30, verbose=2)
model.evaluate(X_test_counts, y_test)

pickle.dump(model, open('model.pkl', 'wb'))

#model = pickle.load(open('model.pkl', 'rb'))