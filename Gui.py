#!/usr/bin/env python
import PySimpleGUI as sg
import cv2 as cv


class Gui:
    def __init__(self):
        # ---===--- define the window layout --- #
        self.layout = [[sg.Combo([], size=(10, 1), default_value=None, key='-ID-')],
                       [sg.Image(key='-FINDER-'), sg.Image(key='-TRACKER-')],
                       [sg.Text('nothing', background_color='white', text_color='black', key='-OUTPUT-')]]

        # create the window and show it without the plot
        self.window = sg.Window('Window', self.layout, no_titlebar=False, location=(500, 300))
        self.combo_elem = self.window['-ID-']
        self.text_elem = self.window['-OUTPUT-']
        self.list_ids = []
        self.event = None
        self.value = None

    def update(self):
        self.event, self.value = self.window.read(timeout=50)

    def update_image(self, name, image):
        image_elem = self.window[name]
        imgbytes = cv.imencode('.ppm', image)[1].tobytes()
        image_elem.update(data=imgbytes)

    # def update_id(self, ids):
    #     val = self.last_id
    #     self.combo_elem.update(value=val, values=ids)

    def add_id(self, ids):
        for id_ in ids:
            if id_ not in self.list_ids:
                self.list_ids.append(id_)
        val = self.combo_elem.get()
        self.combo_elem.update(value=val, values=self.list_ids)

    def get_id(self):
        temp_id = self.combo_elem.get()
        # if temp_id not in ('', None):
        #     self.last_id = temp_id
        return temp_id

    def update_txt_output(self, issafe):
        if issafe:
            self.text_elem.update('The target' + str(self.get_id()) + 'is in a danger zone', text_color='yellow', background_color='red')
        else:
            self.text_elem.update('The target' + str(self.get_id()) + 'is in a safe zone', text_color='black', background_color='white')


if __name__ == '__main__':
    gui = Gui()
    i = 0
    while True:
        gui.update()
        gui.add_id(list(range(i//10)))
        event = gui.event
        value = gui.value
        i += 1
        if event in ('Exit', None):
            break
