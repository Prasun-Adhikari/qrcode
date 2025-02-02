import numpy as np
from log_table import get_log_tables
from encode import bytestream
from log_table import get_generator_2

msize = 80
dsize = 20
tsize = 100

message = np.array(bytestream)[::-1].copy()
generator = get_generator_2(dsize)

message.resize(tsize)
generator.resize(tsize)
message = np.roll(message, dsize)


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

correction = remainder[:dsize][::-1]
message = np.array(bytestream).copy()
data = np.concatenate((message, correction))
