"""
Author: Alex Camai
v1.0.0
gui.py

GUI for the CNav Application.

Contains:
    TODO

"""

import tkinter as tk
import tkinter.messagebox as mb
import tkinter.filedialog as file
import cnav.planner as planner
import cnav.util as util
import cnav.adviser as ca
import tempfile as temp


class CnavRoot(tk.Tk):
    def __init__(self, tasks=None):
        super().__init__()

        if not tasks:
            self.tasks = []
        else:
            self.tasks = tasks

        self.title("CourseNavigator v1")
        self.geometry("300x200")

        main_title = tk.Label(self, text="Course Navigator", font=("application", 15, "bold"), fg="#F2E7DA",
                              bg="#454DEF", pady=20)
        self.tasks.append(main_title)

        start = tk.Button(self, text="Get Started!", font=("application", 15), fg="#454DEF", bg="#F2E7DA")
        self.tasks.append(start)

        self.course_input_win = None
        start.bind("<Button-1>", self.launch_input_win)

        # Add more to-dos here

        for task in self.tasks:
            task.pack(side=tk.TOP, fill=tk.X)

    def launch_input_win(self, event=None):
        self.course_input_win = SemesterInputWindow(self)


class SemesterInputWindow(tk.Toplevel):

    def __init__(self, master):
        super().__init__(master)

        self.master = master

        self.tasks = []

        self.title("Get Started")
        self.geometry("300x200")

        sub_title = tk.Label(self, text="Let's get started!", font=("application", 14, "italic bold"))
        self.tasks.append(sub_title)

        instructions = tk.Label(self, text="Provide some basic information, and we'll get started.", wraplength=250)
        self.tasks.append(instructions)

        for task in self.tasks:
            task.grid(column=1, columnspan=2, ipadx=10)

        semesters = tk.Label(self, text="Semesters to plan: ", font=("application", 12))
        semesters.grid(row=3, column=1, ipadx=15, ipady=5)

        self.sem_input = tk.Entry(self, font=("application", 12), width=1)
        self.sem_input.grid(row=3, column=2, ipadx=15, ipady=5)

        cred = tk.Label(self, text="Max. credit load per semester: ", font=("application", 12))
        cred.grid(row=4, column=1, ipadx=15, ipady=5)

        self.cred_input = tk.Entry(self, font=("application", 12), width=1)
        self.cred_input.grid(row=4, column=2, ipadx=15, ipady=5)

        self.course_input_win = None
        submit = tk.Button(self, text="Manual Course Input", font=("application", 12), command=self.launch_course_input)
        submit.grid(row=5, column=1, ipadx=15, sticky=tk.E)

        self.adviser = None
        select_file = tk.Button(self, text="Upload Excel Spreadsheet", font=("application", 12),
                                command=self.launch_file_selector)
        select_file.grid(row=6, column=1, ipadx=15, sticky=tk.E)

        self.bind("<Return>", self.launch_course_input)

    def launch_course_input(self, event=None):

        if mb.askokcancel(title="Continue to Course Input", message="Continue?", icon=mb.INFO):
            semesters = self.sem_input.get()
            cred = self.cred_input.get()

            try:
                semesters = int(semesters)
                cred = int(cred)
            except ValueError:
                mb.showerror(title="Input Error", message="Error processing your request. Please make sure you have "
                                                          "entered only numbers.", icon=mb.ERROR)
                return
            self.course_input_win = CourseInputWindow(self, semesters, cred)

    def launch_file_selector(self, event=None):

        if mb.askokcancel(title="Select File", message="Please select a valid .xlsx file from the following window.\n"
                                                       "If you do not have a template, download one from the "
                                                       "main menu.", icon=mb.QUESTION):
            filename = self.get_file()
            semesters = self.sem_input.get()
            cred = self.cred_input.get()

            try:
                _, db = temp.mkstemp(suffix=".db")
                courses, taken = util.import_courses(filename, db)
                semesters = int(semesters)
                cred = int(cred)
            except TypeError:
                mb.showerror(title="File Read Error", message="There was a problem with the format of your file.")
                return
            except FileNotFoundError:
                mb.showinfo(title="Select File", message="Operation was cancelled, or file could not be found.")
                return
            except ValueError:
                mb.showerror(title="Input Error", message="Error processing your request. Please make sure you have "
                                                          "entered only numbers.", icon=mb.ERROR)
                return

            adviser = ca.CourseAdviser(courses, taken, semesters_remaining=semesters, max_credits=cred)
            self.adviser = CourseAdviserWindow(self, adviser)

    @staticmethod
    def get_file():
        filename = file.askopenfilename(initialdir="/", title="Open File",
                                        filetypes=(("Excel spreadsheets", "*.xlsx"), ("all files", "*.*")))
        return filename


class CourseInputWindow(tk.Toplevel):

    def __init__(self, master, sem_cap=None, cred_cap=None, tasks=None):
        super().__init__(master)

        self.master = master

        if not tasks:
            self.tasks = []
        else:
            self.tasks = tasks

        self.courseview_canvas = tk.Canvas(self)

        # FIXME
        self.input_frame = CourseInputFrame(self, sem_cap, cred_cap)
        self.courseview_frame = tk.Frame(self.courseview_canvas)

        self.scrollbar = tk.Scrollbar(self.courseview_canvas, orient="vertical", command=self.courseview_canvas.yview)

        self.courseview_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.title("Add/Change Courses")
        self.geometry("880x500")

        # FIXME scrollbar causes entire program to crash
        self.input_frame.pack(side=tk.TOP, fill=tk.X)
        self.courseview_canvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.courseview_canvas.create_window((0, 0), window=self.courseview_frame, anchor='n')

        self.bind("<Configure>", self.on_frame_configure)

        # This feature is currently disabled due to a bug in Tk.
        # self.bind("<MouseWheel>", self.mouse_scroll)

    def on_frame_configure(self, event=None):
        self.courseview_canvas.configure(scrollregion=self.courseview_canvas.bbox("all"))

    def mouse_scroll(self, event):
        if event.delta:
            self.courseview_canvas.yview_scroll(-1 * (event.delta / 120), "units")
        else:
            if event.num == 5:
                move = 1
            else:
                move = -1

            self.courseview_canvas.yview_scroll(move, "units")


class CourseInputFrame(tk.Frame):

    def __init__(self, master, semester_cap, credit_cap):
        super().__init__(master)

        self.master = master

        # Temporary storage for Schedule object
        self.semester_cap = semester_cap
        self.credit_cap = credit_cap

        # TODO should be dicts to allow rapid course deletions
        self.courses = []
        self.taken = []

        self.adviser = None

        # Input Frame Widgets

        # Labels
        instructions = tk.Label(self, text="Enter your course details, or use an Excel spreadsheet. "
                                           "For prerequisites, use the format [SUBJ] [COURSE NUMBER] "
                                           "separated by "
                                           "commas. For example, CHEM 1601, ENGL 2200. 'MULTI' means the "
                                           "course "
                                           "can be taken multiple times for credit. Items in bold are "
                                           "required.",
                                font=("application", 12, "bold italic"), wraplength=700, justify=tk.LEFT)
        instructions.grid(row=1, column=1, columnspan=8, ipadx=5, ipady=10, sticky=tk.W)

        subj = tk.Label(self, text="SUBJECT", font=("application", 12, "bold"))
        subj.grid(row=2, column=1, ipadx=10)

        course_no = tk.Label(self, text="ID #", font=("application", 12, "bold"))
        course_no.grid(row=2, column=2, ipadx=10)

        cred = tk.Label(self, text="CREDITS", font=("application", 12, "bold"))
        cred.grid(row=2, column=3, ipadx=10)

        diff = tk.Label(self, text="DIFFICULTY", font=("application", 12))
        diff.grid(row=2, column=4, ipadx=10)

        pre = tk.Label(self, text="PREREQUISITES", font=("application", 12))
        pre.grid(row=2, column=5, ipadx=10)

        multi = tk.Label(self, text="MULTI?", font=("application", 12))
        multi.grid(row=2, column=6, ipadx=10)

        dl = tk.Label(self, text="DEADLINE", font=("application", 12))
        dl.grid(row=2, column=7, ipadx=10)

        taken = tk.Label(self, text="COMPLETED?", font=("application", 12))
        taken.grid(row=2, column=8, ipadx=10)

        # User Input
        self.subj_input = tk.Entry(self, font=("application", 12), width=4)
        self.subj_input.grid(row=3, column=1, ipadx=10)
        self.subj_input.focus()

        self.cn_input = tk.Entry(self, font=("application", 12), width=4)
        self.cn_input.grid(row=3, column=2, ipadx=10)

        self.cred_input = tk.Entry(self, font=("application", 12), width=3)
        self.cred_input.grid(row=3, column=3, ipadx=10)

        self.diff_input = tk.Scale(self, from_=0.0, to=100.0, tickinterval=50, font=("application", 12),
                                   orient=tk.HORIZONTAL, length=160)
        self.diff_input.grid(row=3, column=4)

        self.pre_input = tk.Entry(self, font=("application", 12))
        self.pre_input.grid(row=3, column=5, ipadx=10)

        self.is_multi = tk.IntVar()
        self.multi_input = tk.Checkbutton(self, variable=self.is_multi)
        self.multi_input.grid(row=3, column=6, ipadx=10)

        self.dl_input = tk.Entry(self, font=("application", 12), width=2)
        self.dl_input.grid(row=3, column=7, ipadx=10)

        self.is_taken = tk.IntVar()
        self.taken_input = tk.Checkbutton(self, variable=self.is_taken)
        self.taken_input.grid(row=3, column=8, ipadx=10)

        # Buttons todo button functions
        help_button = tk.Button(self, text="Need Help?", font=("Courier", 12))
        help_button.grid(row=5, column=5, ipadx=10)

        cancel = tk.Button(self, text="Cancel", font=("Courier", 12), command=self.quit)
        cancel.grid(row=5, column=6, ipady=10)

        add = tk.Button(self, text="Add Course", font=("Courier", 12), command=self.course_input_handler)
        add.grid(row=5, column=7, ipadx=10)

        self.master.bind("<Return>", self.course_input_handler)

        self.adviser_win = None

        submit = tk.Button(self, text="Finish", font=("Courier", 12), command=self.launch_adviser)
        submit.grid(row=5, column=8, ipadx=10)

        error_msg = "Error reading input. Please check that numerical inputs only contain numbers."
        self.error_message = self.error_message = tk.Label(self.master, text=error_msg,
                                                           font=("application", 12), wraplength=700, justify=tk.LEFT,
                                                           fg="red")

    def course_input_handler(self, event=None):
        self.error_message.grid_remove()
        if self.valid_input(self.subj_input.get(), str) and self.valid_input(self.cn_input.get(), int) and \
                self.valid_input(self.cred_input.get(), int):

            dl = int(self.dl_input.get()) if type(self.dl_input) is int else None

            new_course = planner.Course(int(self.cn_input.get()), self.subj_input.get().upper(),
                                        int(self.cred_input.get()), diff=int(self.diff_input.get()) / 100, deadline=dl,
                                        pre_reqs=self.pre_input.get().split(",") if self.pre_input.get() != '' else [],
                                        multi=self.is_multi.get())

            if self.is_taken.get():
                self.taken.append(new_course)
            else:
                self.courses.append(new_course)

            # Add the course
            add = str(new_course) + " || Prerequisites: " + str(new_course.pre_reqs) + \
                  " || Multi:  " + ("YES" if new_course.multi == 1 else "NO") + \
                  " || Taken: " + ("YES" if self.is_taken.get() == 1 else "NO")
            new_entry = tk.Label(self.master.courseview_canvas, text=add, font=("application", 12, "italic"),
                                 justify=tk.RIGHT)
            new_entry.grid(column=1)

        else:
            self.error_message.grid(ipadx=10, sticky=tk.W)

        # Reset inputs
        self.subj_input.delete(0, 'end')
        self.cn_input.delete(0, 'end')
        self.cred_input.delete(0, 'end')
        self.pre_input.delete(0, 'end')
        self.dl_input.delete(0, 'end')

        self.diff_input.set(0)

        self.multi_input.deselect()
        self.taken_input.deselect()

        self.subj_input.focus()

    @staticmethod
    def valid_input(data, expected_type: type):
        if expected_type == int:
            try:
                data = int(data)
            except ValueError:
                return False

        return type(data) is expected_type

    def launch_adviser(self, event=None):

        if mb.askokcancel("Continue", "Are you sure you want to proceed?", icon=mb.INFO):
            _, db = temp.mkstemp(suffix=".db")
            util.create_db(self.courses + self.taken, db)
            self.courses = util.pack(self.courses, db)
            self.taken = util.pack(self.taken, db)

            self.adviser = ca.CourseAdviser(self.courses, self.taken, semesters_remaining=self.semester_cap,
                                            max_credits=self.credit_cap)

            self.adviser_win = CourseAdviserWindow(self.master, self.adviser)


class CourseAdviserWindow(tk.Toplevel):

    def __init__(self, master, adviser=None):
        super().__init__(master)

        self.master = master

        self.title("Schedule")
        self.geometry("880x500")

        self.adviser = adviser

        self.adviser.plan()

        sub_title = tk.Label(self, text="Your Schedule", font=("application", 14, "italic bold"))
        sub_title.grid(row=1, column=0, sticky=tk.S, ipady=15, ipadx=10)

        for index, semester in enumerate(self.adviser.semesters):
            text = "Semester " + str(index + 1) + "\n" + str(semester)
            semester = tk.Label(self, text=text, font=("application", 12))
            semester.grid(row=3, column=index)

        export = tk.Button(self, text="Export as .xlsx file", font=("application", 12), command=self.export_as_xl)
        export.grid(row=4)

    def export_as_xl(self):
        if mb.askokcancel(title="Export file", message="Please choose where you want to export this file to.",
                          icon=mb.QUESTION):
            write_to = file.asksaveasfilename(defaultextension=".xlsx")
            util.write_to_file(self.adviser.schedule, dest=write_to)


if __name__ == "__main__":
    root = CnavRoot()
    root.mainloop()
