import os
import numpy as np 
import matplotlib.pyplot as draw
from scipy import stats

#đọc file
os.chdir('/Users/windsora/LinearRegression')
filename1 = os.getcwd()+'/ex1data2.txt'
X1_lst = []
X2_lst = []
Y_lst = []
temp = []

with open(filename1, 'r+') as fileinput:
    filein = fileinput.readlines() #đọc từng dòng
    for line in filein:
        l = line.split(',')
        temp.append(l)

for i in temp:
    X1_lst.append(float(i[0]))
    X2_lst.append(float(i[1]))
    Y_lst.append(float(i[2]))

X01 = np.array([X1_lst]).T #size
X02 = np.array([X2_lst]).T #bedrooms
y = np.array([Y_lst]).T #price
m = np.size(X01) #number of features

#chuẩn hóa dữ liệu về dạng 0->1 (không theo z-score)
X1 = (X01 - np.min(X01))/(np.max(X01)- np.min(X01))
X2 = (X02 - np.min(X02))/(np.max(X02)- np.min(X02))

eta = 0.0001 #the learning rate

theta0 = 0
theta1 = 0
theta2 = 0
for i in range(10000):
    temp0 = theta0 - eta*np.sum(theta0+theta1*X1+theta2*X2 - y)/m
    temp1 = theta1 - eta*np.sum((theta0+theta1*X1+theta2*X2 - y)*X1)/m
    temp2 = theta2 - eta*np.sum((theta0+theta1*X1+theta2*X2 - y)*X2)/m
    theta0 = temp0
    theta1 = temp1
    theta2 = temp2 

Y = theta0 + theta1*X01 + theta2*X02

