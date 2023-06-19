import numpy as np                       
from matplotlib import pyplot as plt      
import time, sys 
from scipy import interpolate

data = []
rates_min = []
rates_max = []

with open('cum_poisson_length_client.txt') as fobj:
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


q = 50

for i in range(1, len(data)):
    x.append(float(data[i][0]))
    y.append(float(data[i][1]))

x_int = np.linspace(x[0], x[len(x) - 1], len(x))
f = interpolate.interp1d(x, y, kind='linear')
y_int = f(x_int)



buffer_sup = []
sup = []

print(int((12-1)/2))

for i in range(1, int(len(y_int)/2)):
    for j in range(int(len(y_int)/2)):
        buffer_sup.append(y_int[i + j] - y_int[j])
    sup.append(max(buffer_sup))
    buffer_sup.clear()

# print(sup[:50])

# a = max(sup)
# print(a)
print(sup[:50])


y_a = []

for i in range(len(sup)):
    y_a.append(x_int[i] * sup[i])

print("sup" + str(len(sup)))

S_a = np.trapz(sup[:499], x_int[:499])
print("S_a ")
print(S_a)
S_data = np.trapz(y[:499], x[:499])
print("S_data ")
print(S_data)

# f = open("alfa_white_noise_length.txt", "w")
# for i in range(499):
#     f.write(str(x_int[i]) + " " + str(sup[i]) + "\n")
# f.close()

plt.plot(x[:4999], y[:4999], 'b-', label="data")
plt.plot(x_int[:4999], sup[:4999], 'r-', label="convert")
plt.legend()
plt.xlabel('time')
plt.ylabel('length')
plt.title('Cauchy for length on client')
plt.show()