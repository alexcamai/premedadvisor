"""
Author: Alex Camai
v 1.0.0
Adviser.py

The adviser program.
"""
from ScheduleBits import Schedule, Course, Semester
from collections import deque
from random import shuffle


class CourseAdviser:
    """
    Represents the Adviser that will solve the schedule.

    Attributes
        courses_taken: Courses that have been taken.
        course_bucket: Courses that need to be taken.
        schedule:      Schedule for remaining semesters
    """

    def __init__(self, courses_taken: list('Course')=list(), courses_to_take: list('Course')=list()):
        """
        TODO
        :param courses_taken:
        """
        self._course_bucket = deque(courses_to_take)
        self._schedule = Schedule(sem_remaining=6)

        if len(courses_taken) == 0:
            self._courses_taken = dict()
        else:
            self._courses_taken = {course.get_course_code(): course for course in courses_taken}

        shuffle(self._course_bucket)

    def fill_schedule(self):
        # FIXME
        for i in range(50):
            shuffle(self._course_bucket)
            if self._add_course(0):
                return True
        return False

    def _add_course(self, index: int):
        if len(self._course_bucket) == 0:
            return True
        elif index >= len(self._schedule):
            if len(self._course_bucket) == 0:
                return True
            return False
        while index < len(self._schedule) and len(self._course_bucket) != 0:
            course = self._course_bucket.pop()
            result = self._schedule.add_course(course, index)
            if result == 'e':
                continue
            elif result == 'c':
                self._schedule.remove_course(course.get_course_code(), index)
                index += 1
            else:
                if self._check_prereqs(course, index):
                    self._courses_taken[course.get_course_code()] = course
                    return self._add_course(index)
            self._schedule.remove_course(course.get_course_code(), index)
            self._course_bucket.appendleft(course)
            if not self.continuable(index):
                index += 1
            # print("Moving with " + course.get_course_code() + " to Semester " + str(index + 1))

    def _check_prereqs(self, course: 'Course', index):
        for pre_req in course.pre_reqs:
            if pre_req.get_course_code() not in self._courses_taken:
                return False
            elif pre_req.get_course_code() in self._schedule.semesters[index].courses:
                return False
        return True

    def continuable(self, index):
        for course in self._course_bucket:
            if self._check_prereqs(course, index):
                return True
        return False

    # Debug

    def __str__(self):
        return ">>> courses_taken: " + str(self._courses_taken.keys()) + \
               "\n>>> course_bucket: " + str([course.get_course_code() for course in self._course_bucket]) + \
               "\n>>> schedule:\n" + str(self._schedule)
