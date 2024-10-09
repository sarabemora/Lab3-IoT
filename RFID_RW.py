import RPi.GPIO as GPIO
import MFRC522
import signal
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
continue_reading = True

def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

signal.signal(signal.SIGINT, end_read)
# Create the reader object
MIFAREReader = MFRC522.MFRC522()
reader = SimpleMFRC522()

def read():
    id,text = reader.read()
    return text

def write(text):
    reader.write(text)
