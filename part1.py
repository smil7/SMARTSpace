import RPi.GPIO as GPIO
import time
from huskylib import HuskyLensLibrary
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.exceptions import PubNubException
import json
import threading

# Pin configuration
PIR_PIN = 26  # PIR GPIO 26
TRIG_PIN = 23  # HC-SR04 Trig GPIO 23
ECHO_PIN = 24  # HC-SR04 Echo GPIO 24
BUZZER_PIN = 17  # Buzzer signal pin GPIO 17
LED_PIN = 27  # LED GPIO 27

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)


hl = HuskyLensLibrary("I2C", "", address=0x32)


pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-620cd7f5-5e59-4989-b30e-277c71e0eda7'
pnconfig.publish_key = 'pub-c-eb38bccb-ad8b-4f13-a4c7-47776d9dbb8a'
pnconfig.uuid = 'smily'
pnconfig.ssl = False
pubnub = PubNub(pnconfig)

channel = 'smily'

# Shared state variables
motion_detected = False
distance_below_threshold = False
husky_no_objects_detected = False
distance_threshold_cm = 3

# Function to measure distance using the HC-SR04
def measure_distance():
    global distance_below_threshold
    while True:
        # Trigger the sensor
        GPIO.output(TRIG_PIN, True)
        time.sleep(0.00001)  # 10 microseconds
        GPIO.output(TRIG_PIN, False)
        
        # Wait for echo to go HIGH (start of echo pulse)
        pulse_start = None
        start_time = time.time()
        while GPIO.input(ECHO_PIN) == 0:
            pulse_start = time.time()
            if time.time() - start_time > 0.02:  # Timeout after 20 ms
                break  # Timeout
        
        # Wait for echo to go LOW (end of echo pulse)
        start_time = time.time()
        while GPIO.input(ECHO_PIN) == 1:
            pulse_end = time.time()
            if time.time() - start_time > 0.02:  # Timeout after 20 ms
                break  # Timeout

        if pulse_start and pulse_end:
            # pulse duration...
            pulse_duration = pulse_end - pulse_start

            # I Calculate the distance (in cm) 
            distance = (pulse_duration * 34300) / 2

            if distance < distance_threshold_cm:
                distance_below_threshold = True
            else:
                distance_below_threshold = False

        time.sleep(0.1)  # Slight delay to prevent CPU overuse

# Function to monitor motion using PIR sensor
def monitor_pir():
    global motion_detected
    while True:
        if GPIO.input(PIR_PIN):
            print("Motion detected!")
            motion_detected = True
        else:
            motion_detected = False
        time.sleep(0.1)  # Slight delay to prevent CPU overuse

# Function to monitor HuskyLens for object detection
def monitor_husky():
    global husky_no_objects_detected
    while True:
        try:
            detected_objects = hl.learnedBlocks()

            # Ensure detected_objects is iterable and not empty
            if not isinstance(detected_objects, list):
                detected_objects = [detected_objects] if detected_objects else []

            if not detected_objects:  # If no objects are detected by HuskyLens
                husky_no_objects_detected = True
                print("No objects are detected by HuskyLens.")
            else:
                husky_no_objects_detected = False

        except IndexError:
            
            print("working...")
            husky_no_objects_detected = True

        time.sleep(0.1)  # Delay to prevent CPU overuse

# Function to manage the main alert logic
def main_logic():
    while True:
        # Check if all three conditions are met
        if motion_detected and distance_below_threshold and husky_no_objects_detected:
            print("Motion detected, distance < 3 cm, and no objects detected")

            # Prepare data for PubNub
            message = {
                "alert": "triggerAlarm",
                "timestamp": time.time()
            }

            # Publish to PubNub
            try:
                pubnub.publish().channel(channel).message(message).sync()
                print(f"Published: {message}")

                
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
                GPIO.output(LED_PIN, GPIO.HIGH)
                time.sleep(5)  # Keep buzzer and LED on for 5 seconds
                GPIO.output(BUZZER_PIN, GPIO.LOW)
                GPIO.output(LED_PIN, GPIO.LOW)

            except PubNubException as e:
                print(f"Failed to publish message: {e}")

        time.sleep(0.1)  # Avoid tight loop

try:
    # Create and start threads
    distance_thread = threading.Thread(target=measure_distance, daemon=True)
    pir_thread = threading.Thread(target=monitor_pir, daemon=True)
    husky_thread = threading.Thread(target=monitor_husky, daemon=True)

    distance_thread.start()
    pir_thread.start()
    husky_thread.start()

    # Run the main logic in the main thread
    main_logic()

except KeyboardInterrupt:
    print("Exiting program...")
finally:
    GPIO.cleanup()


