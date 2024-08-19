import cv2

def BrightnessContrast(brightness=0):
    brightness = cv2.getTrackbarPos('Brightness', 'GEEK')
    contrast = cv2.getTrackbarPos('Contrast', 'GEEK')
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
    original = cv2.imread(r'contraster.jpg')
    original = resize_to_width(original, 600)
    img = original.copy()
    cv2.namedWindow('GEEK')
    cv2.imshow('GEEK', original)
    cv2.createTrackbar('Brightness', 'GEEK', 255, 2 * 255, BrightnessContrast)
    cv2.createTrackbar('Contrast', 'GEEK', 127, 2 * 127, BrightnessContrast)
    BrightnessContrast(0)
    cv2.waitKey(0)

# import cv2
# import imutils

# # Read the image
# image = cv2.imread("cropped.jpg")

# # Rotate by 45 degrees
# rotated_image = imutils.rotate(image, angle=10)

# # Display the rotated image
# cv2.imshow("Rotated", rotated_image)
# cv2.waitKey(0)