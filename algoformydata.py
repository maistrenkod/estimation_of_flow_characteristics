import numpy as np
from matplotlib import pyplot as plt
import time
import sys
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection


def a_koeff(x, y):
    n = len(x)
    return (n * sum(np.multiply(x, y)) - sum(x)*sum(y))/(n*sum(np.multiply(x, x)) - sum(x)*sum(x))


def updateCritical(p, c_max, c_min, n, x, y):
    if (y[n] < (p*(x[n] - x[c_max]) + y[c_max])):
        c_max = n
    elif (y[n] > (p*(x[n]-x[c_min]) + y[c_min])):
        c_min = n


def isLowerConstrained(T, p, n, c_min, x, y):
    if (y[n] >= (p*(x[n] - x[c_min] - T) + y[c_min])):
        return True
    else:
        return False


def isUpperConstrained(s, p, n, c_max, x, y):
    if (y[n] <= (p*(x[n] - x[c_max]) + s + y[c_max])):
        return True
    else:
        return False


data = []
rates_min = []
rates_max = []

data_alfa = []
x_alfa = []
y_alfa = []

with open('alfa_cauchy_length.txt') as fobj:
    for line in fobj:
        row = line.split()
        data_alfa.append(row[:])

x_alfa.append(float(data_alfa[0][0]))
y_alfa.append(float(data_alfa[0][1]))

for i in range(1, len(data_alfa)):
    x_alfa.append(float(data_alfa[i][0]))
    y_alfa.append(float(data_alfa[i][1]))

with open('cum_cauchy_length_client.txt') as fobj:
    for line in fobj:
        row = line.split()
        data.append(row[:])

print(type(data[0][0]))  # time
print(type(data[0][1]))  # length
print("data ")
print(len(data))

x = []
y = []

x.append(float(data[0][0]))
y.append(int(data[0][1]))
print("y ", y[0])


# q = len(data)
q = 50

for i in range(1, q):
    x.append(float(data[i][0]))
    y.append(float(data[i][1]))


step = 1
s = 1000
T = 0.01
p0 = 10000
print('p0 ', p0)

n = 0
c_max = 0
c_min = 0
p = p0
num_max = []
num_min = []
y_max = []
y_min = []
flag = 0

for i in range(len(x) - 1):
    n = n + 1
    flag = 0  # not zero if c_min/c_max changes
    if (not isLowerConstrained(T, p, n, c_min, x, y)):
        p = ((y[n] - y[c_max]))/(x[n]-x[c_max])
        c_max = n
        c_min = n
        flag = 3
    elif (not isUpperConstrained(s, p, n, c_max, x, y)):
        p = ((y[n] - y[c_min]))/(x[n]-x[c_min])
        c_max = n
        c_min = n
        flag = 3
    else:
        if (y[n] < (p*(x[n] - x[c_max]) + y[c_max])):
            c_max = n
            flag = 2
        elif (y[n] > (p*(x[n] - x[c_min]) + y[c_min])):
            c_min = n
            flag = 1
    if flag == 1 or flag == 3:
        rates_min.append((c_min, p))
    if flag == 2 or flag == 3:
        rates_max.append((c_max, p))

amax_x = []
amin_x = []
amax_y = []
amin_y = []
dx_max = 0.001
dx_min = 0.0005
dots_y =[]
dots_x = []
p = 0
n = 0
for tu in rates_max:
    n = tu[0]
    p = tu[1]
    amax_y.append(y[n] + s)
    amax_x.append(x[n])
    amax_y.append(p*dx_max+y[n] + s)
    amax_x.append(x[n]+dx_max)
    dots_y.append(y[n] + s)
    dots_x.append(x[n])

amax_y.append(p*(x[-1]-x[n])+y[n] + s)
amax_x.append(x[-1])

for tu in rates_min:
    n = tu[0]
    p = tu[1]
    amin_y.append(y[n])
    amin_x.append(x[n]+T)
    amin_y.append(p*dx_min+y[n])
    amin_x.append(x[n]+T+dx_min)
    dots_y.append(y[n])
    dots_x.append(x[n]+T)

fig, ax = plt.subplots(1, 1)

k = 0

# while(amax_x[k] < x[499]):
#     k = k + 1

# print("S_aurora ")
# S_aurora = np.trapz(amax_y[:k], amax_x[:k])
# print(S_aurora)

# S_data = np.trapz(y[:499], x[:499])
# print("S_data ")
# print(S_data)

plt.plot(x[1:], y[1:], 'r-o', label="data", markersize=2)
plt.plot(amax_x, amax_y, 'b-o', label="aurora_max", markersize=2)
plt.plot(amin_x, amin_y, 'g-o', label="aurora_min", markersize=2)
# plt.plot(x_alfa[:50], y_alfa[:50], 'g-', label="maxi+")
# plt.plot(dots_x, dots_y, 'ko', markersize=3)

ax.autoscale()

plt.xlabel('time')
plt.ylabel('length')
plt.title('Cauchy for length on client')
text = "s=" + str(s) + ", T=" + str(T)
plt.text(0.2, 110000, text)
plt.legend()
plt.show()
print(1)
