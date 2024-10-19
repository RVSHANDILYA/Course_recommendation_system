import sqlite3

# Create a new SQLite database (or connect to an existing one)
conn = sqlite3.connect('course_recommendation.db')

# Create a cursor object
cursor = conn.cursor()

# Create the users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
)
''')

# Create the courses table
cursor.execute('''
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT
)
''')

# Create the user_courses table (Many-to-Many relationship)
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_courses (
    user_id INTEGER,
    course_id INTEGER,
    PRIMARY KEY (user_id, course_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
)
''')

# Insert sample users
cursor.executemany('''
INSERT INTO users (name, email) VALUES (?, ?)
''', [
    ('Alice', 'alice@example.com'),
    ('Bob', 'bob@example.com'),
    ('Charlie', 'charlie@example.com')
])

# Insert sample courses
cursor.executemany('''
INSERT INTO courses (title, description) VALUES (?, ?)
''', [
    ('Python Programming', 'Learn the basics of Python programming.'),
    ('Data Science', 'Introduction to Data Science and Machine Learning.'),
    ('Web Development', 'Build modern web applications using HTML, CSS, and JavaScript.')
])

# Enroll users in courses
cursor.executemany('''
INSERT INTO user_courses (user_id, course_id) VALUES (?, ?)
''', [
    (1, 1),  # Alice enrolls in Python Programming
    (1, 2),  # Alice enrolls in Data Science
    (2, 1),  # Bob enrolls in Python Programming
    (3, 2),  # Charlie enrolls in Data Science
    (2, 3)   # Bob enrolls in Web Development
])

# Commit changes and close the connection
conn.commit()
conn.close()