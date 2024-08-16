# Monitor Reader
In order to read the values on a BMS Monitor, we will be using an ESP32 Camera Pro Kit. In this kit, we will be able to observe a live stream of the monitor. In addition, we will save images of the monitor to a folder and perform Optical Character Recognition, a form of Machine Learning that will be able to read and record the text/numbers. 

# Web Camera [Arduino]
The folder _camera_server_ contains the files needed to run a web camera through an Arduino IDE. The board used in this repo is the **ESP32-WROOM-32E**, which came as part of a SunFounder ESP32 Camera Pro Kit. 

**SOME NOTES IN THE FILES:**

- **port** should be the port that where the board's USB connects to the laptop.
- **board** should be the _ESP32 Dev Module_. 
- In lines 35&36, replace **ssid** and **password** with the relevant information from the WiFi Router. Make sure that you do not remove the quotation marks.
- The **baud rate** that is in camera_server.ino should be 115200. This is the same baud that should be put into the serial monitor to get the correct IP address to put into a fresh tab and see the live stream.


# Connect to Git Repo in VSCode
In order to clone this Git Repo on Windows, click the green <>Code button, and coppy the HTTPS address. Change to the working directory where you would like to clone the directory. Then type:

	git clone <HTTPS ADDRESS>

Then, press Enter to create a local clone on your device. 

# Important Libraries
**OpenCV:** Open-source computer vision library used for machine learning and image processing. Performs operations including (but not limited to) cropping, resizing, color transformations, adding shapes, loading and saving images, thresholding, and sharpening. 

**EasyOCR:** Optical character recognition library, a user-friendly way to extract text from images. Handles 80+ languages and writing scripts. Implemented using the PyTorch library. 

**NumPy:**

**Pandas:**
