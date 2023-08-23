import cv2



video_path_out = '{}_out.mp4'.format("rpi")

# Create a VideoCapture object to open the webcam
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
H, W, _ = frame.shape
out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))
 # 0 represents the default camera

# Check if the webcam was successfully opened
if not cap.isOpened():
    print("Failed to open the webcam")
    exit()

# Read and display frames from the webcam until 'q' is pressed
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Check if the frame was successfully read
    if not ret:
        print("Failed to read the frame from the webcam")
        break

    # Display the frame in a window
    out.write(frame)
    cv2.imshow("frame",frame)

    # Check if 'q' key is pressed to exit
    if cv2.waitKey(1) == ord('q'):
        break

# Release the VideoCapture object and close the window
cap.release()
cv2.destroyAllWindows()
