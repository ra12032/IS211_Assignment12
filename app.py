from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"


# --- DATABASE CONNECTION ---
def get_db_connection():
    conn = sqlite3.connect('hw13.db')
    conn.row_factory = sqlite3.Row
    return conn


# --- LOGIN PAGE ---
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # teacher login info
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid username or password."

    return render_template('login.html', error=error)


# --- LOGOUT ---
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# --- DASHBOARD ---
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    quizzes = conn.execute('SELECT * FROM quizzes').fetchall()
    conn.close()

    return render_template('dashboard.html', students=students, quizzes=quizzes)


# --- ADD STUDENT ---
@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    error = None

    if request.method == 'POST':
        first = request.form.get('first_name')
        last = request.form.get('last_name')

        if first and last:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO students (first_name, last_name) VALUES (?, ?)',
                (first, last)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('dashboard'))
        else:
            error = "Please fill out both fields."

    return render_template('add_student.html', error=error)


# --- ADD QUIZ ---
@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    error = None

    if request.method == 'POST':
        subject = request.form.get('subject')
        num_questions = request.form.get('num_questions')
        quiz_date = request.form.get('quiz_date')

        if subject and num_questions and quiz_date:
            try:
                num_questions = int(num_questions)
            except ValueError:
                error = "Number of questions must be a number."
            else:
                conn = get_db_connection()
                conn.execute(
                    'INSERT INTO quizzes (subject, num_questions, quiz_date) VALUES (?, ?, ?)',
                    (subject, num_questions, quiz_date)
                )
                conn.commit()
                conn.close()
                return redirect(url_for('dashboard'))
        else:
            error = "Please fill out all fields."

    return render_template('add_quiz.html', error=error)

# --- VIEW STUDENT QUIZ RESULTS ---
@app.route('/student/<int:student_id>')
def view_results(student_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = get_db_connection()

    # get that student's info
    student = conn.execute(
        'SELECT * FROM students WHERE id = ?',
        (student_id,)
    ).fetchone()

    # get that student's quiz results
    results = conn.execute(
        '''
        SELECT quiz_id, score
        FROM results
        WHERE student_id = ?
        ''',
        (student_id,)
    ).fetchall()

    conn.close()

    return render_template('results.html', student=student, results=results)

# --- ADD QUIZ RESULT ---
@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = get_db_connection()

    # get lists for dropdown menus
    students = conn.execute('SELECT * FROM students').fetchall()
    quizzes = conn.execute('SELECT * FROM quizzes').fetchall()

    error = None

    if request.method == 'POST':
        student_id = request.form.get('student_id')
        quiz_id = request.form.get('quiz_id')
        score = request.form.get('score')

        if student_id and quiz_id and score:
            try:
                score = int(score)
            except:
                error = "Score must be a number."
            else:
                conn.execute(
                    'INSERT INTO results (student_id, quiz_id, score) VALUES (?, ?, ?)',
                    (student_id, quiz_id, score)
                )
                conn.commit()
                conn.close()
                return redirect(url_for('dashboard'))
        else:
            error = "Please fill out all fields."

    conn.close()
    return render_template('add_result.html', students=students, quizzes=quizzes, error=error)


# --- START APP ---
if __name__ == '__main__':
    app.run(debug=True, port=5002)
