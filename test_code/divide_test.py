import numpy as np
from log_table import get_log_tables

text = "Hello!"
text += ' '*(8-len(text))
message = np.array([ord(char) for char in text][::-1])

message = np.array([32, 91, 11, 120, 209, 114, 220, 77, 67, 64, 236, 17, 236, 17, 236, 17][::-1])
generator_i = np.array([0, 251, 67, 46, 61, 118, 70, 64, 94, 32, 45][::-1])
antilog, log = get_log_tables()
generator = antilog[generator_i]

msize = 16
dsize = 10
tsize = 26

message.resize(tsize)
generator.resize(tsize)
message = np.roll(message, dsize)


# def scalar_multiply(arr, n):
#     return antilog[(log[arr] + log[n]) % 255]


def multiply(n1, n2):
    if n1 == 0 or n2 == 0:
        return 0
    antilog, log = get_log_tables()
    return antilog[(log[n1] + log[n2]) % 255]

            
remainder = message
for j in range(msize):
    k = tsize - j - 1
    ak = remainder[k]
    shifted_generator = np.roll(generator, k - dsize)
    remainder = remainder ^ np.array([multiply(num, ak) for num in shifted_generator])
    
print(remainder[:dsize][::-1])