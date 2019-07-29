import socket
host = "10.64.83.186"
port = 5053

if __name__ == '__main__':
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    c, addr = s.accept()
    while True:
        buf = c.recv(16)
        if buf:
            print(buf)
        if(b"esc" in buf):
            break
    s.close()
