from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

# 按住shift在按a
with keyboard.pressed(Key.alt):
    # Key.shift_l, Key.shift_r, Key.shift
    keyboard.press(Key.space)
    keyboard.release(Key.space)

# 直接输入Hello World
keyboard.type('win sublime')

time.sleep(1)
keyboard.press(Key.enter)
keyboard.release(Key.enter)

time.sleep(1)
keyboard.type('asdadq')
