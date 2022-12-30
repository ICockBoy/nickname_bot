import socket

host = "193.124.65.30"
port = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.sendall('code\r1&79873014530'.encode('utf-8'))
data = s.recv(1024)
print(str(data))
s.sendall('auth\r1&12345'.encode('utf-8'))
data = s.recv(1024)
print(str(data))
s.close()

