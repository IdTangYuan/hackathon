import socket
import threading
host = "10.64.83.12"
port = 5052


def receive():
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


if __name__ == '__main__':
    # t1 = threading.Thread(target=f1,args=(111,112))
