import machine
import network
import ssd1306
import time

LED = machine.Pin(25, machine.Pin.OUT)
I2CRESET = machine.Pin(16, machine.Pin.OUT)

I2CRESET.value(0)
LED.value(1)
time.sleep(2) # sleep for a bit
I2CRESET.value(1)
LED.value(0)
# setup OLED interface
i2c = machine.I2C(scl=machine.Pin(15), sda=machine.Pin(4))

oled_width = 128
oled_height = 64

oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
oled.fill(0)
oled.text("Booting", 0, 0)
oled.text("Acclimate v0.1", 0, 10)
oled.show()
