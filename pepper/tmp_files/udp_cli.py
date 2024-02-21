from socket import*
pepper_s=socket(AF_INET, SOCK_DGRAM)
pepper_s.bind(('localhost',1231))
while True:
    buf1, addr=pepper_s.recvfrom(100)
    print(buf1)
