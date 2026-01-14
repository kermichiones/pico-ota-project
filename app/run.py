import time
from machine import Pin
import utils

# Example main script
print("Starting Pico W application...")

# Blink LED to indicate startup
utils.blink_led(3, 0.2)

# Main loop
led = Pin("LED", Pin.OUT)
while True:
    led.toggle()
    print("Heartbeat...")
    time.sleep(1)
