#!/usr/bin/env python
import PySimpleGUI as sg
import cv2 as cv


def main():
    # ---===--- Get the filename --- #
    filename = sg.popup_get_file('Filename to play')
    if filename is None:
        return
    vidFile = cv.VideoCapture(filename)
    # ---===--- Get some Stats --- #
    num_frames = vidFile.get(cv.CAP_PROP_FRAME_COUNT)

    sg.theme('Black')

    # ---===--- define the window layout --- #
    layout = [[sg.Text('OpenCV Demo', size=(15, 1), font='Helvetica 20')],
              [sg.Image(key='-IMAGE-')],
              [sg.Push(), sg.Button('Exit', font='Helvetica 14')]]

    # create the window and show it without the plot
    window = sg.Window('Demo Application - OpenCV Integration', layout, no_titlebar=False, location=(0, 0))

    # locate the elements we'll be updating. Does the search only 1 time
    image_elem = window['-IMAGE-']
    timeout = 0.1                 # time in ms to use for window reads
    
    # ---===--- LOOP through video file by frame --- #
    while vidFile.isOpened():
        event, values = window.read(timeout=timeout)
        if event in ('Exit', None):
            break
        ret, frame = vidFile.read()
        if not ret:  # if out of data stop looping
            break
        out = run_once(frame)

        imgbytes = cv.imencode('.ppm', out)[1].tobytes()  # can also use png.  ppm found to be more efficient
        image_elem.update(data=imgbytes)

main()