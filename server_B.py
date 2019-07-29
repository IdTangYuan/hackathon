import socket
from pynput.keyboard import Key, Controller
host = "10.64.83.186"
port = 5053

if __name__ == '__main__':
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    c, addr = s.accept()
    while True:
        buf = c.recv(16)
        print(buf.decode().__len__())
        if buf.decode().__len__() == 3:
            keyboard.press(buf.decode()[1])
            keyboard.release(buf.decode()[1])
        if(b"esc" in buf):
            break
    s.close()
