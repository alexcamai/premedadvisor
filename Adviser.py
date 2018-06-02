"""
Author: Alex Camai
v 1.0.0
Adviser.py

The adviser program.
"""
from ScheduleBits import Schedule, Course, Semester
from collections import deque


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
        self._schedule = Schedule()

        if len(courses_taken) == 0:
            self._courses_taken = dict()
        else:
            self._courses_taken = {course.get_course_code(): course for course in courses_taken}

    def fill_schedule(self):
        if self._add_course(0):
            return True
        else:
            return False

    def _add_course(self, index: int):
        if index >= len(self._schedule) or len(self._course_bucket) == 0:
            return True
        first_attempt = self._course_bucket[-1]
        current_course = self._course_bucket.pop()
        while len(self._course_bucket) == 0 or self._course_bucket[-1] != first_attempt:
            if self._fits(current_course, index):
                self._schedule.add_course(current_course, index)
                # FIXME the below is only a temporary fix for the unimplemented _fits() function
                if self._add_course(index) or self._add_course(index + 1):
                    self._courses_taken[current_course.get_course_code()] = current_course
                    return True
                self._schedule.remove_course(current_course, index)
                self._course_bucket.appendleft(current_course)
                current_course = self._course_bucket.pop()

    def _fits(self, course: 'Course', index: int):
        return True

    # Debug

    def __str__(self):
        return "courses_taken: " + str(self._courses_taken) + "\ncourse_bucket: " + str(self._course_bucket) + "\n" \
                + "schedule:\n" + str(self._schedule)
