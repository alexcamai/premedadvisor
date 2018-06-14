"""
Author: Alex Camai
v 1.0.0
adviser.py

The adviser program.

Contains:
    CourseAdviser: Manages the course placement algorithm.

"""

from .planner import Schedule, Course
from collections import deque
from random import shuffle


class CourseAdviser:
    """
    Represents the Adviser that will solve the schedule.

    Attributes
        courses_taken: Courses that have been taken
        course_bucket: Courses that need to be taken
        subj_max:      Maximum number of each subject that can be taken in a semester
        schedule:      Schedule for remaining semesters
    """

    def __init__(self, courses_to_take: list('Course') = list(), courses_taken: list('Course') = list(),
                 *, subj_max: int = 3, semesters_remaining: int = 8, max_credits: int = 18, overload: int = 0,
                 diff: int = 0.75):
        """
        Constructor.

        :param courses_taken:         List of Courses already taken
        :param courses_to_take:       List of Courses to take
        :param subj_max:              Maximum number of Courses of each subject to take per semester
        :param semesters_remaining:   Semesters left to plan
        :param max_credits:           Maximum credit load allowed per semester (default 18)
        :param overload:              Maximum amount of credits allowed to overload (default 0)
        :param diff:                  Average difficulty (0.0-1.0) desired per semester (default 0.5/1.0)
        """
        self._course_bucket = deque(sorted(courses_to_take, reverse=True))
        self._schedule = Schedule(sem_remaining=semesters_remaining, max_credits=max_credits, overload=overload,
                                  diff=diff)
        self._subj_max = subj_max

        if len(courses_taken) == 0:
            self._courses_taken = dict()
        else:
            self._courses_taken = {course.get_course_code(): course for course in courses_taken}

    def plan(self):
        """
        plan

        Sorts all required courses into semesters based on credit load, difficulty, and prerequisites.

        :return: Tuple - (Schedule as it stands, True/False if success/failure)
        """
        # Currently a very unstable algorithm that gets less stable as more courses are inputted.
        for i in range(50):
            shuffle(self._course_bucket)
            result = self._place_courses()
            if result:
                print(str(self._schedule))
                return self._schedule, True
        return self._schedule, False

    def _place_courses(self):
        """
        _place_courses

        Private helper. Recursive backtracking solution that places Courses into the Schedule.

        :return: True if path succeeded; False if failed.
        """
        if len(self._course_bucket) == 0:
            return True
        cur = self._course_bucket.pop()
        for index in range(0, len(self._schedule.semesters)):
            if self._check(cur, index):
                self._add_course(cur, index)
                if self._place_courses():
                    return True
                else:
                    self._remove_course(cur, index)
        self._course_bucket.appendleft(cur)
        return False

    def _check(self, course: 'Course', index):
        """
        check

        Checks if the Course can be placed safely at the current Semester.

        :param course: Course to be placed
        :param index:  Semester to be checked (index must be in bounds of self._schedule.semesters)
        :return:       True/False if can/cannot place in this semester
        """
        for pre_req in course.pre_reqs:
            if pre_req.get_course_code() not in self._courses_taken:
                return False
            for ind in range(index, len(self._schedule.semesters)):
                if pre_req.get_course_code() in self._schedule.semesters[ind].courses:
                    return False
            if self._schedule.semesters[index].subj_dist.get(course.subj) is not None and \
                    self._schedule.semesters[index].subj_dist[course.subj] == self._subj_max:
                return False
            # if course.deadline > index + 1: TODO
            # return False
            # FIXME some hardcoded trash here.
            if pre_req.subj == course.subj and pre_req.id >= course.id - 100:
                return index > 0 and pre_req.get_course_code() in self._schedule.semesters[index - 1].courses and \
                       self._schedule.semesters[index].can_place(course)
        # FIXME subj limitations
        return self._schedule.semesters[index].can_place(course)

    def _add_course(self, course: 'Course', index: int):
        """
        _add_course

        Wrapper function to allow Adviser to add a course and keep track of it.

        pre: _check() for this course and index returned True.

        :param course:  Course to add
        :param index:   Semester (index of self._schedule.semesters) to add Course to
        """
        self._schedule.add_course(course, index)
        self._courses_taken[course.get_course_code()] = course

    def _remove_course(self, course: 'Course', index: int):
        """
        _remove_course

        Wrapper function to allow Adviser to remove a course and keep track of it.

        :param course:  Course to remove
        :param index:   Index to search for Course in (index of self._schedule.semesters)
        """
        self._schedule.remove_course(course.get_course_code(), index)
        if self._courses_taken.get(course.get_course_code()) is not None:
            del self._courses_taken[course.get_course_code()]

    # Getter (for GUI)

    @property
    def semesters(self):
        return self._schedule.semesters

    @property
    def schedule(self):
        return self._schedule

    # Debug

    def __len__(self):
        return len(self._schedule)

    def __str__(self):
        return ">>> courses_taken: " + str(self._courses_taken.keys()) + \
               "\n>>> course_bucket: " + str([course.get_course_code() for course in self._course_bucket]) + \
               "\n>>> schedule:\n" + str(self._schedule)
