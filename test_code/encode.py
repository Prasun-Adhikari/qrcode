import numpy as np

text = "Hello World, This is a test"

data = ''
for char in text:
    data += f"{ord(char):08b}"

mode = '0100'
charcount = f"{len(text):08b}"
bitstream = mode + charcount + data

req_length = 8*80

if len(bitstream) < req_length:
    bitstream += '0000'
if len(bitstream) < req_length:
    bitstream += '0'*((-len(bitstream))%8)  

patter = f"{0xEC:08b}", f"{0x11:08b}"

i = 0
while len(bitstream) < req_length:
    bitstream += patter[i]
    i = 1 - i

bytestream = []
for index in range(0, len(bitstream), 8):
    bytestream.append(int(bitstream[index: index+8], base=2))
message = np.array(bytestream)[::-1]

# print(message)