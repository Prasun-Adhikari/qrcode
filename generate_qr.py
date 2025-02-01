import numpy as np


def finder_pattern(qr, set_bits, i, j, buf_dir):
    di, dj = buf_dir
    qr[i-3:i+4, j-3:j+4] = 0
    qr[i-2:i+3, j-2:j+3] = 1
    qr[i-1:i+2, j-1:j+2] = 0
    qr[i+di*4, j-3:j+5] = 1
    qr[i-3:i+5, j+dj*4] = 1
    set_bits[i-3:i+4, j-3:j+4] = 1
    set_bits[i+di*4, j-3:j+5] = 1
    set_bits[i-3:i+5, j+dj*4] = 1


def alignment_pattern(qr, set_bits, i, j):
    qr[i-2:i+3, j-2:j+3] = 0
    qr[i-1:i+2, j-1:j+2] = 1
    qr[i, j] = 0
    set_bits[i-2:i+3, j-2:j+3] = 1


def timing_pattern(qr, set_bits, size):
    qr[6, 7:size-7:2] = 1
    qr[7:size-7:2, 6] = 1
    set_bits[6, :] = 1
    set_bits[:, 6] = 1


def reserve_format_bits(set_bits, size):
    for i in range(0, 8):
        if not set_bits[8, i]:
            set_bits[8, i] = 1
        if not set_bits[i, 8]:
            set_bits[i, 8] = 1
        set_bits[8, 8] = 1
        if not set_bits[size-i-1, 8]:
            set_bits[size-i-1, 8] = 1
        if not set_bits[8, size-i-1]:
            set_bits[8, size-i-1] = 1


def generate_pattern(size):
    i, j = size-1, size-1
    di = -1
    while True:
        yield i, j
        yield i, j-1
        i += di
        if i < 0 or i >= size:
            di = -di
            i += di
            j -= 2
            if j == 6:
                j -= 1
            if j < 0:
                break


def insert_format_data(format_data, qr, size):
    def format_location_1():
        i, j = size-1, 8
        for _ in range(7):
            yield i, j
            i -= 1
        i, j = 8, size-8
        for _ in range(8):
            yield i, j
            j += 1

    def format_location_2():
        i, j = 8, 0
        for _ in range(8):
            yield i, j
            j += 1
            if j == 6:
                j += 1
        i, j = 7, 8
        for _ in range(7):
            yield i, j
            i -= 1
            if i == 6:
                i -= 1

    # get locations for the format bits
    pat1, pat2 = format_location_1(), format_location_2()
    for char in format_data:
        p1, p2 = next(pat1), next(pat2)
        qr[p1] = 1 - int(char)
        qr[p2] = 1 - int(char)


def generate_qr(data):
    # Hardcode size for version 4
    size = 33
    qr = np.zeros((size, size), dtype=np.bool)
    set_bits = np.zeros((size, size), dtype=np.float64)

    # Finder pattern
    finder_pattern(qr, set_bits, 3, 3, (1, 1))
    finder_pattern(qr, set_bits, size-3-1, 3, (-1, 1))
    finder_pattern(qr, set_bits, 3, size-3-1, (1, -1))

    # Alignment pattern
    alignment_pattern(qr, set_bits, 26, 26)

    # Timing pattern
    timing_pattern(qr, set_bits, size)

    # Dark Module
    qr[size-8, 8] = 0
    set_bits[size-8, 8] = 1

    # Reserve format bits
    reserve_format_bits(set_bits, size)

    # Insert data according to pattern
    pattern = generate_pattern(size)
    for word in data:
        for char in f"{word:08b}":
            i, j = next(pattern)
            while set_bits[i, j] != 0:
                i, j = next(pattern)
            if i % 2 == 0:
                qr[i, j] = int(char)
            else:
                qr[i, j] = 1 - int(char)
            set_bits[i, j] = 1

    # Hard code mask bits (Mask pattern 1, ECC level L)
    format_mask_bits = '111001011110011'

    # Insert formmat data in reserved location
    insert_format_data(format_mask_bits, qr, size)

    return qr
