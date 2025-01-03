const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const twilio = require('twilio');
const sgMail = require('@sendgrid/mail');
sgMail.setApiKey(process.env.SENDGRID_API_KEY);
console.log(process.env.SENDGRID_API_KEY);

const app = express();

app.use(cors());
app.use(bodyParser.json());

const accountSid = '[Add your own account Sid]';
const authToken = '[Add your own authentication token]';
const client = twilio(accountSid, authToken);

app.post('/send-sms', async (req, res) => {
  const { to, body } = req.body;

  try {
    const message = await client.messages.create({
      body: body,
      from: '', // Your Twilio number
      to: to,
    });
    res.json({ success: true, message: message.sid });
  } catch (error) {
    console.error('Error sending SMS:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

app.post('/send-email', async (req, res) => {
  const msg = req.body;

  try{
    sgMail.send(msg);
    res.json({success: true});
  } catch (error) {
    console.error('Error sending Email:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});

