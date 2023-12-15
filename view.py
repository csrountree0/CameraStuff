import tkinter as tk

from controller import Controller


# contains gui elements
class View:
    def __init__(self):
        # make a controller object
        self.controller = Controller(self)

        # get a window
        # make background darkmode
        self.root = tk.Tk()
        self.root.geometry("400x250")
        self.root.configure(bg="#3B3B3B")
        self.root.resizable(False, False)
        self.root.after(1, self.showImg)

        # canvas to hold preview of cam
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.config(width=250)
        self.canvas.pack(padx=10, pady=10, side=tk.RIGHT, fill=tk.Y)

        # frame for buttons on right side of screen
        self.btnFrame = tk.Frame(self.root, width=200, height=300, bg="#3B3B3B")
        self.btnFrame.pack(side=tk.LEFT)
        self.btnFrame.pack_propagate(False)

        # button to select pixelated
        self.pxlBtn = tk.Button(self.root, text="Pixelated", command=self.controller.pxlBtnPress)
        self.pxlBtn.pack(side=tk.TOP, pady=(70, 0), in_=self.btnFrame)

        # button for ascii
        self.ascBtn = tk.Button(self.root, text="Ascii", command=self.controller.ascBtnPress, width=7)
        self.ascBtn.pack(pady=(10, 0), side=tk.TOP, in_=self.btnFrame)

        # slider for pixelation
        self.scale = tk.Scale(self.root, from_=1, to=100, orient=tk.HORIZONTAL)
        self.scale.pack(pady=10, side=tk.TOP, in_=self.btnFrame)

    def showImg(self):
        mdl = self.controller.model
        mdl.updateStep(self)
        mdl.readCam()
        #mdl.sendtoVcam()
        if mdl.ret:
            if self.controller.choice == 1:
                mdl.mPixel(mdl.step)
            else:
                mdl.pixtoasc(mdl.step)
            mdl.sendtoVcam()
            mdl.gPhoto(self)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=mdl.cImg)
            # Keep a reference to the PhotoImage object to prevent it from being garbage-collected
            self.canvas.photo = mdl.cImg
        else:
            pass
        self.root.after(1, self.showImg)

    # start the gui
    def start(self):
        self.root.mainloop()
