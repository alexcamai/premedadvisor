"""
Author: Alex Camai
v 1.0.0
ScheduleBits.py

The moving pieces the adviser will reference.

Contains:
    Schedule: Represents a collection of Semesters in one's academic career.
    Semester: Represents a collection of Courses.
    Course:   Represents the details around a course taken in university.

"""


class Schedule:
    """
    Represents a schedule of classes for however many years are left.

    Attributes
        semesters:      List of Semesters left to schedule
        courses_taken:  List of courses that have already been taken and credited for
    """

    def __init__(self, *, sem_remaining: int = 8, max_credits: int = 18, overload: int = 0, diff: int = 0.75):
        """
        Constructor.

        :param sem_remaining: Semesters remaining in the Schedule to be planned
        :param max_credits:   Maximum credits that should be taken
        :param overload:      Amount of credits that can be overloaded
        :param diff:          Maximum difficulty rating (between 0.0-1.0)
        """
        self._semesters = list()

        for i in range(sem_remaining):
            self._semesters.append(Semester(max_load=max_credits, overload_cap=overload, max_diff=diff))

    def add_course(self, course: 'Course', index: int):
        """
        add_course

        Attempts to add a course to the semester at index 'index'

        :raises: IndexError: Index was out of bounds.
        :param course: Course to add to Schedule.
        :param index: Year to add course to (0-based indexing)
        :return: Result code
        """
        if index >= len(self._semesters):
            raise IndexError("Index given was beyond the bounds of self._semesters")
        return self._semesters[index].add_course(course)

    def remove_course(self, key: str, index: int):
        """
        remove_course

        Attempts to remove a course from the semester at index 'index'

        :param key:         course_code of the Course to be deleted
        :param index:       Semester to search for the key Course in
        :raises IndexError: Index was out of bounds
        :return:            True or False based on success/failure
        """
        if index >= len(self._semesters):
            raise IndexError("Index given was beyond the bounds of self._semesters")
        return self._semesters[index].remove_course(key)

    # Setters and Getters

    @property
    def semesters(self):
        return self._semesters

    # Debug

    def __len__(self):
        return len(self._semesters)

    def __str__(self):
        result = "Semesters: \n"
        for i in range(len(self._semesters)):
            result += "\tSemester " + str(i + 1) + "\n" + str(self._semesters[i]) + "\n"
        return result


class Semester:
    """
    Represents a semester of classes taken.

    Attributes
        courses:        Dictionary of Courses currently enrolled in
        subj_dist:      Total count of courses of each subject
        total_load:     Total number of credits enrolled in
        total_diff:     Total of all difficulty ratings
        diff_rating:    Average difficulty rating of all courses (from 0.0-1.0)
        max_load:       Maximum number of credits that can be taken this semester
        overload_cap:   How many credits can be overloaded this semester
        max_diff:       Maximum difficulty rating (related to diff_rating)
    """

    def __init__(self, *, max_load=18, overload_cap=0, max_diff=0.5):
        """
        Constructor - Creates empty Semester with the following properties:

        :param max_load (int):      Maximum amount of credits to take
        :param overload_cap (int):  How many credits can be overloaded, if any. 0 as default
        :param max_diff (float):    The maximum difficulty rating for the semester
        """
        self._courses = dict()
        self._subj_dist = dict()
        self._total_load = 0
        self._total_diff = 0
        self._diff_rating = 0.0
        self._max_load = max_load
        self._overload_cap = overload_cap
        self._max_diff = max_diff

    def can_place(self, course: 'Course'):
        """
        can_place

        Shows if course can be added

        :raises: TypeError: Only Course objects can be added.
        :param course:  Course to be added

        :return: True/false if the course can/cannot be placed in this semester
        """
        if type(course) != Course:
            raise TypeError("Cannot use argument of type {} in list of type <class 'Course'>.".format(type(course)))

        key = course.get_course_code()

        # Check if the course already exists and can only be taken once
        if key in self._courses and not course.multi:
            return False

        # Check credit load before adding
        if self._total_load + course.credit_load > self._max_load + self._overload_cap:
            return False

        # Check difficulty rating before adding
        if (self._total_diff + course.difficulty) / (len(self._courses) + 1) > self._max_diff:
            return False

        return True

    def add_course(self, course: 'Course'):
        """
        Adds a Course to the Semester.

        pre: can_place(course) returned True.

        :param course: Course to be added.
        """

        new_diff = self._total_diff + course.difficulty
        new_diff_rating = new_diff / (len(self._courses) + 1)

        # Add course
        self._courses[course.get_course_code()] = course

        # Update attributes
        self._total_load += course.credit_load
        if self._subj_dist.get(course.subj) is None:
            self._subj_dist[course.subj] = 0
        self._subj_dist[course.subj] += 1
        self._total_diff = new_diff
        self._diff_rating = new_diff_rating

    def remove_course(self, key: str):
        """
        remove_course

        Remove a course from the Semester, by key.

        :param key: Key in format "[subj] [id] [credit load]"
        :return:    True if successfully removed, false if failed
        """
        if key in self._courses:
            self._total_load -= self._courses[key].credit_load
            self._total_diff -= self._courses[key].difficulty
            del self._courses[key]
            if len(self._courses) > 0:
                self._diff_rating = self._total_diff / len(self._courses)
            else:
                self._diff_rating = 0.0
            return True
        return False

    # Setters and Getters

    @property
    def courses(self):
        return self._courses

    @property
    def load(self):
        return self._total_load

    @property
    def difficulty(self):
        return self._diff_rating

    @property
    def subj_dist(self):
        return self._subj_dist

    # Other Attributes

    def __len__(self):
        return len(self._courses)

    def __str__(self):
        result = ""
        for key in self._courses:
            result += "\t\t>" + str(self._courses[key]) + "\n"
        return result


class Course:
    """
    Represents a course taken at university.

    Attributes
        id:             Course ID number
        subj:           Course subject
        credit_load:    Course's credit load
        diff:           Subjective course difficulty, on a scale of 0 to 1.0
        deadline:       The semester (starting with 0 for semester 1 year 1) the course must be scheduled at or before
        pre_reqs:       A tuple of prerequisites for the course, of type Course
        multi:   If the Course can be taken multiple times for credit
    """

    def __init__(self, id_no: int, subj: str, cred: int, *, diff: float = 0.5, deadline: int = 0,
                 pre_reqs: list('Course')=list(), multi: bool=False):
        """
        Constructor.

        :param id_no:       Course's ID number
        :param cred:        Credit load
        :param diff:        Difficulty rating 0-1.0
        :param deadline:    Deadline for course enrollment
        :param pre_reqs:    Prerequisite courses
        :param multi:       If can be taken multiple times for credit

        :type pre_reqs:     tuple(Course)
        """
        self._id = id_no
        self._subj = subj
        self._credit_load = cred
        self._difficulty = diff
        self._deadline = deadline
        self._pre_reqs = list(pre_reqs)
        self._multi = multi

    def get_course_code(self):
        """
        get_course_code

        :return: The course's unique course code in the format [SUBJ] [ID.NO] [CREDITS]
        """
        return self._subj + " " + str(self._id)

    # Relational Operators

    def __eq__(self, other: 'Course'):
        return self._subj == other.subj and self._id == other.id and self._credit_load == other.credit_load

    def __ne__(self, other: 'Course'):
        return not self.__eq__(other)

    # These are not "conventional" < and > operators

    def __gt__(self, other: 'Course'):
        return len(self.pre_reqs) > len(other.pre_reqs)

    def __lt__(self, other: 'Course'):
        return not self > other

    # Setters and Getters

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id):
        self._id = new_id

    @property
    def subj(self):
        return self._subj

    @subj.setter
    def subj(self, subj):
        self._subj = subj

    @property
    def credit_load(self):
        return self._credit_load

    @credit_load.setter
    def credit_load(self, load: int):
        self._credit_load = load

    @property
    def difficulty(self):
        return self._difficulty

    @difficulty.setter
    def difficulty(self, diff: float):
        self._difficulty = diff

    @property
    def deadline(self):
        return self._deadline

    @deadline.setter
    def deadline(self, dl: int):
        self._deadline = dl

    @property
    def pre_reqs(self):
        return self._pre_reqs

    @pre_reqs.setter
    def pre_reqs(self, pre: list('Course')):
        self._pre_reqs = pre

    @property
    def multi(self):
        return self._multi

    # Debug

    def __str__(self):
        return "{} {} || load={} || difficulty={} || take by={}".format(self._subj, self._id,
                                                                        self._credit_load, self._difficulty,
                                                                        self._deadline)
