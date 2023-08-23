import PySimpleGUI as sg
import cv2

def capture_frame():
    cap = cv2.VideoCapture(0)  # Change 0 to the camera index you want to use (e.g., 0 for the default camera)

    if not cap.isOpened():
        sg.popup_error('Failed to access the camera!')
        return None

    ret, frame = cap.read()
    cap.release()

    return frame



def main():
    layout = [
        [sg.Image(key='-IMAGE-'), sg.Text('', key='-RESULT-', font=('Helvetica', 20))]
    ]

    window = sg.Window('YOLO v8 Image Detection', layout, finalize=True,size=(1920,1080))
    captured_image = capture_frame()
            #processed_image, detection_result = process_image(captured_image)
    window['-IMAGE-'].update(data=captured_image)
    window['-RESULT-'].update("goom")

   
    

    

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

    window.close()  

if __name__ == '__main__':
    main()
