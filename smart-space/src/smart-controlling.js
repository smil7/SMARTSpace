// variables for selecting the buttons
const photo_button = document.getElementById('takePhotoBtn');
const rotate_motor_button = document.getElementById('rotateMotorBtn');
const adjust_temp_button = document.getElementById('adjustTempBtn');
const toggle_lights_button = document.getElementById('toggleLightsBtn');
const trigger_alarm_button = document.getElementById('triggerAlarmBtn');
console.log('after creating the variables');

const sendSMS = async () => {
    const data = {
      to: '', // Replace with the recipient's number
      body: 'INTRUDER IS WITHIN YOUR HOME!!!', // Your SMS text
    };
  
    try {
        console.log('before fetching');
      const response = await fetch('http://localhost:5000/send-sms', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      console.log('after fethcing');
      const result = await response.json();
      if (result.success) {
        console.log('SMS sent successfully!', result.message);
      } else {
        console.error('Failed to send SMS:', result.error);
      }
    } catch (error) {
      console.error('Error connecting to server:', error);
    }
};

const sendEmail = async () => {
    const msg = {
        to: '', // Change to your recipient
        from: '', // Change to your verified sender
        subject: 'IMPORTANT WARNING!!!',
        text: 'INTRUDER IS WITHIN YOUR HOME!!!',
    };

    try {
        const response = await fetch('http://localhost:5000/send-email', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(msg),
        });
    
        const result = await response.json();
        if (result.success) {
          console.log('Email sent successfully!', result.message);
        } else {
          console.error('Failed to send Email:', result.error);
        }
      } catch (error) {
        console.error('Error connecting to server:', error);
      }
};

// Initialize PubNub
const channel_sending = "";
const pubnub = new PubNub({
    publishKey: '',  
    subscribeKey: '',
});

console.log('Starting to receive messages');


pubnub.subscribe({
    channels: ['']
});

pubnub.addListener({
    // Messages
    message: function (m) {
      const received_msg = {
        channelName: m.channel,
        pubTT: m.timetoken,
        msg: m.message,
        publisher: m.publisher
      }
      console.log(received_msg);
      if (received_msg.msg.action === 'alertTrigger'){
        sendSMS();
        sendEmail();
      }
    },
});

// Take Photo Button
photo_button.addEventListener('click', function() { 
    console.log('Capturing a photo...') 
    pubnub.publish({
        channel: channel_sending,
        message: { action: "Capturing a photo..." }
    }, function(status, response) {
        if (status.error) {
            alert("Failed to send photo request. Please try again.");
        } else {
            alert("Photo request sent successfully!");
            console.log('Photo captured!')
            // Send an sms
            sendSMS();
            sendEmail();
        }
    });
});

// Rotate Motor Button
rotate_motor_button.addEventListener('click', function() {  
    pubnub.publish({
        channel: channel_sending,
        message: { action: "rotateMotor" }
    }, function(status, response) {
        if (status.error) {
            alert("Failed to send motor rotation request. Please try again.");
        } else {
            alert("Motor rotation request sent successfully!");
        }
    });
});

// Adjust Temperature Button
adjust_temp_button.addEventListener('click', function() {  
    pubnub.publish({
        channel: channel_sending,
        message: { action: "adjustTemperature", value: "optimal" }
    }, function(status, response) {
        if (status.error) {
            alert("Failed to send temperature adjustment request. Please try again.");
        } else {
            alert("Temperature adjustment request sent successfully!");
        }
    });
});

// Toggle Lights Button
toggle_lights_button.addEventListener('click', function() {  
    pubnub.publish({
        channel: channel_sending,
        message: { action: "toggleLights" }
    }, function(status, response) {
        if (status.error) {
            alert("Failed to send lights toggle request. Please try again.");
        } else {
            alert("Lights toggle request sent successfully!");
        }
    });
});

// Trigger Alarm Button
trigger_alarm_button.addEventListener('click', function() {  
    pubnub.publish({
        channel: channel_sending,
        message: { action: "triggerAlarm" }
    }, function(status, response) {
        if (status.error) {
            alert("Failed to send alarm trigger request. Please try again.");
        } else {
            alert("Alarm trigger request sent successfully!");
        }
    });
});
