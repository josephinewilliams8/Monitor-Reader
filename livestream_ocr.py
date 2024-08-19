from easyocr import Reader
import cv2
import numpy as np
from datetime import datetime as dt
import pandas as pd

# saving image to device from local website
import requests
import time
import shutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

print('Program started...')
url = 'http://192.168.0.133'
reader = Reader(['en'])

print('OCR Reader loaded...')

try:
    options = webdriver.EdgeOptions()
    options.add_argument('log-level=3')
    print('Loading up the driver...') 
    driver = webdriver.Edge()
    print('Edge Driver loaded...')
    driver.get(url)
    print('The title of loaded page is:', driver.title)

    button = driver.find_element(By.ID, 'toggle-stream')
    select = Select(driver.find_element(By.ID, 'framesize'))
    select.select_by_visible_text('UXGA(1600x1200)')
    print('Success!')

except:
    print('ERROR DETECTED:')
    print(f'There were some errors loading up the local address {url}.')
    print(f'Check that your url is the correct IP Address.')
    print(f'Check that connection is secure, and Arduino code is running with the correct SSID/Password.')
    print(f'Confirm that the camera is turned on, and that the resolution is selected properly.')
    
def main():
    # WRITE 'calibrate = True' IN ORDER TO DO INITIAL CALIBRATION
    calibrate = False
    
    # Initialize the folder CSV file and Pandas dataframe
    csv = 'Monitor Readings.csv'
    df = pd.read_csv(csv)
    
    i=0
    while True:
        if calibrate is True:
            break
        try:
            button.click()
            milli = int(round(time.time()*1000))

            # Save frame from livestream
            r = requests.get(f'{url}/capture?_cb={milli}', stream=True)

            img_path = f'screens/img{i}.png'
            
            with open(img_path, 'wb') as out_file:
                shutil.copyfileobj(r.raw, out_file)
            
            # Process image and save data to CSV file
            frame = cv2.imread(img_path)
            processed_frame = process_image(frame)
            if processed_frame is not None:
                ocr_result = reader.readtext(processed_frame)
                send_results(ocr_result, df, csv)
                
            button.click()
            
            # Time asleep between each frame capture (in seconds):
            time.sleep(3)
            
            i += 1
        except:
            print('there were some problems with the stream, try again.')
            break

    if calibrate is True:
        for i in range(1,11):
            try:
                button.click()
                milli = int(round(time.time()*1000))

                r = requests.get(f'{url}/capture?_cb={milli}', stream=True)

                img_path = f'calibration/img{i}.png'
                
                with open(img_path, 'wb') as out_file:
                    shutil.copyfileobj(r.raw, out_file)
                    
                button.click()
                time.sleep(3)
            except:
                print('there were some problems with the stream, try again.')
                break

def process_image(image):
    """
    Process the image to extract readable text from a digital screen.
    
    Args:
        image (np.ndarray): Array from the input image.
    
    Returns:
        np.ndarray: Processed image ready for OCR.
    """
    # Uncomment line below if the image needs to be rotated by 'angle' degrees. 
    # image = imutils.rotate(image, angle=10)

    # Resize the image and convert to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Insert HSV min/max values, calibrated from hsv_selector.py
    hmin, smin, vmin = 35, 200, 30
    hmax, smax, vmax = 90, 255, 255
    
    # Find high/low values for HSV masking
    lower = np.array([hmin, smin, vmin], np.uint8)
    upper = np.array([hmax, smax, vmax], np.uint8)
    
    # Apply thresholding
    thresh = cv2.inRange(hsv, lower, upper)

    # Change brightness/contrast values here:
    brightness = 255
    contrast = 127

    # Find contours and extract the largest contour (which is our display monitor)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        cropped = image[y:y+h, x:x+w]
        
        filtered = cv2.addWeighted(cropped, 1 + contrast / 127.0, cropped, 0, brightness - 255)
        filtered = resize_to_width(filtered, 200)
        
        return filtered
    return None

def take_numbers(text):
    """
    Extracts the number from the text generated by EasyOCR, excluding units (SM3 or SM3/H).
    
    Args:
        text (str): Text generated by EasyOCR's reading.
    
    Returns:
        str: Extracted number from the text.
    """
    pos = -1
    for i, char in enumerate(text):
        if char in [' ', 'S', 'M', 'H']:
            pos = i
            break
    return text[:pos] if pos != -1 else text

def send_results(easy_ocr_result, df, csv):
    """
    Sends the results of the monitor reading to a CSV file.
    
    Args:
        easy_ocr_result (list): OCR result from EasyOCR.
        df (pd.DataFrame): DataFrame to append the new readings.
        csv (str): Path to the CSV file which stores OCR results from the DataFrame.
    """
    nums = [0, 0]
    index = 0
    for _, text, _ in easy_ocr_result:
        temp = take_numbers(text)
        if temp:
            nums[index] = temp
            index += 1
            if index >= 2:
                break
    
    try:
        sm3h, sm3 = float(nums[0]), int(nums[1])
    except ValueError:
        return
    
    # Record the date/time that the display monitor was read
    current = dt.now()
    date = current.strftime("%Y-%m-%d")
    time = current.strftime("%H:%M:%S")
    
    # Format data to be put into the CSV file
    new_data = [date, time, sm3h, sm3]
    df.loc[len(df)] = new_data
    
    # Send data to the CSV file
    df.to_csv(csv, mode='w', header=True, index=False)


# ---- OLD CODE ----
def resize_to_width(img, width):
    """
    Resizes the input image to the specified width while maintaining the aspect ratio.
    
    Args:
        img (np.ndarray): Input image.
        width (int): Desired width of the resized image.
    
    Returns:
        np.ndarray: Resized image with the specified width.
    """
    height = int(img.shape[0] * width / img.shape[1])
    return cv2.resize(img, (width, height))

# def resize_to_scale(img, scale):
#     """
#     Resizes the input image by a specified scale percentage.
    
#     Args:
#         img (np.ndarray): Input image.
#         scale (float): Scale percentage to resize the image.
    
#     Returns:
#         np.ndarray: Resized image scaled by the specified percentage.
#     """
#     width = int(img.shape[1] * scale / 100)
#     height = int(img.shape[0] * scale / 100)
#     return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

# def process_image(image, calibrate):
#     """
#     Process the image to extract readable text from a digital screen.
    
#     Args:
#         image (np.ndarray): Array from the input image. If the image path is a string, use cv2.imread to turn it into an np.ndarray. 
#         calibrate (bool): If true, will display images to help calibrate the system to perform OCR on inputs. If false, will continue with program as usual. 
#     Returns:
#         str: Extracted text from the image.
#     """
#     # Resize the image and convert to grayscale
#     image = resize_to_scale(image, 55)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     # Apply thresholding
#     _, thresh = cv2.threshold(gray, 75, 150, 0) 
#     kernel = np.ones((5, 5), np.uint8)
#     thresh = cv2.morphologyEx(thresh, cv2.MORPH_GRADIENT, kernel)
    
#     # Find contours and extract the largest contour
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#     if contours:
#         largest_contour = max(contours, key=cv2.contourArea)
#         x, y, w, h = cv2.boundingRect(largest_contour)
#         cropped = image[y:y+h, x:x+w]
        
#         # Resize and enhance the image
#         cropped = resize_to_width(cropped, 600)
#         edges = cv2.Canny(cropped, 75, 160) # CALIBRATE THRESHOLD1 AND THRESHOLD2
#         blurred_edges = cv2.GaussianBlur(edges, (27, 27), cv2.BORDER_REPLICATE) # CALIBRATE MIDDLE VALUE OF ARRAY
#         sharpening_kernel = np.array([[-1, -1, -1],
#                                       [-1, 40, -1], # CALIBRATE MIDDLE VALUE OF ARRAY
#                                       [-1, -1, -1]])
        
#         sharpened_image = cv2.filter2D(blurred_edges, -1, sharpening_kernel)
#         blurred_edges = cv2.medianBlur(sharpened_image, 3, cv2.BORDER_REPLICATE)
        
#         # Invert and resize the image for OCR
#         inverted_image = cv2.bitwise_not(blurred_edges) 
#         before = cv2.dilate(inverted_image,kernel)
#         resized_for_ocr = resize_to_width(before, 500)
        
#         # Judge images to help calibrate system
#         if calibrate:
#             cv2.imshow('Unprocessed Image', image)
#             cv2.imshow('Highlighted Edges', edges)
#             cv2.imshow('Processed Image', resized_for_ocr)
#             cv2.waitKey(0)
            
#         return resized_for_ocr
#     else:
#         return None

# def take_numbers(text):
#     """
#     Extracts the number from the text generated by EasyOCR, excluding units (SM3 or SM3/H).
    
#     Args:
#         text (str): Text generated by EasyOCR's reading.
    
#     Returns:
#         str: Extracted number from the text.
#     """
#     pos = -1
#     for i, char in enumerate(text):
#         if char in [' ', 'S', 'M', 'H']:
#             pos = i
#             break
#     return text[:pos] if pos != -1 else text

# def send_results(easy_ocr_result, df, csv):
#     """Sends the results of our monitor reading to {database or csv or spreadsheet, tbd}. In the list that is returned, the first item is the SM3 reading, and the second item is the SM3/H reading. 

#     Args:
#         easy_ocr_result (list): OCR result from EasyOCR.
#         df (pd.DataFrame): DataFrame to append the new readings.
#         csv (str): Path to the CSV file which stores OCR results from the DataFrame.
#     """
#     nums = [0,0]
#     index = 0
#     for _, text, _ in easy_ocr_result:
#         temp = take_numbers(text)
#         if temp:
#             nums[index] = temp
#             index += 1
#             if index >= 2:
#                 break
    
#     current = dt.now()
#     sm3h, sm3 = nums
#     date = current.strftime("%Y-%m-%d")
#     time = current.strftime("%H:%M:%S")
    
#     new_data = [date, time, sm3h, sm3]
#     df.loc[len(df)] = new_data
    
#     df.to_csv(csv, mode='w', header=True, index=False)
#     print(new_data)

# def capture_frame_every_length(video_url, length, df, csv, calibrate):
#     """
#     Will send to a sheet the SM3 and SM3/H readings from a recording of a monitor every length of time that is passed in (in seconds). Note that one hour is 3600 seconds. Will also consider the FPS of a video, that it will be more accurate with the timing.  
    
#     Args:
#         video_url (str): location of Video Stream, whether it be pre-recorded as an MP4, or if it is a link [or other form that cv2 can parse]
#         length (int): the number of seconds with which we would like to take the data from our video stream.
#         df (pd.DataFrame): DataFrame to append the new readings.
#         calibrate (bool): If true, helps calibrate the system for OCR on inputs.
#         csv (str): Path to the CSV file which stores OCR results from the DataFrame.
#     """
#     if calibrate:
#         return
#     # initialize video capture
#     cap = cv2.VideoCapture(video_url)
#     fps = int(cap.get(cv2.CAP_PROP_FPS))
#     print(fps)
    
#     # confirm the video capture is initialized
#     if not cap.isOpened():
#         print("Error: Unable to open video stream")
#         return

#     # initialize EasyOCR reader
#     reader = Reader(['en'])  # add other languages if needed

#     frame = 0 
#     while True:
#         # read each frame of our video
#         ret, img = cap.read()
        
#         if not ret:
#             print("Error: Unable to read frame from video stream")
#             break
        
#         # check to see if it is time to record the monitor's reading. then, process image, apply EasyOCR, process results
#         if frame==length*fps:
#             processed_img = process_image(img, calibrate)
#             if processed_img is not None:
#                 ocr_result = reader.readtext(processed_img)
#                 send_results(ocr_result, df, csv)
            
#             # reset frame count
#             frame = 0 

#         frame +=1

#     # release the video capture
#     cap.release()
    
# def calibrate_system(img, df, csv):
#     """
#     Calibrates the system by processing a single image and sending OCR results to a CSV file.
    
#     Args:
#         img (str): Path to the image for calibration.
#         df (pd.DataFrame): DataFrame to append the new readings.
#         csv (str): Path to the CSV file which stores OCR results from the DataFrame.
#     """
#     if img is None:
#         return
    
#     image = cv2.imread(img)
#     processed_image = process_image(image, calibrate=True)
#     

# def main():
#     calibrate = False
#     img_path = None
    
#     video_path = r'C:\Users\josephine.williams\python_env\lcd_ocr\monitor_one.mp4'
#     csv = 'Monitor Readings.csv'
    
#     # # UNCOMMENT THE NEXT THREE LINES TO CALIBRATE THE SYSTEM
#     # calibrate = True
#     # img_path = r'C:\Users\josephine.williams\python_env\lcd_ocr\images\test_four.jpg'
#     # csv = 'Tester.csv'
    
#     dataframe = pd.read_csv(csv)
#     capture_frame_every_length(video_path, 12, dataframe, csv, calibrate)
    
#     if calibrate:
#         calibrate_system(img_path, dataframe, csv)
    
# if __name__ == "__main__":
#     main()

if __name__ == "__main__":
    main()