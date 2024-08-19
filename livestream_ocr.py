from easyocr import Reader
import cv2
import numpy as np
from datetime import datetime as dt
import pandas as pd
import imutils

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
    
    print('Program running successfully!')
    if calibrate:
        print('Calibration mode is on. Saving 10 photos to "Calibration Images" folder.')
        print('Refer to README.md for further instruction.')
        print('If you would like to run normal livestream, edit line 46 such that calibrate=False')
    else:
        print('Calibration mode is not on, running normal livestream.')
        print('To calibrate variables, stop running program and follow directions in README.md.')
    
    # Initialize the folder CSV file and Pandas dataframe
    csv = 'Monitor Readings.csv'
    df = pd.read_csv(csv)
    
    i=0
    while True:
        if calibrate is True:
            break
        try:
            sleep_sec = 3600
            # Every sleep_sec seconds, take 3 frames of the livestream to record data
            for _ in range(3):
                # Start livestream and record current time
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
                 
                # Stop livestream and increase recorded frame count by 1
                button.click()
                i += 1
            
            # Time asleep between each frame capture (in seconds):
            time.sleep(sleep_sec)
            
        except:
            print('Program ran into problem with livestream and terminated. Try running again.')
            break
    
    # Save 10 photos to the folder called 'calibration' in order to do pre-processing measurements
    if calibrate is True:
        for i in range(1,11):
            sleep_sec = 15
            try:
                # Start livestream
                button.click()
                milli = int(round(time.time()*1000))
                
                # Save image from livestream to img_path
                r = requests.get(f'{url}/capture?_cb={milli}', stream=True)
                img_path = f'Calibration Images/img{i}.png'
                
                with open(img_path, 'wb') as out_file:
                    shutil.copyfileobj(r.raw, out_file)
                
                # Stop livestream and sleep for sleep_sec
                button.click()
                time.sleep(sleep_sec)
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
    # UNCOMMENT LINE BELOW IF IMAGE NEEDS TO BE ROTATED BY 'ang' DEGREES. 
    # ang = 10
    # image = imutils.rotate(image, angle=ang)

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
    contrast = 0

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

if __name__ == "__main__":
    main()