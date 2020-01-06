import os
import numpy as np 
import matplotlib.pyplot as draw

#đọc file
os.chdir('/Users/windsora/LinearRegression')
filename1 = os.getcwd()+'/ex1data1.txt'
X_lst = []
Y_lst = []
temp = []

with open(filename1, 'r+') as fileinput:
    filein = fileinput.readlines() #đọc từng dòng
    for line in filein:
        l = line.split(',')
        temp.append(l)

for i in temp:
    X_lst.append(float(i[0]))
    Y_lst.append(float(i[1]))

#matrix X is the population of a city
X = np.array([X_lst]).T #vì lưu dưới dạng array list của numpy nên ta phải chuyển vị nó để tính toán

#matrix Y is the profit of a food truck in that city
y = np.array([Y_lst]).T

#a) Vẽ đồ thị
draw.plot(X, y, 'rx')
draw.xlabel('population of a city')
draw.ylabel('profit of a food truck in that city')
draw.show()

#b) Implementing gradient descent
#building the model
theta0 = 0
theta1 = 0
m = len(X)
eta = 0.0001 #the learning rate
for i in range(10000):
    temp0 = theta0 - eta*np.sum(theta0+theta1*X - y)/m
    temp1 = theta1 - eta*np.sum((theta0+theta1*X - y)*X)/m
    theta0 = temp0
    theta1 = temp1

Y_ = theta0 + theta1*X
draw.plot(X, y, 'rx')
draw.plot([min(X), max(X)], [min(Y_), max(Y_)])
draw.xlabel('population of a city')
draw.ylabel('profit of a food truck in that city')
draw.show()