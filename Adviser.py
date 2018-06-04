"""
Author: Alex Camai
v 1.0.0
Adviser.py

The adviser program.
"""

from ScheduleBits import Schedule, Course
from collections import deque
from random import shuffle


class CourseAdviser:
    """
    Represents the Adviser that will solve the schedule.

    Attributes
        courses_taken: Courses that have been taken.
        course_bucket: Courses that need to be taken.
        subj_max:      Maximum number of each subject that can be taken in a semester
        schedule:      Schedule for remaining semesters
    """

    def __init__(self, courses_taken: list('Course') = list(), courses_to_take: list('Course') = list(),
                 subj_max: int = 3):
        """
        TODO
        :param courses_taken:
        """
        self._course_bucket = deque(sorted(courses_to_take, reverse=True))
        self._schedule = Schedule(sem_remaining=6)
        self._subj_max = subj_max

        if len(courses_taken) == 0:
            self._courses_taken = dict()
        else:
            self._courses_taken = {course.get_course_code(): course for course in courses_taken}

    def plan(self):
        # FIXME unstable
        for i in range(50):
            shuffle(self._course_bucket)
            result = self._place_courses()
            if result:
                print("Success; Courses placed: " + str(len(self._courses_taken)))
                return True
        print("Failed; Courses placed: " + str(len(self._courses_taken)) + ' / '
              + str(len(self._courses_taken) + len(self._course_bucket)))
        return False

    def _place_courses(self):
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
        for pre_req in course.pre_reqs:
            if pre_req.get_course_code() not in self._courses_taken:
                return False
            elif pre_req.get_course_code() in self._schedule.semesters[index].courses:
                return False
            if self._schedule.semesters[index].subj_dist.get(course.subj) is not None and \
                    self._schedule.semesters[index].subj_dist[course.subj] == self._subj_max:
                return False
            # FIXME some hardcoded trash here. Also, causes infinite loop
            if pre_req.subj == course.subj and pre_req.id > course.id - 100:
                return index > 0 and pre_req.get_course_code() in self._schedule.semesters[index - 1].courses and \
                       self._schedule.semesters[index].can_place(course)
        # FIXME subj limitations
        return self._schedule.semesters[index].can_place(course)

    def _add_course(self, course: 'Course', index: int):
        self._schedule.add_course(course, index)
        self._courses_taken[course.get_course_code()] = course

    def _remove_course(self, course: 'Course', index: int):
        self._schedule.remove_course(course.get_course_code(), index)
        if self._courses_taken.get(course.get_course_code()) is not None:
            del self._courses_taken[course.get_course_code()]

    # Debug

    def __str__(self):
        return ">>> courses_taken: " + str(self._courses_taken.keys()) + \
               "\n>>> course_bucket: " + str([course.get_course_code() for course in self._course_bucket]) + \
               "\n>>> schedule:\n" + str(self._schedule)
