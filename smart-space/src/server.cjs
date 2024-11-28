const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const twilio = require('twilio');

const app = express();

app.use(cors());
app.use(bodyParser.json());

const accountSid = 'AC664274fdccb8d3af224a9cb68388b096';
const authToken = '3e49094861c62c3db89d4635d6130f74';
const client = twilio(accountSid, authToken);

app.post('/send-sms', async (req, res) => {
  const { to, body } = req.body;

  try {
    const message = await client.messages.create({
      body: body,
      from: '+16812305992', // Your Twilio number
      to: to,
    });
    res.json({ success: true, message: message.sid });
  } catch (error) {
    console.error('Error sending SMS:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});

