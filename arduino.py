import serial
import time
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback


arduino_port = '/dev/serial0'  
baud_rate = 9600


try:
    arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
    time.sleep(2)  
    print(f"Connected to Arduino on {arduino_port}")
except Exception as e:
    print(f"Failed to connect to Arduino: {e}")
    exit()


pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-620cd7f5-5e59-4989-b30e-277c71e0eda7'
pnconfig.publish_key = 'pub-c-eb38bccb-ad8b-4f13-a4c7-47776d9dbb8a'
pnconfig.uuid = "smily"

pubnub = PubNub(pnconfig)

# PubNub callback to process incoming messages
class MySubscribeCallback(SubscribeCallback):
    def message(self, pubnub, message):
        try:
            command = message.message.get('command', '')
            print(f"Received message: {command}")

            if command.lower() == "manipulate window":
                print("Sending 'manipulate window' command to Arduino.")
                arduino.write((command + '\n').encode())  # Send command to Arduino
            else:
                print("Ignoring unrelated command.")
        except Exception as e:
            print(f"Error processing message: {e}")


pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('smily').execute()


try:
    print("Listening for PubNub messages and Arduino responses...")
    while True:
        if arduino.in_waiting > 0:
            response = arduino.readline().decode().strip()
            print(f"Arduino response: {response}")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    arduino.close()
    print("Closed serial connection to Arduino.")
