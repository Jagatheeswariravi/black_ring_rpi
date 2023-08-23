import cv2

# Global variables
refPt = []
cropping = False

def draw_box(event, x, y, flags, param):
    global refPt, cropping

    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True
    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        cropping = False

        # Draw a rectangle around the selected region
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("Image", image)

def get_roi(image_path):
    global image, refPt

    # Load the image
    image = cv2.imread(image_path)
    clone = image.copy()

    # Create a window and set the mouse callback function
    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", draw_box)

    # Keep looping until the 'Esc' key is pressed
    while True:
        cv2.imshow("Image", image)
        key = cv2.waitKey(1) & 0xFF

        # Press 'r' to reset the selection
        if key == ord("r"):
            image = clone.copy()
            refPt = []

        # Press 'c' to confirm the selection and get the ROI
        elif key == ord("c"):
            if len(refPt) == 2:
                x, y = refPt[0]
                width = refPt[1][0] - refPt[0][0]
                height = refPt[1][1] - refPt[0][1]
                print(refPt)
                #print(f"(x, y) = ({x}, {y}), Width = {width}, Height = {height}")
                break

        # Press 'Esc' to exit without selecting ROI
        elif key == 27:
            break

    # Close all open windows
    cv2.destroyAllWindows()
    

# Example usage
image_path = "C:\\Users\\PMTC-ELE\\Documents\\black_ring\\ok\\frame_0060.jpg"
get_roi(image_path)
