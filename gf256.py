import numpy as np


def get_log_tables():
    antilog_table = np.zeros(255, dtype=int)
    log_table = np.zeros(256, dtype=int)
    antilog_table[0] = 1
    log_table[0] = -1
    for i in range(1, 255):
        next_num = antilog_table[i-1] * 2
        if next_num >= 2**8:
            next_num = next_num ^ 0b100011101
        antilog_table[i] = next_num
        log_table[next_num] = i

    return antilog_table, log_table


def multiply(n1, n2):
    if n1 == 0 or n2 == 0:
        return 0
    return antilog[(log[n1] + log[n2]) % 255]


def get_generator_poly(number):
    cur_pol = np.array([1])
    for k in range(number):
        multiplier_pol = np.array([antilog[k], 1], dtype=int)
        next_pol = np.zeros(len(cur_pol)+1, dtype=int)
        for i1, n1 in enumerate(cur_pol):
            for i2, n2 in enumerate(multiplier_pol):
                i = i1 + i2
                n = multiply(n1, n2)
                next_pol[i] = next_pol[i] ^ n
        cur_pol = next_pol
    return cur_pol


antilog, log = get_log_tables()
