<img width="707" alt="image" src="https://github.com/user-attachments/assets/5db5d836-adc9-4314-8b5f-a7e40e764ca2"># Monitor Reader
In order to read the values on a BMS Monitor, we will be using an ESP32 Camera Pro Kit. In this kit, we will be able to observe a livestream of the monitor through a local web adress. In addition, we will save images of the monitor and perform Optical Character Recognition, a computer vision task which extracts text from images which can then be further processed. In this program, the extracted data will be inserted into a CSV file. 

# Web Camera [Arduino]
The folder _camera_server_ contains the files needed to run a web camera through an Arduino IDE. The board used in this repo is the **ESP32-WROOM-32E**, which came as part of a SunFounder ESP32 Camera Pro Kit. 

**SOME NOTES IN THE FILES:**
- **port** should be the port that where the board's USB connects to the laptop.
- **board** should be the _ESP32 Dev Module_. 
- In lines 35&36, replace **ssid** and **password** with the relevant information from the WiFi Router. Make sure that you do not remove the quotation marks.
- The **baud rate** that is in camera_server.ino should be 115200. This is the same baud that should be put into the serial monitor to get the correct IP address to put into a fresh tab and see the live stream.

**CONNECTING TO LOCAL ADDRESS WITH LIVESTREAM:**

After the arduino is flashed with code, open the Serial Monitor. In the Serial Monitor, there should be information similar to the following printed out:

 	. . . . . . 
	WiFi connected
	Starting web server on port: '--'
	Starting stream server on port: '--'
	Camera Ready! Use 'http://192.168.0.133/' to connect

If you do not see this information, check that Wi-Fi connection is sufficient. If it is, try clicking the left button on the camera's board to try and reset the system.

Record and/or copy the local address that the Serial Monitor prints out. If you open this link in your web browser with a device connected to the same Wi-Fi as the camera, you should see an interface that looks like the following:

If all of this works properly, insert the same address into line 18 of livestream.py (replacing any address that might already be in place). 

# System Calibration
To ensure that the frames captured from the livestream video of our monitor can be read properly, we can perform some initial calibration to set up our system properly. 

To begin, we will save 10 images to the folder '_Calibration Images_.' In order to save the 10 images, open the file '_livestrem_ocr.py_' and in **line 46**, change the statement such that it says 'calibrate = True'. Now, after running the file, we will have a small set of images that we can work with.

**HSV MASKING**

Once we've saved our 10 images, the next step is to perform HSV masking so that we are able to properly crop our frame to the desired display monitor. Open up the file '_hsv_selector.py_' -- in **line 23**, insert the path to the image which you would like to work with (the default is the fifth image in our calibration image set). Then, run the file. There should be a new window that pops up, with six trackbars for the minimum/maximum hue, saturation, and value numbers. 

Move the trackbar until most of the background is removed from the frame (i.e. black), without removing any of the display monitor itself. If any of the display monitor is removed at this stage, it will reduce the efficacy of the program's ability to crop to the monitor. An example of a well-masked image is shown below for reference:

INSERT IMAGES HERE

Make note of the **HMin, SMin, VMin, HMax, SMax, VMax** values, as these will be used in the next steps!

**OCR TESTING**

Once we have our min/max values saved, we can test out our OCR program on our test folder. Open up the file '_calibration_ocr.py_' and in **lines 52-53** input the values for HSV min/max noted earlier. Run the file. 

The print statements that show up should express the time, date, SM3/H and SM3 readings of each image, as well as the image that the reading connects to. The data should automatically be sent to the '_Tester.csv_' file. 

**If all of the readings are correct:** Woohoo! Go into '_livestream_ocr.py_' and insert HSV values into **lines 139-140**, then run the file. The system should be up and running properly. 

**If some of the readings are incorrect:** More set-up may be required. This can relate to the brightness, contrast, and/or resolution of the image. 

**BRIGHTNESS/CONTRAST** 

To test the brightness/contrast of our video frames, open up the file '_contrast.py_,' where we will again perform testing on one of the images from our calibration folder. Similar to the HSV Masking, the default is the fifth image in the folder (but the path to any image can be inserted in **line 29**). Run the file, and use the trackbars to manipulate the brightness/contrast (making note of the respective values). An example is shown below:

INSERT IMAGE HERE

Once they have been recorded, insert the values into **lines 63-64** of '_calibration_ocr.py_.' Run '_calibration_ocr.py_' to check the accuracy of the program. 

**If all of the readings are correct:** Woohoo! Go into 'livestream_ocr.py' and insert brightness/contrast values into **lines 150-151** and then run the file; the system should be up and running properly. 

**If some of the readings are still incorrect:** The camera hardware may need to be moved in order to get a more clear picture of the display, as the resolution of the display is too small to get an accurate reading. Fix the camera's location, and perform calibration tests again. 

# Why HSV Masking? 
Insert info here about why we do HSV masking instead of something like B/W or RGB. 

# What is Optical Character Recognition?
Insert info here about what OCR is/what it does. 

# Connect to Git Repo in VSCode
In order to clone this Git Repo on Windows, click the green <>Code button, and coppy the HTTPS address. Change to the working directory where you would like to clone the directory. Then type:

	git clone <HTTPS ADDRESS>

Then, press Enter to create a local clone on your device. 

# Important Libraries
**OpenCV:** Open-source computer vision library used for machine learning and image processing. Performs operations including (but not limited to) cropping, resizing, color transformations, adding shapes, loading and saving images, thresholding, and sharpening. 

**EasyOCR:** Optical character recognition library, a user-friendly way to extract text from images. Handles 80+ languages and writing scripts. Implemented using the PyTorch library. 

**NumPy:** Provides a multidimensional array object for efficient operations. Foundation for other data science packages to be built (is used by libraries such as EasyOCR). 

**Pandas:** Library for data manipulation and analysis. This includes extracting, cleaning, and visualizing data. Built on top of NumPy, with its contained data often passed through machine learning algorithms. 
