import cv2
import numpy as np
import pyvirtualcam

# list of chars we can use
lst = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`. "
lst = lst[::-1]


# convert pixel to ascii
def pixtoasc(frame, step):
    # convert to black and white
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # create empty frame
    ascii_frame = np.zeros_like(frame, dtype=np.uint8)

    rows, cols = gray_frame.shape
    # iterate through rows in increments of 10
    for i in range(0, rows, step):
        # iterate through columns in increment of 10
        for j in range(0, cols, step):
            # get
            intensity = gray_frame[i, j]
            index = int(intensity / 255 * (len(lst) - 1))
            cv2.putText(ascii_frame, lst[index], (j, i), cv2.FONT_HERSHEY_SIMPLEX, .4, (255, 255, 255), 1, cv2.LINE_AA)

    return ascii_frame


# OpenCV camera
cam_port = 0
cam = cv2.VideoCapture(cam_port)

# Set the window size
window_width = 640
window_height = 480

choice = int(input("(1)Ascii\n(2)Pixelated\n"))

if choice == 1:
    step = int(input("Enter step size: "))
elif choice == 2:
    pixel_size = int(input("Enter pixel size: "))
else:
    print("retard")
    exit(1)

# set up the virtual cam for use
with pyvirtualcam.Camera(width=window_width, height=window_height, fps=30) as virtual_cam:
    while True:
        # Reading the input using the camera
        ret, frame = cam.read()
        # If frame is read without any errors, show it
        if ret:
            # Send the frame to the virtual camera
            if choice == 1:
                ascii_frame = pixtoasc(frame, step)
                cv2.imshow("Ascii", ascii_frame)
                virtual_cam.send(ascii_frame)
            elif choice == 2:
                resized_frame = cv2.resize(frame, (window_width // pixel_size, window_height // pixel_size))
                pixelated_frame = cv2.resize(resized_frame, (window_width, window_height),interpolation=cv2.INTER_NEAREST)
                cv2.imshow("Pixelated", pixelated_frame)
                virtual_cam.send(pixelated_frame)
            # will wait parameter ms before updating
            cv2.waitKey(1)

        else:
            print("Error reading frame")
