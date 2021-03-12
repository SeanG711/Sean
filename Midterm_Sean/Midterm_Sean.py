# import modules and libraries
import time
import board
import adafruit_hcsr04
import neopixel
import digitalio
from digitalio import DigitalInOut, Direction, Pull
from simpleio import map_range


# declare objects and variables
# pir
pir = digitalio.DigitalInOut(board.A1)
pir.direction = digitalio.Direction.INPUT
pirPre = False
# sonic&breathing
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, auto_write=False)
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.A3, echo_pin=board.A2)
# breathingcolorvalueinitial
w = 20
# speed
a = 1
breath = [0, 0, 0]
breathInterval = 0.5
breathInterval1 = 0.5
breathTime = time.monotonic() + breathInterval
# distance
distanceTH = 150
S = sonar.distance
UltrasonicMode = False
# timer
timer = time.monotonic()
timerMode = False
# button
button = DigitalInOut(board.A6)
button.direction = Direction.INPUT
button.pull = Pull.UP
# color
B = 255
blue = [0, 0, B]
blueConstant = (0, 0, 150)
black = (0, 0, 0)
# blinking
blinkInterval = 0.5
blinkTime = time.monotonic() + blinkInterval

ledMode = 0

# loop foerver
while True:

    if not button.value:
        ledMode = 2
    else:
        # reset blinkTime
        blinkTime = time.monotonic()
        # use motion value to trigger the Ultrasonic sensor
        if pir.value:
            UltrasonicMode = True

        if UltrasonicMode:
            S = int(sonar.distance)
            # start timer
            if S > distanceTH and pir.value is False:
                ledMode = 0
                timerMode = True
            if S <= distanceTH:
                ledMode = 1
            if timerMode:
                # reset timer & Ultrasonic
                if time.monotonic() >= timer + 3:
                    timerMode = False
                    UltrasonicMode = False
            else:
                timerMode = False
                timer = time.monotonic()
        else:
            ledMode = 0
    # normal state
    if ledMode == 0:
        pixels.fill(blueConstant)
        pixels.show()
    # breathing
    if ledMode == 1:
        scaled_val = map_range(S, 0, 150, 5000, 1)
        breathInterval1 = breathInterval/scaled_val
        if time.monotonic() >= breathTime:
            breathTime += breathInterval1
            w += a
            if w > 40 or w < 2:
                a = -a        # dim
            breath = [0, 0, w]
            pixels.fill(breath)
            pixels.show()
    # blinking
    if ledMode == 2:
        blue = [0, 0, B]
        pixels.fill(blue)
        pixels.show()
        if time.monotonic() >= blinkTime:
            B = 255 - B
            blinkTime += blinkInterval

    time.sleep(0.01)


