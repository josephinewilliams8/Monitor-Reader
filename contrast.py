import cv2
import imutils

def BrightnessContrast(brightness=0):
    brightness = cv2.getTrackbarPos('Brightness', cb)
    contrast = cv2.getTrackbarPos('Contrast', cb)
    effect = cv2.addWeighted(img, 1 + contrast / 127.0, img, 0, brightness - 255)
    cv2.imshow('Effect', effect)

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


if __name__ == '__main__':
    cb = 'Contrast/Brightness'

    try:
        og = cv2.imread('Calibration Images/img5.png')
        og = resize_to_width(og, 600)
        img = og.copy()
        
        # Making new window with trackbars to adjust contrast and brightness.
        cv2.namedWindow(cb)
        cv2.imshow(cb, og)
        cv2.createTrackbar('Brightness', cb, 255, 2 * 255, BrightnessContrast)
        cv2.createTrackbar('Contrast', cb, 127, 2 * 127, BrightnessContrast)
        BrightnessContrast(0)
        cv2.waitKey(0)
    except:
        print('Error loading image. Check that the image has the right path in line 29.')
