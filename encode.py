import numpy as np
from gf256 import get_generator_poly, multiply


def encode_text(text):
    # use byte encoding on text
    data = ''
    for char in text:
        data += f"{ord(char):08b}"

    # prepend mode and character count info
    mode = '0100'
    charcount = f"{len(text):08b}"
    bitstream = mode + charcount + data

    # hard coded length for version 4 L
    req_length = 8*80

    # add terminator and pad with 0s to nearest byte
    if len(bitstream) + 4 <= req_length:
        bitstream += '0000'
    if len(bitstream) < req_length:
        bitstream += '0'*((-len(bitstream)) % 8)

    # add alternating patter bytes to pad the rest
    patter = f"{0xEC:08b}", f"{0x11:08b}"
    i = 0
    while len(bitstream) < req_length:
        bitstream += patter[i]
        i = 1 - i

    # convert bitstring to an array of bytes
    bytestream = []
    for index in range(0, len(bitstream), 8):
        bytestream.append(int(bitstream[index: index+8], base=2))

    return np.array(bytestream)


def correction_code(orig_message):
    # hardcoded message, correction code and total length for version 4 L
    msize = 80
    dsize = 20
    tsize = 100

    message = orig_message[::-1].copy()
    generator = get_generator_poly(dsize)

    # resize message and generator polynomials
    message.resize(tsize)
    generator.resize(tsize)
    message = np.roll(message, dsize)

    # find remainder when dividing message polynomial by generator polynomial
    remainder = message
    for j in range(msize):
        k = tsize - j - 1
        ak = remainder[k]
        shifted_generator = np.roll(generator, k - dsize)
        remainder = remainder ^ np.array([multiply(num, ak) for num in shifted_generator])

    correction = remainder[:dsize][::-1]
    return np.concatenate((orig_message, correction))
