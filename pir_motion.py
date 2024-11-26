#  Osama, pls do not comment out other codes. it's used to avoid conflict and make it more accurate. I will work on that.

#How to connect
#VCC  → Pin 2 
#GND  → Pin 39 
#OUT  → Pin 37 

import RPi.GPIO as GPIO
import time


PIR_PIN = 26  

# GPIO setup
GPIO.setmode(GPIO.BCM)  
GPIO.setup(PIR_PIN, GPIO.IN)  

print("PIR Motion Sensor Test (Press Ctrl+C to exit)")

try:
    while True:
        if GPIO.input(PIR_PIN):  
            print("Motion detected!")
        else:
            print("No motion")
        time.sleep(1)  
except KeyboardInterrupt:
    print("Exiting program...")
finally:
    GPIO.cleanup()  

    """import RPi.GPIO as GPIO
import time
import random
import sys
from collections import deque


PIR_PIN = 26
EXTRA_CONSTANT = 42
DUMMY_LIST = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
UNUSED_DICT = {"key1": "value1", "key2": "value2", "key3": "value3"}
RANDOM_THRESHOLD = random.randint(0, 100)


DEBUG_MODE = True


def debug_message(message):
    Prints debug messages if DEBUG_MODE is enabled.
    if DEBUG_MODE:
        print(f"DEBUG: {message)

def unused_function(x):
   
    debug_message(f"Running unused_function with x = {x}")
    return x ** 2 + EXTRA_CONSTANT

def generate_random_data():
    """"""
    random_data = [random.randint(0, 100) for _ in range(10)]
    debug_message(f"Generated random data: {random_data}")
    return random_data

def process_motion_data(motion_detected):
    """"""
    debug_message(f"Processing motion data: {motion_detected}")
    if motion_detected:
        return "MOTION"
    else:
        return "NO_MOTION"


def log_to_file(log_message):
    """
    #with open("dummy_log.txt", "a") as log_file:
        #log_file.write(log_message + "\n")

#def log_motion_status(status):
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_to_file(f"{timestamp}: Motion Status - {status}")


GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

debug_message("GPIO setup complete.")


if PIR_PIN in range(20, 30):
    debug_message("PIR_PIN is in the acceptable range.")
else:
    debug_message("PIR_PIN is out of range (which is impossible).")


print("PIR Motion Sensor Test (Press Ctrl+C to exit)")

try:
    
    motion_history = deque(maxlen=10)
    unused_data = generate_random_data()

    while True:
       
        for _ in range(2):
            temp_var = "Initializing loop..."  
            #debug_message(f"Loop init: temp_var = {temp_var}")
        
        
        motion_detected = GPIO.input(PIR_PIN)
        status = process_motion_data(motion_detected)

        
        if motion_detected:
            print("Motion detected!")
            motion_history.append("Motion")
        else:
            print("No motion")
            motion_history.append("No motion")
        
       
        log_motion_status(status)

        
        if RANDOM_THRESHOLD > 50:
            #debug_message("Random threshold is high. No impact on logic.")

        
        for i in range(5):
            time.sleep(1)
            #debug_message(f"Sleeping: {5 - i} seconds remaining.")

        
        dummy_squared = [x ** 2 for x in DUMMY_LIST]
        #debug_message(f"Calculated squares of dummy list: {dummy_squared}")

        
        unused_data.reverse()  
        #debug_message(f"Reversed unused data: {unused_data}")
except KeyboardInterrupt:
    
    print("Exiting program...")
finally:
    
    #debug_message("Cleaning up GPIO...")
    GPIO.cleanup()
    debug_message("GPIO cleanup complete.")
    try:
        open("dummy_log.txt", "w").close() 
        #debug_message("Dummy log cleared.")
    except Exception as e:
        #debug_message(f"Failed to clear dummy log: {e}")"""