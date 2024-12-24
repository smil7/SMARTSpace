# SMARTSpace
SMARTSpace is an IoT Smart Environmental Control System capable of monitoring, adjusting, and securing a given space such as home or offices. 

## Architecture Overview
![image](https://github.com/user-attachments/assets/de607e1f-fbe9-4e4e-bab7-df190ab1f0bc)

Reading the below description, you will notice that there aren't any explanation or step-by-step guide of how the sensors are connected to the Raspberry Pi 4. We decided to leave this to the reader who decided to expand on our project.

## Backend
A simple backend is designed using NodeJS with the Express framework.

To run the backend successfully, you need to download NodeJS and npm libraries. NPM is a library that allows you to install dependinces to your Javascript projects. Using npm, you can install express, cors (cross-origin resource sharing), body-parser, and twilio (an api that allows you to send notifications to your phones and it provides other services as well). After downloading those libraries, you can run the `server.js` by running the following command (assuming you are in the parent directory):
`node ./src/server.cjs`.

## Frontend
The front-end is a simple UI developed using Vanilla HTML/CSS/Javascript.

To run the front-end successfully as well, you need to download vite. Vite is a tool that facilitates the process of building front-end applications (https://vite.dev/). Please read its documentations as it will help you in downloading the tool and guide you on how to use it. After going through the documentation you should be able to start running the front-end code. When you want to run the project on vite, go to the root directory of this repo then run the following command:
`npm run dev`

By Running this command, it should provide you with a local host link that enables you to interact with the user interface.

## Hardware
The "Explanation.txt" file explains how to run the files that are related to the hardware components which are connected to Raspberry Pi 4.

## Future Plans
•	Designing and building a database that stores the new registered users and checks if weather the user is logging in are already registered.

•	Connecting more microcontrollers and mechanical arms to manage and handle the windows limitations.

•	Training an Object Detection Model on the same dataset to be able to track the person in live feed video using the Pi Camera.

•	Quantisize the size of the model to be able to be installed on the Raspberry Pi. 
