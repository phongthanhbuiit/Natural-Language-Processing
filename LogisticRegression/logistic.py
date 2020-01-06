import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
import warnings
'''
đọc file dữ liệu
'''
warnings.filterwarnings("ignore", category=FutureWarning)
sms = pd.read_csv('spam.csv', encoding='latin-1')
sms = sms.drop(labels=["Unnamed: 2", "Unnamed: 3", "Unnamed: 4"], axis=1)
sms.columns = ["result", "text"]
result = np.array(sms["result"])
text = np.array(sms["text"])

print("Ví dụ dữ liệu: ")
print(sms.head())

X_train_raw, X_test_raw, y_train, y_test = train_test_split(text,result)

print("Ví dụ dữ liệu X_train_raw: ")
for index in range(10):
    print(X_train_raw[index])

print("Ví dụ dữ liệu y_train: ")
for index in range(10):
    print(y_train[index])

print("Ví dụ dữ liệu X_test_raw: ")
for index in range(10):
    print(X_test_raw[index])

print("Ví dụ dữ liệu y_test: ")
for index in range(10):
    print(y_test[index])

'''
Xây dựng các vector
return n sample and n feauture
'''
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_train_raw)
X_test = vectorizer.transform(X_test_raw)

print("Ví dụ dữ liệu X_train: ")
for index in range(1):
    print(X_train[index])

print("Ví dụ dữ liệu X_test: ")
for index in range(1):
    print(X_test[index])

# model creation and training
classifier = LogisticRegression()
classifier.fit(X_train, y_train)
predictions = classifier.predict(X_test)

print("classifier LogisticRegression: ")
print(classifier)

print("Độ chính xác trong test data: ")

score = classifier.score(X_test, y_test)
print("Accuracy:", score*100)

