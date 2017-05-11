import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# GPIO pin assignment
GREEN_LED = 21
RED_LED = 20
START_BLINK = 16
# GPIO pin initialization
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.output(GREEN_LED, False)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.output(RED_LED, False)
GPIO.setup(START_BLINK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Setup counters
COUNT = 0
# Setup variables
BLINKS = 10 # Set number of blinks
BLINK_PAUSE = 0.5 # Set time in seconds between blinks
TRIGGER_PAUSE = 3 # Set time in seconds needed to activate script once contact is made

def loop():
	global COUNT
	GPIO.output(GREEN_LED, True)
	GPIO.output(RED_LED, False)
	time.sleep(BLINK_PAUSE)
	GPIO.output(GREEN_LED, False)
	GPIO.output(RED_LED, True)
	time.sleep(BLINK_PAUSE)
	COUNT += 1
	while COUNT < BLINKS:
		loop()
	else:
		GPIO.cleanup()

def detect() :
	global SHUTDOWN_COUNT
	buttonState1 = True
	while buttonState1 == True :
		GPIO.wait_for_edge(TRIGGER, GPIO.FALLING)
		print "Edge detected"
		time.sleep(TRIGGER_PAUSE)
		buttonState1 = GPIO.input(TRIGGER)
		if buttonState1 == 0 :
			print "Excecuting"
			SHUTDOWN_COUNT = 0
			long_lead_loop()
		else :
			print "Maintain contact for 3 seconds"
			SHUTDOWN_COUNT += 1
			if SHUTDOWN_COUNT == 3 :
				finish()

def finish() :
	GPIO.cleanup()
	exit()

if __name__ == "__main__" :
	detect()