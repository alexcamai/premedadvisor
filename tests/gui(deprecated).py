"""
Author: Alex Camai
v1.0.0
gui.py

GUI for the CNav Application.

Contains:
    TODO

"""

from tkinter import Tk, Label, Button, Toplevel, Frame, Entry, Scale, Checkbutton, Scrollbar
from tkinter import N, E, S, W, LEFT, HORIZONTAL, VERTICAL, DISABLED, NORMAL
from tkinter import filedialog
from tkinter import StringVar, IntVar

from cnav.adviser import CourseAdviser, Course


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

        # Data
        self._adviser = None
        self._semesters = 0
        self._credits = 0
        self._courses = []
        self._taken = []

        self.semesters_input = None
        self.total_credit_input = None

        self.subj_input = None
        self.cn_input = None
        self.cred_input = None
        self.diff_input = None
        self.pre_input = None
        self.is_multi = None
        self.dl_input = None
        self.is_taken = None

        # Window
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

        self.file = Button(master, text="Select File", font="Courier", command=self.get_file)
        self.file.grid(row=5, column=1, ipady=5)

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
        self.wiz_main = Toplevel(self)
        self.wiz_main.wm_title("Basic Information")
        self.wiz_main.geometry('%dx%d' % (500, 200))

        instructions = Label(self.wiz_main,
                             text="Please fill out the following so I can learn more about your situation.",
                             font=("Courier", 12, "bold italic"), wraplength=400, justify=LEFT)
        instructions.grid(row=1, column=1, ipadx=5, ipady=10, sticky=W)

        semesters = Label(self.wiz_main, text="How many semesters do you want to plan?", font=("Courier", 12))
        semesters.grid(row=2, column=1, ipadx=5, ipady=10, sticky=W)
        self.semesters_input = Entry(self.wiz_main, font=("Courier", 12), width=2)
        self.semesters_input.grid(row=2, column=2, ipadx=5)

        credit_load = Label(self.wiz_main, text="How many credits would you like to take per semester?",
                            font=("Courier", 12))
        credit_load.grid(row=3, column=1, ipadx=5, ipady=10, sticky=W)
        self.total_credit_input = Entry(self.wiz_main, font=("Courier", 12), width=2)
        self.total_credit_input.grid(row=3, column=2, ipadx=5)

        entry_button = Button(self.wiz_main, text="Submit", font=("Courier", 12))
        entry_button.bind("<Button-1>", self.basic_info_handler)
        entry_button.grid(row=5, column=2, ipadx=5)

        self.wiz_main.bind("<Return>", self.basic_info_handler)

    def basic_info_handler(self, event=None):
        if self.valid_input(self.semesters_input.get(), int) and self.valid_input(self.total_credit_input.get(), int):
            self._semesters = int(self.semesters_input.get())
            self._credits = int(self.total_credit_input.get())
            self.open_course_input()

    @staticmethod
    def valid_input(data, expected_type: type):
        if expected_type == int:
            try:
                data = int(data)
            except ValueError:
                return False
        return type(data) is expected_type

    # FIXME is event needed? (After fix)
    def open_course_input(self):
        self.wiz_main.destroy()

        # FIXME what is this self stuff
        self.course_input = Toplevel(self)
        self.course_input.wm_title("Enter Courses")
        self.course_input.geometry('%dx%d' % (850, 200))

        instructions = Label(self.course_input, text="Enter your course details, or use an Excel spreadsheet. "
                                                     "For prerequisites, use the format [SUBJ] [COURSE NUMBER] "
                                                     "separated by "
                                                     "commas. For example, CHEM 1601, ENGL 2200. 'MULTI' means the "
                                                     "course "
                                                     "can be taken multiple times for credit. Items in bold are "
                                                     "required.",
                             font=("Courier", 12, "bold italic"), wraplength=700, justify=LEFT)
        instructions.grid(row=1, column=1, columnspan=8, ipadx=5, ipady=10, sticky=W)

        subj = Label(self.course_input, text="SUBJECT", font=("Courier", 12, "bold"))
        subj.grid(row=2, column=1, ipadx=10)

        course_no = Label(self.course_input, text="ID #", font=("Courier", 12, "bold"))
        course_no.grid(row=2, column=2, ipadx=10)

        cred = Label(self.course_input, text="CREDITS", font=("Courier", 12, "bold"))
        cred.grid(row=2, column=3, ipadx=10)

        diff = Label(self.course_input, text="DIFFICULTY", font=("Courier", 12))
        diff.grid(row=2, column=4, ipadx=10)

        pre = Label(self.course_input, text="PREREQUISITES", font=("Courier", 12))
        pre.grid(row=2, column=5, ipadx=10)

        multi = Label(self.course_input, text="MULTI?", font=("Courier", 12))
        multi.grid(row=2, column=6, ipadx=10)

        dl = Label(self.course_input, text="DEADLINE", font=("Courier", 12))
        dl.grid(row=2, column=7, ipadx=10)

        taken = Label(self.course_input, text="COMPLETED?", font=("Courier", 12))
        taken.grid(row=2, column=8, ipadx=10)

        self.subj_input = Entry(self.course_input, font=("Courier", 12), width=4)
        self.subj_input.grid(row=3, column=1, ipadx=10)

        self.cn_input = Entry(self.course_input, font=("Courier", 12), width=4)
        self.cn_input.grid(row=3, column=2, ipadx=10)

        self.cred_input = Entry(self.course_input, font=("Courier", 12), width=3)
        self.cred_input.grid(row=3, column=3, ipadx=10)

        self.diff_input = Scale(self.course_input, from_=0.0, to=100.0, tickinterval=50, font=("Courier", 12),
                                orient=HORIZONTAL)
        self.diff_input.grid(row=3, column=4)

        self.pre_input = Entry(self.course_input, font=("Courier", 12))
        self.pre_input.grid(row=3, column=5, ipadx=10)

        self.is_multi = IntVar()
        self.multi_input = Checkbutton(self.course_input, variable=self.is_multi)
        self.multi_input.grid(row=3, column=6, ipadx=10)

        self.dl_input = Entry(self.course_input, font=("Courier", 12), width=2)
        self.dl_input.grid(row=3, column=7, ipadx=10)

        self.is_taken = IntVar()
        self.taken_input = Checkbutton(self.course_input, variable=self.is_taken)
        self.taken_input.grid(row=3, column=8, ipadx=10)

        help_button = Button(self.course_input, text="Need Help?", font=("Courier", 12))
        help_button.bind("<Button-1>", self.display_help)
        help_button.grid(row=4, column=5, ipadx=10)

        file = Button(self.course_input, text="Select File", font=("Courier", 12), command=self.get_file)
        file.grid(row=4, column=6, ipady=10)

        add = Button(self.course_input, text="Add Course", font=("Courier", 12), command=self.data_handler)
        add.grid(row=4, column=7, ipadx=10)

        self.course_input.bind("<Return>", self.data_handler)

        submit = Button(self.course_input, text="Next", font=("Courier", 12), command=self.finalize_data)
        submit.grid(row=4, column=8, ipadx=10)

    def data_handler(self, event=None):
        # FIXME messy af
        if self.valid_input(self.subj_input.get(), str) and self.valid_input(self.cn_input.get(), int) and \
                self.valid_input(self.cred_input.get(), int):

            dl = int(self.dl_input.get()) if self.valid_input(self.dl_input.get(), int) else None

            new_course = Course(int(self.cn_input.get()), self.subj_input.get().upper(), int(self.cred_input.get()),
                                diff=int(self.diff_input.get()) / 100, deadline=dl,
                                pre_reqs=self.pre_input.get().split(","), multi=self.is_multi.get())
            if self.is_taken.get():
                self._taken.append(new_course)
            else:
                self._courses.append(new_course)

            self.subj_input.delete(0, 'end')
            self.cn_input.delete(0, 'end')
            self.cred_input.delete(0, 'end')
            self.pre_input.delete(0, 'end')
            self.dl_input.delete(0, 'end')

            self.diff_input.set(0)

            self.multi_input.deselect()
            self.taken_input.deselect()

            self.subj_input.focus()

    def finalize_data(self, event=None):
        self.course_input.destroy()
        
        # TODO edit data inline
        self.finalize_win = Toplevel(self)
        self.finalize_win.wm_title("Review Data")
        self.finalize_win.geometry('%dx%d' % (400, 300))

        notice = Label(self.finalize_win, text="Is the following information correct?", font=("Courier", 12),
                       wraplength=350, justify=LEFT)
        notice.grid(row=1, column=1, ipadx=5, ipady=10, sticky=W)

        data = Label(self.finalize_win, text="Number of semesters:                   " + str(self._semesters) +
                                             "\n\nMaximum credit load per semester:      " + str(self._credits) +
                                             "\n\nCourses to plan:\n" +
                                             str([course.get_course_code() + " " for course in self._courses]),
                     font=("Courier", 12), wraplength=300, justify=LEFT)
        data.grid(row=2, column=1, ipadx=10)

        # no = Button(todo)

        yes = Button(self.finalize_win, text="Yes", font=("Courier", 12))
        yes.grid(row=3, column=2, ipadx=10, sticky=W)

    def display_help(self, event=None):
        help_window = Toplevel(self)
        help_window.wm_title("Enter Courses")
        help_window.geometry('%dx%d' % (275, 500))

        info = Label(help_window, text="SUBJECT: Enter a short code corresponding to the course's subject.\n\n"
                                       "ID #: Enter a number corresponding to the course's number.\n\n"
                                       "CREDITS: Enter the number of credit hours the course is worth.\n\n"
                                       "DIFFICULTY: Set the slider to the approximate subjective difficulty (with 0 "
                                       "being easy, 100 being difficult).\n\n"
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
