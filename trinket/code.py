import board
import digitalio
import touchio
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

AUDIO = 0
VIDEO = 1
def cmd(opt):
  if opt == AUDIO:
    keyboard.press(Keycode.COMMAND, Keycode.SHIFT, Keycode.A)
    time.sleep(0.01)
    keyboard.release_all()

# Sleep to avoid a race
time.sleep(2)

# Set up the keyboard
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)  

# The status LED
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# For touch (testing)
touch = touchio.TouchIn(board.A0)

print("Waiting for key pin...")

while True:
  if touch.value:
    led.value = True
    cmd(AUDIO)
    
  else: 
    led.value = False

  time.sleep(0.25)
