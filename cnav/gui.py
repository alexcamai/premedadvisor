"""
Author: Alex Camai
v1.0.0
gui.py

GUI for the CNav Application.

Contains:
    TODO

"""

from tkinter import Tk, Label, Button, Toplevel, Frame, Entry, Scale, Radiobutton, Scrollbar
from tkinter import N, E, S, W, LEFT, HORIZONTAL, VERTICAL
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
                    "Made with tkinter"
                    ]

    def __init__(self, master):
        Frame.__init__(self)
        self.master = master
        master.title("Course Navigator")

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
        wiz_main = Toplevel(self)
        wiz_main.wm_title("Basic Information")
        wiz_main.geometry('%dx%d' % (500, 200))

        instructions = Label(wiz_main, text="Please fill out the following so I can learn more about your situation.",
                             font=("Courier", 12, "bold italic"), wraplength=400, justify=LEFT)
        instructions.grid(row=1, column=1, ipadx=5, ipady=10, sticky=W)

        semesters = Label(wiz_main, text="How many semesters do you want to plan?", font=("Courier", 12))
        semesters.grid(row=2, column=1, ipadx=5, ipady=10, sticky=W)
        semester_input = Entry(wiz_main, font=("Courier", 12), width=2)
        semester_input.grid(row=2, column=2, ipadx=5)

        credit_load = Label(wiz_main, text="How many credits would you like to take per semester?",
                            font=("Courier", 12))
        credit_load.grid(row=3, column=1, ipadx=5, ipady=10, sticky=W)
        credit_input = Entry(wiz_main, font=("Courier", 12), width=2)
        credit_input.grid(row=3, column=2, ipadx=5)

        # TODO error message. Appears using .grid() / .grid_remove()

        entry_button = Button(wiz_main, text="Submit", font=("Courier", 12))
        # TODO
        entry_button.bind("<Button-1>", self.open_course_input)
        entry_button.grid(row=4, column=2, ipadx=5)

    # FIXME is event needed? (After fix)
    def open_course_input(self, event):
        course_input = Toplevel(self)
        course_input.wm_title("Enter Courses")
        course_input.geometry('%dx%d' % (920, 200))

        instructions = Label(course_input, text="Enter your course details, or use an Excel spreadsheet. "
                                                "For prerequisites, use the format SUBJ [COURSE NUMBER] separated by "
                                                "commas. For example, CHEM 1601, ENGL 2200. 'MULTI' means the course "
                                                "can be taken multiple times for credit.",
                             font=("Courier", 12, "bold italic"), wraplength=700, justify=LEFT)
        instructions.grid(row=1, column=1, columnspan=8, ipadx=5, ipady=10, sticky=W)

        subj = Label(course_input, text="SUBJECT", font=("Courier", 12, "bold"))
        subj.grid(row=2, column=1, ipadx=10)

        course_no = Label(course_input, text="ID #", font=("Courier", 12, "bold"))
        course_no.grid(row=2, column=2, ipadx=10)

        cred = Label(course_input, text="CREDITS", font=("Courier", 12, "bold"))
        cred.grid(row=2, column=3, ipadx=10)

        diff = Label(course_input, text="DIFFICULTY", font=("Courier", 12, "bold"))
        diff.grid(row=2, column=4, ipadx=10)

        pre = Label(course_input, text="PREREQUISITES", font=("Courier", 12, "bold"))
        pre.grid(row=2, column=5, ipadx=10)

        multi = Label(course_input, text="MULTI?", font=("Courier", 12, "bold"))
        multi.grid(row=2, column=6, ipadx=10)

        dl = Label(course_input, text="DEADLINE", font=("Courier", 12, "bold"))
        dl.grid(row=2, column=7, ipadx=10)

        taken = Label(course_input, text="COMPLETED?", font=("Courier", 12, "bold"))
        taken.grid(row=2, column=8, ipadx=10)

        subj_input = Entry(course_input, font=("Courier", 12), width=4)
        subj_input.grid(row=3, column=1, ipadx=10)

        cn_input = Entry(course_input, font=("Courier", 12), width=4)
        cn_input.grid(row=3, column=2, ipadx=10)

        cred_input = Entry(course_input, font=("Courier", 12))
        cred_input.grid(row=3, column=3, ipadx=10)

        diff_input = Scale(course_input, from_=0.0, to=100.0, tickinterval=25, font=("Courier", 12), orient=HORIZONTAL)
        diff_input.grid(row=3, column=4)

        pre_input = Entry(course_input, font=("Courier", 12))
        pre_input.grid(row=3, column=5, ipadx=10)

        multi_input = Radiobutton(course_input)
        # FIXME multi_input.bind()
        multi_input.grid(row=3, column=6, ipadx=10)

        dl_input = Entry(course_input, font=("Courier", 12), width=2)
        dl_input.grid(row=3, column=7, ipadx=10)

        taken_input = Radiobutton(course_input)
        # FIXME taken_input.bind("<Button-1", taken_input.deselect())
        taken_input.grid(row=3, column=8, ipadx=10)

        help_button = Button(course_input, text="Need Help?", font=("Courier", 12))
        help_button.bind("<Button-1>", self.display_help)
        help_button.grid(row=4, column=6, ipadx=10)

        file = Button(course_input, text="Select File", font=("Courier", 12), command=self.get_file)
        file.grid(row=4, column=7, ipady=10)

        submit = Button(course_input, text="Add Course", font=("Courier", 12))
        submit.grid(row=4, column=8, ipadx=10)

    def display_help(self, event):
        help_window = Toplevel(self)
        help_window.wm_title("Enter Courses")
        help_window.geometry('%dx%d' % (275, 500))

        info = Label(help_window, text="SUBJECT: Enter a short code corresponding to the course's subject.\n\n"
                                       "ID #: Enter a number corresponding to the course's number.\n\n"
                                       "CREDITS: Enter the number of credit hours the course is worth.\n\n"
                                       "DIFFICULTY: Set the slider to the approximate subjective difficulty (with 0 "
                                       "being easy, 100 being difficult.\n\n"
                                       "PREREQUISITES: Enter the course codes of all prerequisite courses. Follow the "
                                       "format SUBJECT ID#. For example, CHEM 1601.\n\n"
                                       "MULTI: Can the course be taken multiple times for credit?\n\n"
                                       "DEADLINE: With 1 being semester 1 and n being semester n, when should the "
                                       "course be taken, at the latest?\n\n"
                                       "COMPLETED: Has the course been taken for credit already? Do not mark for "
                                       "courses that can be taken more than once.",
                     font=("Courier", 12, "italic"), wraplength=230, justify=LEFT)
        info.grid(row=1, column=1, columnspan=8, ipadx=5, ipady=10, sticky=W)

        scroller = Scrollbar(help_window, orient=VERTICAL)
        scroller.grid()


if __name__ == "__main__":
    root = Tk()

    # Set root geometry
    w = 400
    h = 150

    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    main_window = GUI(root)
    root.mainloop()
