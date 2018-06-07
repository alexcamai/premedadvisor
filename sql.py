from ScheduleBits import Course

import _sqlite3


def create_db(course_list: list('Course'), db: str = './courses.db'):
    conn = _sqlite3.connect(db)

    c = conn.cursor()

    # Create the table
    # FIXME overwrite the table if it exists
    c.execute("DROP TABLE IF EXISTS courses;")
    c.execute("CREATE TABLE courses(id text, subj text, num int, credit_load int, diff float, dl int);")

    for course in course_list:
        code = course.get_course_code()
        subj = course.subj
        num = course.id
        credit_load = course.credit_load
        diff = course.difficulty
        dl = course.deadline

        c.execute('SELECT id FROM courses WHERE id=?;', (code,))
        if c.fetchone() is None:
            c.execute('''INSERT into courses VALUES (?, ?, ?, ?, ?, ?);''',
                      (code, subj, num, credit_load, diff, dl))

    # Save
    conn.commit()
    conn.close()


def find(courses: list(), db: str = './courses.db'):
    results = list()

    conn = _sqlite3.connect(db)

    c = conn.cursor()

    for course_code in courses:
        for row in c.execute("SELECT * FROM courses WHERE id=?", (str(course_code),)):
            if row is not None:
                results.append(Course(row['num'], row['subj'], row['credit_load'],
                                      diff=row['diff'], deadline=row['dl']))

    conn.close()
