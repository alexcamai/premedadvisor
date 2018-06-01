"""
Author: Alex Camai
v 1.0.0
ScheduleBits.py

The moving pieces the adviser will reference.
"""


class Schedule:
    """
    Represents a schedule of classes for however many years are left.
    """

    def __init__(self): pass


class Semester:
    """
    Represents a semester of classes taken.

    Attributes
        TODO
    """

    def __init__(self, *, max_load=18, overload_cap=0, max_diff=0.75):
        """
        Constructor - Creates empty Semester with the following properties:

        :param max_load (int): Maximum amount of credits to take
        :param overload_cap (int): How many credits can be overloaded, if any. 0 as default.
        :param max_diff (float): The maximum difficulty rating of the semester
        """
        self._courses = dict()
        self._total_load = 0
        self._total_diff = 0
        self._diff_rating = 0.0
        self._max_load = max_load
        self._overload_cap = overload_cap
        self._max_diff = max_diff

    def add_course(self, *args):
        for course in args:
            key = course.subj + " " + str(course.id) + " " + str(course.credit_load)

            # Check if the course already exists
            if key in self._courses:
                return False

            if type(course) != Course:
                raise TypeError("Cannot use argument of type {} in list of type Course.".format(type(course)))

            if self._total_load + course.credit_load > self._max_load + self._overload_cap:
                return False

            self._total_load += course.credit_load
            new_diff = self._total_diff + course.difficulty

            # Check difficulty rating before adding
            new_diff_rating = new_diff / (len(self._courses) + 1)
            if new_diff_rating > self._max_diff:
                return False

            # Finally, add course and update attributes
            self._courses[key] = course
            self._total_diff = new_diff
            self._diff_rating = new_diff_rating

            return True

    # Debug

    def __str__(self):
        print(self._courses)


class Course:
    """
    Represents a course taken at university.
    """

    def __init__(self, id_no: int, subj: str, cred: int, *, diff=0.5, deadline=None, pre_reqs=()):
        """
        Constructor.

        :param id_no: Course's ID number
        :param cred:
        :param diff:
        :param deadline:
        :param pre_reqs:
        :type pre_reqs: tuple(Course)
        """
        self._id = id_no
        self._subj = subj
        self._credit_load = cred
        self._difficulty = diff
        self._deadline = deadline
        self._pre_reqs = pre_reqs

    # Relational Operators

    def __eq__(self, other):
        return self._subj == other.subj and self._id == other.id and self._credit_load == other.credit_load

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return self._subj > other.subj or self._id > other.id

    def __lt__(self, other):
        return not self.__gt__(other) and not self.__eq__(other)

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    # Setters and Getters

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

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

    # Debug

    def __str__(self):
        return "{} {} || load={} || difficulty={} || take by={}".format(self._subj, self._id,
                                                                        self._credit_load, self._difficulty,
                                                                        self._deadline)
