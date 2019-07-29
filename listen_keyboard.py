from pynput.keyboard import Key, Listener
import socket
import threading
import re

localHost = "10.64.83.12"
transferHost1 = "10.64.83.12"
transferHost2 = "10.64.83.186"
receivePort1 = 5051
receivePort2 = 5052

transferPort = 5053
receiveSocket = [None] * 2
transferSocket = [None] * 2
target = 0

receiveSocket[0] = socket.socket()
receiveSocket[0].bind((localHost, receivePort1))
receiveSocket[0].listen(5)
receiveSocket[1] = socket.socket()
receiveSocket[1].bind((localHost, receivePort2))
receiveSocket[1].listen(5)
transferSocket[0] = socket.socket()
transferSocket[0].connect((transferHost1, transferPort))
transferSocket[1] = socket.socket()
transferSocket[1].connect((transferHost2, transferPort))


def receive(number):
    global target
    global receiveSocket
    c, addr = receiveSocket[number].accept()
    while True:
        result = c.recv(20).decode()
        if result == "True":
            target = number
            print("change target :", target)


def on_press(key):
    global transferSocket
    global target
    key = str(key).encode()
    transferSocket[target].send(key)
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
    receiveThread = [None] * 2
    receiveThread[0] = threading.Thread(target=receive, args=(0,))
    receiveThread[0].setDaemon(True)
    receiveThread[0].start()
    receiveThread[1] = threading.Thread(target=receive, args=(1,))
    receiveThread[1].setDaemon(True)
    receiveThread[1].start()
    transfer()
