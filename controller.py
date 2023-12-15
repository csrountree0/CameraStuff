from model import Model


class Controller:
    def __init__(self, view):
        self.model = Model()
        self.view = view
        self.choice = 1


    def pxlBtnPress(self):
        self.choice = 1
        self.view.scale.config(from_=1, to=100)
    def ascBtnPress(self):
        self.choice = 2
        self.view.scale.config(from_=10, to=30)
        self.model.step=10

