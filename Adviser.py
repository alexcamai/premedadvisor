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

    def __init__(self, courses_taken: list('Course')=list(), courses_to_take: list('Course')=list(), subj_max: int=3):
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

    def fill_schedule(self):
        # FIXME unstable
        for i in range(500):
            shuffle(self._course_bucket)
            try:
                result = self._add_course(0, self._course_bucket)
            except IndexError:
                continue
            if result:
                print("Success; Courses placed: " + str(len(self._courses_taken)))
                return True
        print("Failed; Courses placed: " + str(len(self._courses_taken)) + ' / '
              + str(len(self._courses_taken) + len(self._course_bucket)))
        return False

    def _add_course(self, index: int, course_bucket: deque):
        if len(course_bucket) == 0:
            return True
        elif index >= len(self._schedule):
            if len(course_bucket) == 0:
                return True
            return False
        while index < len(self._schedule) and len(course_bucket) != 0:
            course = course_bucket.pop()
            result = self._schedule.add_course(course, index)
            if result == 'e':
                continue
            elif result == 'c':
                self._schedule.remove_course(course.get_course_code(), index)
                index += 1
            else:
                if self._check(course, index):
                    self._courses_taken[course.get_course_code()] = course
                    return self._add_course(index, course_bucket)
            self._schedule.remove_course(course.get_course_code(), index)
            course_bucket.appendleft(course)
            if not self.continuable(index):
                index += 1
            # print("Moving with " + course.get_course_code() + " to Semester " + str(index + 1))

    def _check(self, course: 'Course', index):
        # TODO add functionality for course sequences (course sequences should be taken in consecutive semesters)
        for pre_req in course.pre_reqs:
            if pre_req.get_course_code() not in self._courses_taken:
                return False
            elif pre_req.get_course_code() in self._schedule.semesters[index].courses:
                return False
            # TODO course sequence implementation
            if pre_req.subj == course.subj and pre_req.id < course.id:
                return index > 0 and pre_req.get_course_code() in self._schedule.semesters[index - 1].courses
        return True
        # TODO logic is bad
        # course.subj not in self._schedule.semesters[index].subj_dist or \
        # self._schedule.semesters[index].subj_dist[course.subj] < self._subj_max

    def continuable(self, index):
        for course in self._course_bucket:
            if self._check(course, index):
                return True
        return False

    # Debug

    def __str__(self):
        return ">>> courses_taken: " + str(self._courses_taken.keys()) + \
               "\n>>> course_bucket: " + str([course.get_course_code() for course in self._course_bucket]) + \
               "\n>>> schedule:\n" + str(self._schedule)
