"""
Author: Alex Camai
v1.0.0
gui.py

GUI for the CNav Application.

Contains:
    TODO

"""

from tkinter import Tk, Label, Button, Toplevel, Frame
from tkinter import filedialog
from tkinter import StringVar


class GUI(Frame):
    """
    TODO
    """

    DESC_OPTIONS = ["The Course Navigator!",
                    "Made for Students",
                    "Wholesome!",
                    "www.github.com/alexcamai",
                    "100% Fat Free",
                    ]

    def __init__(self, master):
        Frame.__init__(self)
        self.master = master
        master.title("Course Navigator v1.0.0")

        self.title = Label(master, text="CNavigator", font=("Courier", 20))
        self.title.grid(row=1, column=1, columnspan=1, ipadx=35)

        self.desc_index = 0
        self.desc_text = StringVar()
        self.desc_text.set(self.DESC_OPTIONS[self.desc_index])
        self.desc = Label(master, textvariable=self.desc_text, font=("Courier", 12))
        self.desc.bind("<Button-1>", self.cycle_desc_text)
        self.desc.grid(row=2, column=1, rowspan=2, columnspan=1, ipady=5)

        self.start = Button(master, text="Get Started", font="Courier", command=self.open_nav_wizard)
        self.start.grid(row=4, column=1, ipady=5)

        self.wiz = Button(master, text="Select File", font="Courier", command=self.get_file)
        self.wiz.grid(row=5, column=1, ipady=5)

    @staticmethod
    def get_file():
        filename = filedialog.askopenfilename(initialdir="/", title="Open File",
                                              filetypes=(("Excel spreadsheets", "*.xlsx"), ("all files", "*.*")))
        return filename

    def cycle_desc_text(self, event):
        self.desc_index += 1
        self.desc_index %= len(self.DESC_OPTIONS)
        self.desc_text.set(self.DESC_OPTIONS[self.desc_index])

    def open_nav_wizard(self):
        input_window = Toplevel(self)
        input_window.wm_title("Input Courses")
        input_window.geometry(get_center_coord(root, 400, 300))


def get_center_coord(app_root, width, height):

    ws = app_root.winfo_screenwidth()
    hs = app_root.winfo_screenheight()
    x = (ws / 2) - (width / 2)
    y = (hs / 2) - (height / 2)

    return '%dx%d+%d+%d' % (w, h, x, y)


if __name__ == "__main__":
    root = Tk()

    # Set root geometry
    w = 400
    h = 150
    root.geometry(get_center_coord(root, w, h))

    main_window = GUI(root)
    root.mainloop()
