from pandas import Series,DataFrame
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import csv

csv_file = open("train_loss.csv")
val_file = open("val_loss.csv")
csv_reader = csv.reader(csv_file)
val_reader = csv.reader(val_file)
csv_data = list(csv_reader)
val_data = list(val_reader)

x = list()
y = list()

x1 = list()
y1 = list()


for i in range(1, 201):
    x.append(float(csv_data[i][0]))
    y.append(float(csv_data[i][1]))

for i in range(1, 41):
    x1.append(float(val_data[i][0]))
    y1.append(float(val_data[i][1]))

print(x1)
print(y1)

x_major_locator = MultipleLocator(20)
y_major_locator = MultipleLocator(5)

ax = plt.gca()
ax.xaxis.set_major_locator(x_major_locator)
ax.yaxis.set_major_locator(y_major_locator)

plt.xlim(0, 200)
plt.ylim(0, 50)

plt.plot(x, y, label="train loss")
plt.plot(x1, y1, c="red", label="val loss")

#X,Y轴标签
plt.xlabel("epoch", fontsize=14)
plt.ylabel("loss", fontsize=14)
plt.title("Loss", fontsize=14)

plt.legend()
plt.show()






