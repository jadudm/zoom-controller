import board
import digitalio
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
import neopixel

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3, auto_write=False)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

AUDIO = 0
VIDEO = 1
EMERGENCY = 2

def cmd(b):
  if b.get('command') == AUDIO:
    pixel.fill(b.get('color'))
    pixel.show()
    keyboard.press(Keycode.COMMAND, Keycode.SHIFT, Keycode.A)
    time.sleep(0.01)
    keyboard.release_all()
  if b.get('command') == VIDEO:
    pixel.fill(b.get('color'))
    pixel.show()
    keyboard.press(Keycode.COMMAND, Keycode.SHIFT, Keycode.V)
    time.sleep(0.01)
    keyboard.release_all()
  if b.get('command') == EMERGENCY:
    pixel.fill(b.get('color'))
    pixel.show()
    keyboard.press(Keycode.COMMAND, Keycode.SHIFT, Keycode.V)
    time.sleep(0.01)
    keyboard.press(Keycode.COMMAND, Keycode.SHIFT, Keycode.A)
    time.sleep(0.01)
    keyboard.press(Keycode.COMMAND, Keycode.W)
    time.sleep(0.01)
    keyboard.release_all()

# Sleep to avoid a race
time.sleep(2)

# Set up the keyboard
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)  

# The status LED
# led = digitalio.DigitalInOut(board.D13)
# led.direction = digitalio.Direction.OUTPUT

# Audio button
class Button:
  def __init__(self):
    self.h = {}

  def set (self, k, v):
    self.h[k] = v
  def get (self, k):
    return self.h[k]

objs = []
buttons = [board.D3, board.D4, board.D5]
commands = [EMERGENCY, AUDIO, VIDEO, ]
colors = [RED, GREEN, BLUE]

print("Setting up buttons...")
for i in range(3):
  b = Button()
  b.set('obj', digitalio.DigitalInOut(buttons[i]))
  b.set('color', colors[i])
  b.set('command', commands[i])
  objs.append(b)

for b in objs:
  b.get('obj').direction = digitalio.Direction.INPUT

print("Quieting Neopixel...")
pixel.fill((0,0,0))
pixel.show()

print("Grabbing the time...")
lastcheck = time.monotonic()

print("Waiting for key pin...")
while True:
  if time.monotonic() > lastcheck + 3:
    pixel.fill((0,0,0))
    pixel.show()

  for b in objs:
    if not b.get('obj').value:
      cmd(b)
      lastcheck = time.monotonic()

  time.sleep(0.05)
