import cv2

def extract_frames(video_path, output_folder):
    # Open the video file
    video_capture = cv2.VideoCapture(video_path)

    # Get the frames per second (fps) and the total number of frames
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"Video FPS: {fps}")
    print(f"Total Frames: {total_frames}")

    # Counter to keep track of the frames
    frame_count = 0

    # Loop through the video and extract frames
    while True:
        # Read a frame
        ret, frame = video_capture.read()

        # Break the loop if no frames are left
        if not ret:
            break

        # Save the frame to the output folder
        output_path = f"{output_folder}/frame_notok{frame_count:04d}.jpg"
        cv2.imwrite(output_path, frame)

        frame_count += 10

    # Release the video capture object
    video_capture.release()

    print("Frames extraction completed.")

if __name__ == "__main__":
    # Replace 'video_path' with the path to your video file
    video_path = "C:\\Users\\PMTC-ELE\\Documents\\ok .mp4"

    # Replace 'output_folder' with the folder where you want to save the frames
    output_folder = "C:\\Users\\PMTC-ELE\\Documents\\black_ring\\not_ok"

    extract_frames(video_path, output_folder)
