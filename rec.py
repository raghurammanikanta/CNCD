import socket

def xor(a, b):
    result = []
    for i in range(len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
    return "".join(result)

def mod2div(dividend, divisor):
    pick = len(divisor)
    tmp = dividend[0:pick]

    while pick < len(dividend):
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + dividend[pick]
        else:
            tmp = xor('0' * pick, tmp) + dividend[pick]
        pick += 1

    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0' * pick, tmp)

    return tmp

def decodeData(data, key):
    appended_data = data
    remainder = mod2div(appended_data, key)
    return remainder

s = socket.socket()
print("Socket successfully created")

port = 1240
s.bind(("", port))
print("Socket binded to %s" % port)

s.listen(5)
print("Socket is listening")

while True:
    c, addr = s.accept()
    print('Got connection from', addr)

    data = c.recv(1024).decode()
    print("Received encoded data in binary format:", data)

    # Split data and key using a known separator
    if "|" in data:
        encoded_data, key = data.split("|")
        print("Received Key:", key)
    else:
        print("Invalid data format. Expecting 'data|key'")
        c.close()
        continue

    if not encoded_data:
        break

    ans = decodeData(encoded_data, key)
    print("Remainder after decoding is -> " + ans)

    temp = "0" * (len(key) - 1)
    if ans == temp:
        msg = encoded_data[:-(len(key) - 1)]
        z = ""
        for x in range(0, len(msg), 7):
            m = msg[x:x + 7]
            z += chr(int(m, 2))
        print(z)
        c.sendto(("Thank you Data -> " + encoded_data + " Received No error found").encode(), addr)
    else:
        c.sendto(("Error in data").encode(), addr)
    
    c.close()

