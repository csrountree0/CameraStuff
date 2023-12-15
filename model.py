import cv2
import numpy as np
import pyvirtualcam
from PIL import ImageTk, Image


# contains work done to camera
class Model:

    def __init__(self):
        # set cam to port 0, probably need to change later to prevent error
        self.cam = cv2.VideoCapture(0)
        # set list of strings we'll use
        self.lst = ".`^,:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

        # see if ret was read successfully, store frame in frame
        self.ret = None
        self.frame = None
        fmt = pyvirtualcam.PixelFormat.BGR
        self.virtual_cam = pyvirtualcam.Camera(width=640, height=480, fps=30, fmt=fmt)

        self.cImg = None

        self.step = 1

    def readCam(self):
       self.ret, self.frame = self.cam.read()

    # assuming camera is 1080p then we take 1920/step and 1080/step to get rows and columns of ascii
    def pixtoasc(self, step):
        # convert to black and white
        gf = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        # create empty frame
        ascii_frame = np.zeros_like(self.frame, dtype=np.uint8)

        rows, cols = gf.shape
        # iterate through rows in increments of step
        for i in range(0, rows, step):
            # iterate through columns in increment of step
            for j in range(0, cols, step):
                # get
                intensity = gf[i, j]
                index = int(intensity / 255 * (len(self.lst) - 1))
                cv2.putText(ascii_frame, self.lst[index], (j, i), cv2.FONT_HERSHEY_SIMPLEX, .4, (255, 255, 255), 1,cv2.LINE_AA)

        self.frame = ascii_frame

    def mPixel(self, step):
        self.frame = cv2.resize(self.frame, (640 // step, 480 // step))
        self.frame = cv2.resize(self.frame, (640, 480), interpolation=cv2.INTER_NEAREST)

    def gPhoto(self, v):
        # Convert the BGR frame to RGB
        rgb_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

        # Convert the RGB frame to a PIL Image
        pil_image = Image.fromarray(rgb_frame)

        # Resize the image to fit the canvas while preserving aspect ratio
        width, height = v.canvas.winfo_width(), v.canvas.winfo_height()
        pil_image = pil_image.resize((width, height), Image.Resampling.LANCZOS)

        # Convert the resized PIL Image to a PhotoImage
        self.cImg = ImageTk.PhotoImage(pil_image)
        #self.cImg = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)))

    def updateStep(self, v):
        self.step = v.scale.get()

    def sendtoVcam(self):
        #self.frame = cv2.cvtColor(self.frame, cv2.COLOR_GRAY2BGR)
        self.virtual_cam.send(self.frame)