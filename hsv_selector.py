import cv2
import numpy as np

def nothing(x):
    pass

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

# Insert file path to the image here:
try:
    img = cv2.imread('Calibration Images/img5.png')
    img = resize_to_width(img, 600)

    # Uncomment line below if the image needs to be rotated
    # img = imutils.rotate(img, angle=10)

    # Create a window
    cv2.namedWindow('image')

    # create trackbars for color change
    cv2.createTrackbar('HMin','image',0,179,nothing) # Hue is from 0-179 for Opencv
    cv2.createTrackbar('SMin','image',0,255,nothing)
    cv2.createTrackbar('VMin','image',0,255,nothing)
    cv2.createTrackbar('HMax','image',0,179,nothing)
    cv2.createTrackbar('SMax','image',0,255,nothing)
    cv2.createTrackbar('VMax','image',0,255,nothing)

    # Set default value for MAX HSV trackbars.
    cv2.setTrackbarPos('HMax', 'image', 179)
    cv2.setTrackbarPos('SMax', 'image', 255)
    cv2.setTrackbarPos('VMax', 'image', 255)

    # Initialize to check if HSV min/max value changes
    hMin = sMin = vMin = hMax = sMax = vMax = 0
    # phMin = psMin = pvMin = phMax = psMax = pvMax = 0

    output = img
    waitTime = 33

    while(1):

        # get current positions of all trackbars
        hMin = cv2.getTrackbarPos('HMin','image')
        sMin = cv2.getTrackbarPos('SMin','image')
        vMin = cv2.getTrackbarPos('VMin','image')

        hMax = cv2.getTrackbarPos('HMax','image')
        sMax = cv2.getTrackbarPos('SMax','image')
        vMax = cv2.getTrackbarPos('VMax','image')

        # Set minimum and max HSV values to display
        lower = np.array([hMin, sMin, vMin])
        upper = np.array([hMax, sMax, vMax])

        # Create HSV Image and threshold into a range.
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        output = cv2.bitwise_and(img,img, mask= mask)
        
        # Display output image
        cv2.imshow('image',output)

        # Wait longer to prevent freeze for videos.
        if cv2.waitKey(waitTime) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
except:
    print('Image did not load.')
    print('Make sure you have written the correct path in line 23.')
    print('If errors persist, rerun livestream.py to add images to "Calibration Images."')
    print('Else, check for errors in livestream.py code.')