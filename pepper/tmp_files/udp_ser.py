from socket import*
pepper_s=socket(AF_INET, SOCK_DGRAM)
pepper_s.bind(('localhost',1230))
while True:
    mes_S = input('msg: ')
    socket.sendall(mes_S.encode(encoding='utf-8'),('',1231))
