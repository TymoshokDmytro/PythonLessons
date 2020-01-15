class Queries:
    sql_get_all_students = "select * from students order by id"

    sql_get_student_by_field = "select * from students where {} = ?"

    sql_get_students_by_mark_gt_than = "select * from students where avg_mark >= ? order by avg_mark desc"

    sql_create_student = 'insert into students (fullname, department, "group", avg_mark, stud_ticket) VALUES (?, ?, ?, ?, ?)'

    sql_update_student = 'update students set {}=? where id = ?'

    sql_remove_student = 'delete from students where id=?'
