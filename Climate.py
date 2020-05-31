import RPi.GPIO as GPIO
import time
import sys
import Adafruit_DHT
import LCD1602

SensPin = 7
RelayPin = 11 #not right pin maybe pin16
LightsOff = False
OffTemp = 39

def setup():
    GPIO.setwarnings(False)
    LCD1602.init(0x27, 1)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SensPin, GPIO.OUT)
    #GPIO.setup(RelayPin, GPIO.OUT)

def loop():
    global LightsOff
    global OffTemp
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(11, 4)
        if humidity is not None and temperature is not None:
            if temperature > OffTemp:
                #GPIO.output(RelayPin, GPIO.LOW)
                LightsOff = True
                LCD1602.clear()
                LCD1602.write(0, 0, 'High temp!!!')
                LCD1602.write(0, 1, 'Temp=%.0fC' %temperature)
                time.sleep(3)
            elif temperature < OffTemp:
                LCD1602.clear()
                LCD1602.write(0, 0, 'Temp=%.0fC' %temperature)
                LCD1602.write(0, 1, 'Humidity=%.0f%%' %humidity)
        else:
            LCD1602.write(0, 0, 'Reading Failed')
            LCD1602.write(0, 1, 'Trying again...')
        time.sleep(20)

def destroy():
    GPIO.output(SensPin, GPIO.HIGH)
   # GPIO.output(RelayPin, GPIO.HIGH)
    GPIO.cleanup()
    LCD1602.clear()

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()
