DROP TABLE IF EXISTS results;
DROP TABLE IF EXISTS quizzes;
DROP TABLE IF EXISTS students;

-- 1. Students table
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name  TEXT NOT NULL
);

-- 2. Quizzes table
CREATE TABLE quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject       TEXT NOT NULL,
    num_questions INTEGER NOT NULL,
    quiz_date     TEXT NOT NULL   -- store as 'YYYY-MM-DD'
);

-- 3. Results table (link student + quiz)
CREATE TABLE results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    quiz_id    INTEGER NOT NULL,
    score      INTEGER NOT NULL,  -- 0–100
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (quiz_id)   REFERENCES quizzes(id)
);

-- Sample data for the assignment:

-- student named "John Smith"
INSERT INTO students (first_name, last_name)
VALUES ('John', 'Smith');

-- quiz: "Python Basics", 5 questions, on Feb 5, 2015
INSERT INTO quizzes (subject, num_questions, quiz_date)
VALUES ('Python Basics', 5, '2015-02-05');

-- John Smith got 85 on that quiz
INSERT INTO results (student_id, quiz_id, score)
VALUES (1, 1, 85);