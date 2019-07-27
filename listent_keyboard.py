from pynput.keyboard import Key, Listener


def on_press(key):
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


# 连接事件以及释放
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
