import csv
import os
import glob
import pandas as pd
import numpy as np
from collections import Counter

'''
    BUI THANH PHONG - 51600063
    POS TAGGING
'''

'''
    TRAINING DATA
'''

# read file
# reference: https://www.programcreek.com/python/example/92/glob.glob
cwd = os.getcwd() + '/training/*.seg.pos'
list_file = glob.glob(cwd)
lst = []
for file_name in list_file:
    f = open(file_name, 'r')
    for line in f:
        line.strip()
        line = line.replace("\n", '')
        line = line.replace("//", '')
        lst.append(line)
    f.close()

lst = np.array(lst)
training_word = []
training_label = []
# chay toan bo dong` trong lst
for line in lst:
    # khoi tao chuoi word rong
    word = ''
    # khoi tao mang 1 chieu de luu word
    words = []
    # khoi tao mang 1 chieu de luu label
    labels = []
    # doc chuoi trong line
    for token in range(len(line)):

        word = word + line[token]
        word = word.lower()
        if (line[token] == '/'):
            words.append(word[:-1])
            word = ''
            pos_last_label = token

        if (line[token] == ' '):
            labels.append(word[:-1])
            word = ''

    labels.append(line[pos_last_label+1:])

    # luu du lieu vo mang 2 chieu
    training_word.append(words)
    training_label.append(labels)

# chuyen du lieu vo trong dict voi key la word va value la label
training_dict = {}
for line in range(len(training_word)):
    for word, label in zip(training_word[line], training_label[line]):
        if word not in training_dict.keys():
            training_dict.update({word: [label]})
        else:
            temp = training_dict[word]
            temp.append(label)
            training_dict.update({word: temp})

'''
    TAO MODEL
'''
# count du lieu
for word in training_dict:
    labels = training_dict[word]
    unique, counts = np.unique(labels, return_counts=True)
    temp = np.asarray((unique, counts)).T
    temp = temp.tolist()
    training_dict.update({word: temp})

# count lablel one gram
label_dict_onegram_count = {}
labels_all = []
for line in training_label:
    for label in line:
        labels_all.append(label)
# do mot so label khong hop le do traning data 1 so cho bi sai do thieu dau / hoac _
label_remove = []
unique, counts = np.unique(labels_all, return_counts=True)
for key, value in zip(unique, counts):
    if value > 10:
        label_dict_onegram_count.update({key: value})
    else:
        label_remove.append(key)
        label_remove = list(label_remove)

# remove label
for line in range(len(training_label)):
    for label in training_label[line]:
        if label in label_remove:
            training_label[line].remove(label)

# them stop vao label
for line in range(len(training_label)):
    temp = 'STOP'
    training_label[line].append(temp)

label_dict_trigram_count = {}
label_dict_bigram_count = {}

# create bigram
labels_bigram_all = []

for line in training_label:
    for label in range(len(line)-1):
        label_bigram = [line[label], line[label+1]]
        labels_bigram_all.append(label_bigram)

# count bigram
for labels in set(map(tuple, labels_bigram_all)):
    key = labels
    value = labels_bigram_all.count(list(labels))
    label_dict_bigram_count.update(
        {key: value})

# create trigram
labels_trigram_all = []

for line in training_label:
    for label in range(len(line)-2):
        label_trigram = [line[label], line[label+1], line[label+2]]
        labels_trigram_all.append(label_trigram)

# count bigram
for labels in set(map(tuple, labels_trigram_all)):
    key = labels
    value = labels_trigram_all.count(list(labels))
    label_dict_trigram_count.update(
        {key: value})

'''
    TESING
'''

'''
    TRAINING DATA
'''
# read file
# reference: https://www.programcreek.com/python/example/92/glob.glob
cwd = os.getcwd() + '/testing/*.seg.pos'
list_file = glob.glob(cwd)
lst = []
for file_name in list_file:
    f = open(file_name, 'r')
    for line in f:
        line.strip()
        line = line.replace("\n", '')
        line = line.replace("//", '')
        lst.append(line)
    f.close()

lst = np.array(lst)
testing_word = []
testing_label = []
# chay toan bo dong` trong lst
for line in lst:
    # khoi tao chuoi word rong
    word = ''
    # khoi tao mang 1 chieu de luu word
    words = []
    # khoi tao mang 1 chieu de luu label
    labels = []
    # doc chuoi trong line
    for token in range(len(line)):

        word = word + line[token]
        word.lower()
        if (line[token] == '/'):
            words.append(word[:-1])
            word = ''
            pos_last_label = token

        if (line[token] == ' '):
            labels.append(word[:-1])
            word = ''

    labels.append(line[pos_last_label+1:])

    # luu du lieu vo mang 2 chieu
    testing_word.append(words)
    testing_label.append(labels)

print(testing_word)


def viterbi(list_sequence, lamda=0.01, V=len(training_word)):
    resurt = ['']*len(list_sequence)
    p = [1]*len(list_sequence)
