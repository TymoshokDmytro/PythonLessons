class Queries:
    sql_get_all_students = """select s.*, m.avg_mark
from students s
join (select student_id, ROUND(AVG(mark), 2) as avg_mark from marks
group by student_id) m on s.id=m.student_id
"""

    sql_get_student_by_field = sql_get_all_students + " where {} = ?"

    sql_get_students_by_mark_gt_than = sql_get_all_students.replace('by student_id)', 'by student_id having avg(mark) >= ?)')

    sql_get_avg_mark_by_id = 'select ROUND(AVG(mark), 2) as avg_mark from marks where student_id = ?'

    sql_create_student = 'insert into students (fullname, department, "group", stud_ticket) VALUES (?, ?, ?, ?)'

    sql_insert_mark = 'insert into marks (student_id, mark) VALUES (?, ?)'

    sql_remove_marks_by_id = 'delete from marks where student_id = ?'

    sql_get_max_student_id = 'SELECT MAX(id) AS max_id FROM students'

    sql_update_student = 'update students set "{}" = ? where id = ?'

    sql_remove_student = 'delete from students where id=?'
