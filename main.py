from encode import encode_text, correction_code
from generate_qr import generate_qr

input_str = input("Enter string: ")

# generate qr code
message = encode_text(input_str)
data = correction_code(message)
qrcode = generate_qr(data)

# Display qr code to the terminal
black = chr(0x2b1b)
white = chr(0x2b1c)

print(white * 35)
for line in qrcode:
    print(white, end='')
    for char in line:
        if char:
            print(white, end='')
        else:
            print(black, end='')
    print(white)
print(white * 35)
print()
