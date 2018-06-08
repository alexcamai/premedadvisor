"""
Author: Alex Camai
v 1.0.0
PreMedAdvisor.sql

Handles interaction with local databases.

Contains:
    create_db: Used to create a .db file based on a list of Courses.
    find:      Used to find a course based on its course code.

"""

from ScheduleBits import Course

import _sqlite3


def create_db(course_list: list('Course'), db: str = './courses.db'):
    """
    create_db

    Creates a database of Courses based on the list course_list.

    :param course_list: List of courses to make
    :param db:          Relative path to the database file
    """
    conn = _sqlite3.connect(db)

    c = conn.cursor()

    # Create the table
    c.execute("DROP TABLE IF EXISTS courses;")
    c.execute("CREATE TABLE courses(id text, subj text, num int, credit_load int, diff float, dl int, multi boolean);")

    # Insert each course using SQL queries
    for course in course_list:
        code = course.get_course_code()
        subj = course.subj
        num = course.id
        credit_load = course.credit_load
        diff = course.difficulty
        dl = course.deadline
        multi = course.multi

        c.execute('SELECT id FROM courses WHERE id=?;', (code,))
        if c.fetchone() is None:
            c.execute('''INSERT into courses VALUES (?, ?, ?, ?, ?, ?, ?);''',
                      (code, subj, num, credit_load, diff, dl, multi))

    # Save
    conn.commit()
    conn.close()


def find(courses: list(), db: str = './courses.db'):
    """
    find

    Returns a list of courses connected to the course codes in list courses.

    :param courses:       List of course KEYS to search for in the database
    :param db:            Relative path to database file
    :raises LookupError:  The course code was not found in the database
    :return:              List of Courses found
    """
    results = list()

    conn = _sqlite3.connect(db)

    c = conn.cursor()

    # Search for each course in the database, add to results list
    for course_code in courses:
        c.execute("SELECT * FROM courses WHERE id=?", (str(course_code.strip()),))
        row = c.fetchone()
        if row is not None:
            results.append(Course(row[2], row[1], row[3],
                                  diff=row[4], deadline=row[5]))
        else:
            raise LookupError("Error: Course " + course_code + " has no entries in the database.")

    conn.close()

    return results
