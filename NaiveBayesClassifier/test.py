import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk import word_tokenize
import collections
import math
'''
đọc file dữ liệu
'''
sms = pd.read_csv('spam.csv', encoding='latin-1')
sms = sms.drop(labels=["Unnamed: 2", "Unnamed: 3", "Unnamed: 4"], axis=1)
sms.columns = ["result", "text"]
'''
tách ra spam hoặc ham
'''
spam_sms = sms[sms["result"] == "spam"]["text"]
ham_sms = sms[sms["result"] == "ham"]["text"]

'''
- Loại bỏ những từ trong stop word trong tiếng anh
- Loại bỏ những kí tự đặc biệt
- Đưa về cùng loại viết thường
'''
spam_words = []
ham_words = []

def splitWordsSpam(spamSMS):
    global spam_words
    words = []
    for word in word_tokenize(spamSMS):
        if word.lower() not in stopwords.words('english'):
            if word.lower().isalpha():
                words.append(word.lower())
    spam_words = spam_words + words

def splitWordsHam(HamSMS):
    global ham_words
    words = []
    for word in word_tokenize(HamSMS):
        if word.lower() not in stopwords.words('english'):
            if word.lower().isalpha():
                words.append(word.lower())
    ham_words = ham_words + words

spam_sms.apply(splitWordsSpam)
ham_sms.apply(splitWordsHam)
spam_sms = np.array(spam_sms)
ham_sms = np.array(ham_sms)
'''
Chuyển các danh sách thành các vecrtor
'''
spam_words = np.array(spam_words)
ham_words = np.array(ham_words)


'''
Khởi tạo vector training x spam
công thức Multinomial Naive Bayes
p(xi/c) = (Nci + a)/(Nc + d.a)
'''
x_spam = collections.Counter(spam_words)
x_ham = collections.Counter(ham_words)

x_spam = x_spam.most_common()
x_ham = x_ham.most_common()

x_feature = []
for index in x_spam:
    index = list(index)
    x_feature.append(index)
num = len(x_feature)
for index in x_ham:
    index = list(index)
    x_feature.append(index)
'''
Tinh Nc
'''
sum_words = len(x_spam) + len(x_ham)
N_C_spam_da = len(spam_sms) + sum_words
N_C_ham_da = len(ham_sms) + sum_words
'''
Tính Nci
'''
x_feature_spam = []
a = 1
for index in range(num):
    x_feature_spam.append([x_feature[index][0], (1 + x_feature[index][1]) / N_C_spam_da])

for index in range(num, len(x_feature)):
    x_feature_spam.append([x_feature[index][0], (1) / N_C_spam_da])

x_feature_ham = []
for index in range(num):
    x_feature_ham.append([x_feature[index][0], (1) / N_C_ham_da])

for index in range(num, len(x_feature)):
    x_feature_ham.append([x_feature[index][0], (1 + x_feature[index][1]) / N_C_ham_da])


'''
Testing ...
'''
'''
đọc file dữ liệu
'''
sms = pd.read_csv('test.csv', encoding='latin-1')
sms = sms.drop(labels=["Unnamed: 2", "Unnamed: 3", "Unnamed: 4"], axis=1)
sms.columns = ["result", "text"]
y_test = sms["result"]
y_test = list(y_test)
y_test_vector = []
for index in y_test:
    if index == 'spam':
        y_test_vector.append(1)
    else:
        y_test_vector.append(0)
x_test = sms["text"]
x_test = list(x_test)

def splitWords(sms):
    words = []
    for word in word_tokenize(sms):
        if word.lower() not in stopwords.words('english'):
            if word.lower().isalpha():
                words.append(word.lower())
    words_collection = collections.Counter(words)
    words_tuple = list(words_collection.most_common())
    words_list = list()
    for index in words_tuple:
        words_list.append(list(index))
    return words_list

def createVector(words_list):
    global x_feature
    x_vector = list()
    for index in x_feature:
        x_vector.append(['0', 0])
    for index in range(len(words_list)):
        for pos in range(len(x_feature)):
            if words_list[index][0] == x_feature[pos][0]:
                x_vector[pos][0] = x_feature[pos][0]
                x_vector[pos][1] = words_list[index][1]
    return x_vector

def computeP(x_vector):
    global x_feature, x_feature_spam, x_feature_ham
    P_spam = len(spam_sms)/(len(spam_sms) + len(ham_sms))
    P_ham = len(ham_sms)/(len(spam_sms) + len(ham_sms))
    for index in range(len(x_vector)):
        if x_vector[index][0] == x_feature_spam[index][0]:
            P_spam = P_spam*math.pow(x_feature_spam[index][1], x_vector[index][1])
        else:
            P_spam = P_spam*x_feature_spam[index][1]

    for index in range(len(x_vector)):
        if x_vector[index][0] == x_feature_ham[index][0]:
            P_ham = P_ham*math.pow(x_feature_ham[index][1], x_vector[index][1])
        else:
            P_ham = P_ham*x_feature_ham[index][1]

    if P_spam > P_ham:
        return 1
    else:
        return 0

result = []
for words in x_test:
    words_list = splitWords(words)
    x_vector = createVector(words_list)
    p = computeP(x_vector)
    result.append(p)

temp = 0
for index in range(len(y_test_vector)):
    if y_test_vector[index] == result[index]:
        temp+=1
print('Độ dài đặc trưng:                        ', len(x_feature))
print('Độ dài đặc trưng của spam:               ', len(x_feature_spam))
print('Độ dài đặc trưng của ham:                ', len(x_feature_ham))
print('Vector y_testing(1 -> spam, 0 -> ham):   ', y_test_vector)
print('Ví dụ data phần tử đầu tiên x_test[0]:   ', x_test[0])
print('Cắt chuỗi và giữ lại các đặc trưng   :   ', splitWords(x_test[0]))
print('Chuyển thành vector phần tử đầu:         ', createVector(splitWords(x_test[0])))
print('Phần trăm đúng: ', temp/len(y_test_vector)*100)
'''
refence:
1. Bài 32: Naive Bayes Classifier - machine learning co ban
2. Bài 31: Maximum Likelihood và Maximum A Posteriori estimation
3. Collection Counter https://stackabuse.com/introduction-to-pythons-collections-module/
4. Numpy https://www.geeksforgeeks.org/python-numpy/
5. Data get in: https://www.kaggle.com/ishansoni/sms-spam-collection-dataset/
6. Tokenizer: https://www.kaggle.com/ishansoni/sms-spam-collection-dataset/notebook
'''
