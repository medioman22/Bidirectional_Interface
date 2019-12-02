# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 10:29:38 2019

@author: hkohli
"""

import threading
import tkinter as tk
from tkinter import ttk

from PIL import ImageTk, Image

win = tk.Tk()
win.geometry('1000x1000')  # set window size
win.resizable(0, 0)  # fix window

panel = tk.Label(win)
panel.pack()
folder = "experiment_pictures/"
images = ['up', 'down', 'left', 'right', 'front' , 'back', 'extend', 'contract']
extension = '.png'
images = iter(images)  # make an iterator

test = "Bite"

comboDevice = ttk.Combobox(win, 
                            values=[
                                    "Glove", 
                                    "Bracelets"])

def comboCallback(event):
    print("Device chosen")
    next_img()
    comboDevice.destroy()
    btn.pack()
    
def test_fct():
    global test
    print(test)
    test = "Belle bite"

comboDevice.current()
comboDevice.pack()
comboDevice.bind("<<ComboboxSelected>>",comboCallback )


def next_img():
       
    try:
        img = next(images)  # get the next image from the iterator
    except StopIteration:
        btn.destroy()
        return  # if there are no more images, do nothing

    # load the image and display it
    img = Image.open(folder + img+extension)
    img = ImageTk.PhotoImage(img)
    panel.img = img  # keep a reference so it's not garbage collected
    panel['image'] = img
    
    

#print(comboDevice.current(), comboDevice.get())    

btn = tk.Button(text='Next image', command=next_img)


# show the first image
#next_img().


win.mainloop()