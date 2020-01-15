from flask import Flask, render_template

from lesson08.classwork.db_data import STUDENTS

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', students=STUDENTS)

@app.route('/students/avg_mark/<int:id>')
def avg_mark(id):
    student = next(iter([stud for stud in STUDENTS if stud['id'] == id]))
    marks = student['marks']
    avg = sum(marks) / len(marks)
    return f"""
    <html>
        <body>
            <a href="/">Back</a>
            { 'Name=' + student['name'] + ' | Marks=' + str(marks) + ' | Avg=' + str(avg) }
        </body>
    </html>
    """


if __name__ == '__main__':
    app.run(debug=True)
