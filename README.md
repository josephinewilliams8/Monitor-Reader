# LCD-OCR

# Web Camera [Arduino]
The folder _camera_server_ contains the files needed to run a web camera through an Arduino IDE. The board used in this repo is the **ESP32-WROOM-32E**, which came as part of a SunFounder ESP32 Camera Pro Kit. 

**SOME NOTES IN THE FILES:**

- **port** should be the port that where the board's USB connects to the laptop.
- **board** should be the _ESP32 Dev Module_. 
- In lines 35&36, replace **<ssid>** and **<password>** with the relevant information from the WiFi Router. Make sure that you do not remove the quotation marks.
- The **baud** that is in camera_server.ino should be 115200. This is the same baud that should be put into the serial monitor to get the correct IP address to put into a fresh tab and see the live stream.

# Connect to Git Repo in VSCode
In order to clone this Git Repo on Windows, click the green <>Code button, and coppy the HTTPS address. Change to the working directory where you would like to clone the directory. Then type:

	git clone <HTTPS ADDRESS>

Then, press Enter to create a local clone on your device. 
