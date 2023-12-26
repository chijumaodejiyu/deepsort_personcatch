#!/usr/bin/env python
import PySimpleGUI as sg
import cv2 as cv


class Gui:
    def __init__(self):
        # ---===--- define the window layout --- #
        self.layout = [[sg.Combo((0, 1), size=(10, 1), default_value=0, key='-ID-')],
                       [sg.Image(key='-FINDER-'), sg.Image(key='-TRACKER-')]]

        # create the window and show it without the plot
        self.window = sg.Window('Window', self.layout, no_titlebar=False, location=(500, 300))
        self.combo_elem = self.window['-ID-']
        self.event = None
        self.value = None

    def update(self):
        self.event, self.value = self.window.read(timeout=50)

    def update_image(self, name, image):
        image_elem = self.window[name]
        imgbytes = cv.imencode('.ppm', image)[1].tobytes()
        image_elem.update(data=imgbytes)

    def update_id(self, ids):
        last_id = self.get_id()
        if last_id in ids:
            val = last_id
        else:
            val = ids[0]
        self.combo_elem.update(value=val, values=ids)

    def get_id(self):
        return self.combo_elem.get()


if __name__ == '__main__':
    gui = Gui()
    while True:
        gui.update()
        gui.update_id([1, 2, 3, 4])
        event = gui.event
        value = gui.value
        if event in ('Exit', None):
            break
