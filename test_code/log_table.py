import numpy as np

def get_log_tables():
    antilog_table = np.zeros(255, dtype=int)
    log_table = np.zeros(256, dtype=int)
    antilog_table[0] = 1
    log_table[0] = -1
    for i in range(1, 255):
        next = antilog_table[i-1] * 2
        if next >= 2**8:
            next = next ^ 0b100011101
        antilog_table[i] = next
        log_table[next] = i

    return antilog_table, log_table


def antisum(index1, index2):
    antilog_table, log_table = get_log_tables()
    if index1 != -1:
        n1 = antilog_table[index1] 
    else:
        n1 = 0
    n2 = antilog_table[index2]
    return log_table[n1 ^ n2]


def get_generator(number):
    cur_pol = np.array([0])
    for k in range(number):
        multiplier_pol = np.array([k,0], dtype=int)
        next_pol = np.ones(len(cur_pol)+1, dtype=int) * -1
        for i1, index1 in enumerate(cur_pol):
            for i2, index2 in enumerate(multiplier_pol):
                i = i1 + i2
                index = (index1 + index2) % 255
                next_pol[i] = antisum(next_pol[i], index)
        cur_pol = next_pol
    return cur_pol


def get_generator_2(number):
    antilog, log = get_log_tables()
    cur_pol = np.array([1])
    for k in range(number):
        multiplier_pol = np.array([antilog[k], 1], dtype=int)
        next_pol = np.zeros(len(cur_pol)+1, dtype=int)
        for i1, n1 in enumerate(cur_pol):
            for i2, n2 in enumerate(multiplier_pol):
                i = i1 + i2
                n = antilog[(log[n1] + log[n2]) % 255]
                next_pol[i] = next_pol[i] ^ n
        cur_pol = next_pol
    return cur_pol