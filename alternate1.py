import cv2
import numpy as np

refPt = [(114, 450), (184, 518)]

def search_for_black_circle(image_path):
    global image, refPt

    # Load the image
    image = cv2.imread(image_path)
    clone = image.copy()
    roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    detected_circles = process_roi(roi)

    if detected_circles is not None:
        for circle in detected_circles:
            center = (circle[0] + refPt[0][0], circle[1] + refPt[0][1])
            radius = circle[2]
            cv2.circle(image, center, radius, (0, 0, 255), 2)

    # Show the whole image with detected circles (if any)
    cv2.imshow("Image with Detected Circles", image)
    cv2.waitKey(0)

def process_roi(roi):
    # Convert ROI to grayscale
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding to create a binary image
    _, binary_roi = cv2.threshold(gray_roi, 50, 255, cv2.THRESH_BINARY)

    # Use Hough Circle Transform to detect circles
    circles = cv2.HoughCircles(binary_roi, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=5, maxRadius=50)


    if circles is not None:
        circles = np.uint16(np.around(circles))
        return (circles[0,:])


    else:
        return None



# Example usage
image_path = "C:\\Users\\PMTC-ELE\\Documents\\black_ring\\not_ok\\frame_notok1450.jpg"
search_for_black_circle(image_path)
