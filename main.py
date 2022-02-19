"""
main.py
"""

import utime
import machine
import ssd1306
from config import json_read, json_write

import gc
gc.collect()

# Hardware Setup

# setup OLED interface
i2c = machine.I2C(scl=machine.Pin(15), sda=machine.Pin(4))
OLED = ssd1306.SSD1306_I2C(128, 64, i2c)
LED = machine.Pin(25, machine.Pin.OUT)
PUMP = machine.Pin(14, machine.Pin.OUT)
INPUT = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_DOWN)

screen_interval = 1000

DATA = {'pump_on_min': 12, 'pump_on_sec':0, 'pump_off_min': 20, 'pump_off_sec': 0}

state = ['Off', 'On']
LATCH = {
    'state': 0,
    'interval': 1000,
    'curr_interval': 0
}
print(state)
# Function initilization
def print_screen(data1, data2, data3):
    """prints data to the OLED"""

    OLED.fill(0)
    OLED.text(data1, 0, 0)
    OLED.text(state[data2], 0, 20)
    OLED.text(state[data3], 0, 40)
    OLED.show()


def handle_interrupt(pin):
    global LATCH
    if not LATCH['state']:
        LATCH['curr_interval'] = utime.ticks_ms()
        print("Got Pin")
        output_toggle(PUMP)
        LATCH['state'] = 1
    else:
        print("Latched")
        print(LATCH)

INPUT.irq(trigger=machine.Pin.IRQ_RISING, handler=handle_interrupt)

def output_toggle(output):
    if output.value():
        output.value(0)
    else:
        output.value(1)

def main():
    """main loop function"""

    # Initilize local variables
    global data

    screen_start = utime.ticks_ms()

    if (not INPUT.value()) and LATCH['state']:
        print("Checking Time")
        if utime.ticks_diff(utime.ticks_ms(), LATCH['curr_interval']) > LATCH['interval']:
            print("Unlatching")
            LATCH['state'] = 0

    while 1:
        if utime.ticks_diff(utime.ticks_ms(), screen_start) > screen_interval:
            print_screen("Waiting", PUMP.value(), INPUT.value())
            output_toggle(LED)
            screen_start = utime.ticks_ms()

print_screen('Initializing...', 0, 0)
json_read(DATA)
main()
