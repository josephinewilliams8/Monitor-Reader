# Monitor Reader
In order to read the values on a BMS Monitor, we will be using an ESP32 Camera Pro Kit. In this kit, we will be able to observe a live stream of the monitor. In addition, we will save images of the monitor to a folder and perform Optical Character Recognition, a form of Machine Learning that will be able to read and record the text/numbers. 

# Web Camera [Arduino]
The folder _camera_server_ contains the files needed to run a web camera through an Arduino IDE. The board used in this repo is the **ESP32-WROOM-32E**, which came as part of a SunFounder ESP32 Camera Pro Kit. 

**SOME NOTES IN THE FILES:**
- **port** should be the port that where the board's USB connects to the laptop.
- **board** should be the _ESP32 Dev Module_. 
- In lines 35&36, replace **ssid** and **password** with the relevant information from the WiFi Router. Make sure that you do not remove the quotation marks.
- The **baud rate** that is in camera_server.ino should be 115200. This is the same baud that should be put into the serial monitor to get the correct IP address to put into a fresh tab and see the live stream.

# Pre-Processing Images
In order to crop the image to the desired screen, open the file _hsv_selector.py_. In line 28, insert the path to an image that contains the display. By moving the trackbar, make note of the H-,S-,V- Min/Max values when the display is highlighted without an extraneous features. If needed, resize the image using cv2.resize(). 

Once the appropriate Min/Max values are obtained, enter the information in lines 56-57 in the file _livestream_ocr.py_. (NOTE TO SELF -- FIX THIS)

If further processing is required, such as increasing contrast, run the file _contrast.py_ on the desired image. Once again, by moving the trackbar we can see what values to put into line 68 of the file.

# Connect to Git Repo in VSCode
In order to clone this Git Repo on Windows, click the green <>Code button, and coppy the HTTPS address. Change to the working directory where you would like to clone the directory. Then type:

	git clone <HTTPS ADDRESS>

Then, press Enter to create a local clone on your device. 

# Important Libraries
**OpenCV:** Open-source computer vision library used for machine learning and image processing. Performs operations including (but not limited to) cropping, resizing, color transformations, adding shapes, loading and saving images, thresholding, and sharpening. 

**EasyOCR:** Optical character recognition library, a user-friendly way to extract text from images. Handles 80+ languages and writing scripts. Implemented using the PyTorch library. 

**NumPy:** Provides a multidimensional array object for efficient operations. Foundation for other data science packages to be built (is used by libraries such as EasyOCR). 

**Pandas:** Library for data manipulation and analysis. This includes extracting, cleaning, and visualizing data. Built on top of NumPy, with its contained data often passed through machine learning algorithms. 
