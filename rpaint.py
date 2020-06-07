from tkinter import *
from tkinter.colorchooser import askcolor
import ctypes

#Python Paint Application created using Tkinter

class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOUR = 'red'

    def __init__(self):
        self.root = Tk()
        self.root.title("R Paint")

        #PEN Button

        self.pen_button = Button(self.root, text='Pencil', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        #Colour of the pen button

        self.colour_button = Button(self.root, text='Colour', command=self.choose_colour)
        self.colour_button.grid(row=0, column=1)

        #Eraser Button

        self.eraser_button = Button(self.root, text='Eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=2)

        #A scale out of 10 to choose the width of the pencil line

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=3)

#setting the height and the width of the canvas as the same as the monitor's resolution
        user32 = ctypes.windll.user32
        monitor_width = user32.GetSystemMetrics(0)
        monitor_height = user32.GetSystemMetrics(1)
#setting the background
        self.c = Canvas(self.root, bg='black', width=monitor_width, height=monitor_height)
        self.c.grid(row=1, columnspan=4)

        self.setup()
        #infinite loop
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.colour = self.DEFAULT_COLOUR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)#the left mouse button when clicked goes to the paint
        self.c.bind('<B3-Motion>', self.paint)#the right mouse button when clicked goes to the paint
        self.c.bind('<ButtonRelease-1>', self.reset)


    def use_pen(self):
        self.activateButton(self.pen_button)

    def choose_colour(self):
        self.eraser_on = False # cannot select the eraser button option
        self.colour = askcolor(color=self.colour)[1]

    def use_eraser(self):
        self.activateButton(self.eraser_button, eraser_mode=True)

    # On clicking the button, the button gets raised

    def activateButton(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    #creating a line and choosing the line width according to the scale

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_colour = 'black' if self.eraser_on else self.colour
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_colour,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    #Resetting the background of the paint

    def reset(self, event):
        self.old_x, self.old_y = None, None


if __name__ == '__main__':
    Paint()