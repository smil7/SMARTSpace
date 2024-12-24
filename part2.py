import smbus2
import bme280 as bme280_library
import time
import RPi.GPIO as GPIO
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.exceptions import PubNubException

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-620cd7f5-5e59-4989-b30e-277c71e0eda7'
pnconfig.publish_key = 'pub-c-eb38bccb-ad8b-4f13-a4c7-47776d9dbb8a'
pnconfig.uuid = "smily"

pubnub = PubNub(pnconfig)

I2C_BUS = 1
BME280_ADDRESS = 0x76  # I2C address for BME280

# Servo motor which is used to manipulate the window
SERVO_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, 50)  #PWM frequency
servo.start(0)

# Create an instance of the SMBus
i2c = smbus2.SMBus(I2C_BUS)

# Load the BME280 calibration parameters
calibration_params = bme280_library.load_calibration_params(i2c, BME280_ADDRESS)

# Callback function to handle PubNub publish result
def publish_callback(result, status):
    if status.is_error():
        print("Publish failed: ", status)
    else:
        print("Message published successfully.")


def set_servo_angle(angle):
    duty_cycle = 2 + (angle / 18)
    GPIO.output(SERVO_PIN, True)
    servo.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)
    GPIO.output(SERVO_PIN, False)
    servo.ChangeDutyCycle(0)

# Initial window state
window_open = False

try:
    while True:
        # Read data from the BME280 sensor
        data = bme280_library.sample(i2c, BME280_ADDRESS, calibration_params)
        
        # Extract temperature, pressure, and humidity
        temperature = data.temperature
        pressure = data.pressure
        humidity = data.humidity
        
        # Print the values
        print(f"Temperature: {temperature:.2f} °C")
        print(f"Pressure: {pressure:.2f} hPa")
        print(f"Humidity: {humidity:.2f} %")
        print("-----------------------------")
        
        # Publish data to PubNub and control the servo based on conditions
        if humidity > 80 and not window_open:
            # Humidity condition has higher priority to open the window
            try:
                pubnub.publish().channel("smily").message("CLOSE").pn_async(publish_callback)
                set_servo_angle(90)  # Rotate the servo to open the window
                window_open = True
            except PubNubException as e:
                print("Error during publish: ", e)
        elif temperature < 20 and window_open and humidity <= 20:
            # Close the window if temperature is low and humidity is not high
            try:
                pubnub.publish().channel("smily").message("CLOSE").pn_async(publish_callback)
                set_servo_angle(0)  # Rotate the servo to close the window
                window_open = False
            except PubNubException as e:
                print("Error during publish: ", e)
        elif temperature > 35 and not window_open:
            # Open the window if temperature is high and humidity does not require closing
            try:
                pubnub.publish().channel("smily").message("CLOSE").pn_async(publish_callback)
                set_servo_angle(90)  # Rotate the servo to open the window
                window_open = True
            except PubNubException as e:
                print("Error during publish: ", e)
        
        # Wait for 2 seconds before reading again
        time.sleep(2)

except KeyboardInterrupt:
    # Cleanup GPIO and close the bus when done
    servo.stop()
    GPIO.cleanup()
    i2c.close()
    print("Program terminated.")
