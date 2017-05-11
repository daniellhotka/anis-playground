import time
from time import strftime, localtime
import picamera
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# GPIO pin assignment
GREEN_LED = 21
RED_LED = 20
TRIGGER = 16
# GPIO pin initialization
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.output(GREEN_LED, False)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.output(RED_LED, False)
GPIO.setup(TRIGGER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Setup counters
LED_COUNT = 0 
SHOT_COUNT = 0
CAMERA_COUNT = 0
SHUTDOWN_COUNT = 0
# Setup variables
LONG_BLINKS = 5 # Set number of blinks
SHORT_BLINKS = 2 # Set number of blinks between shots
CAMERA_SHOTS = 3 # Set number of shots in the sequence
BLINK_PAUSE = 0.5 # Set time in seconds between blinks
TRIGGER_PAUSE = 3 # Set time in seconds needed to activate script once contact is made

# New instance of camera object
camera = picamera.PiCamera()
# Fix camera being upside down
camera.vflip = True
camera.hflip = True
# Set resolution of photos
camera.resolution = (3280, 2464)

def lead_loop(dur) :
	# Blinks a red LED as countdown, duration swaps between two options
	global LED_COUNT
	DURATION = {'short': SHORT_BLINKS, 'long': LONG_BLINKS} # Duration options
	print "Taking photo in " + str(DURATION[dur] - LED_COUNT) + " seconds"
	GPIO.output(RED_LED, True)
	time.sleep(BLINK_PAUSE)
	GPIO.output(RED_LED, False)
	time.sleep(BLINK_PAUSE)
	LED_COUNT += 1
	while LED_COUNT < DURATION[dur] :
		lead_loop(dur)
	else:
		take_shot()

def take_shot() :
	# Turns on green LED, takes photo and turns off the LED
	global LED_COUNT, SHOT_COUNT, CAMERA_COUNT
	print "Taking photo"
	GPIO.output(GREEN_LED, True)
	CAPTURE_TIME = strftime("%Y%m%d_%H%M%S", localtime())
	camera.capture('image_'+CAPTURE_TIME+'.jpg')
	GPIO.output(GREEN_LED, False)
	SHOT_COUNT += 1
	CAMERA_COUNT += 1
	LED_COUNT = 0
	time.sleep(1)
	while SHOT_COUNT < CAMERA_SHOTS :
		lead_loop('short')
	else :
		SHOT_COUNT = 0
		print "\nSequence finished"
		print "\nReady for new trigger"
		detect()

def relay() :
	

def detect() :
	global SHUTDOWN_COUNT
	buttonState1 = True
	while buttonState1 == True :
		# Waits for button press
		GPIO.wait_for_edge(TRIGGER, GPIO.FALLING)
		print "\nButton pressed, hold for 3 seconds"
		time.sleep(TRIGGER_PAUSE)
		buttonState1 = GPIO.input(TRIGGER)
		# Is button still pressed?
		if buttonState1 == 0 :
			print "\nStarting image sequence\n"
			SHUTDOWN_COUNT = 0
			time.sleep(1)
			lead_loop('long')
		else :
			print "Please hold button for 3 seconds"
			SHUTDOWN_COUNT += 1
			if SHUTDOWN_COUNT == 3 :
				# If pressed incorrectly 3 straight times, quit
				print "\nExit sequence input, shutting down"
				finish()

def finish() :
	GPIO.cleanup()
	exit()

if __name__ == "__main__" :
	print "\nWelcome to Ani's Camera Booth"
	print "Press and hold button for 3 seconds to start image sequence"
	detect()
