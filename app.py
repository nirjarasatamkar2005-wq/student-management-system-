from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        course = request.form['course']

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO students (name, roll, course) VALUES (?, ?, ?)',
            (name, roll, course)
        )
        conn.commit()
        conn.close()

        return redirect('/students')
    return render_template('add_student.html')

@app.route('/students')
def students():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('view_students.html', students=students)

@app.route('/delete/<int:id>')
def delete_student(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/students')

if __name__ == '__main__':
    app.run(debug=True)
