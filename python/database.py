def fetch_todo(cursor,_id) -> dict:
    cursor.execute("SELECT a.taskID, b.task_name, b.task_status, b.task_day FROM todo.user_tasks a inner join todo.tasks b on a.taskID=b.taskID Where a.userID='{}';".format(_id))
    todo_list = []
    for result in cursor:
        item = {
            "id": result[0],
            "task": result[1],
            "status": result[2],
            "day": result[3]
        }
        todo_list.append(item)
    return todo_list


def insert_new_task(cursor, text: str, day: str, user_id:int) -> int:
    query1 = "Insert Into todo.tasks (task_name, task_status,task_day ) VALUES ('{}', {}, '{}');".format(text, 0,
                                                                                                        day.lower())
    cursor.execute(query1)
    cursor.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in cursor]
    task_id = query_results[0][0]
    query2 = "INSERT INTO todo.user_tasks (taskID,userID) VALUES ({},{});".format(task_id, user_id)
    cursor.execute(query2)
    return task_id


def update_task_entry(cursor, task_id: int, day: str, text: str) -> None:
    query = "Update todo.tasks set task_name = '{}', task_day='{}' where taskID = {};".format(text, day, task_id)
    cursor.execute(query)


def update_status_entry(cursor, task_id: int, status: int) -> None:
    query = "Update todo.tasks set task_status = '{}' where taskID = {};".format(status, task_id)
    cursor.execute(query)


def remove_task_by_id(cursor, task_id: int) -> None:
    query1 = "Delete From tasks where taskID={};".format(task_id)
    query2 = "delete from todo.tasks where taskID={};".format(task_id)
    cursor.execute(query1)
    cursor.execute(query2)


def sign_up_new_user(cursor, _name, _email, _password) -> list:
    query = "CALL add_new_user('{}', '{}', '{}');".format(_name,_email,_password)
    cursor.execute(query)
    data = cursor.fetchall()
    return data

def log_in_user(cursor, _email, _password) -> list:
    query = "SELECT * FROM todo.users where user_login = '{}' and user_password='{}';".format(_email, _password)
    cursor.execute(query)
    data = cursor.fetchall()
    return data

def update_user_info(cursor, _id, _name, _email, _password) -> list:
    query = "CALL update_user_info('{}', '{}', '{}', '{}');".format(_id,_name, _email,_password,_id)
    cursor.execute(query)
    data = cursor.fetchall()
    return data

def stats_all_today(cursor, _id):
    query = "SELECT COUNT(*) AS plans_count FROM todo.tasks a inner join todo.user_tasks b on a.taskID=b.taskID WHERE LOWER(a.task_day) = LOWER(DAYNAME(NOW())) and b.userID = '{}';".format(_id)
    cursor.execute(query)
    data = cursor.fetchall()
    print(data[0][0])
    return data[0][0]

def stats_done_today(cursor, _id):
    query = "SELECT COUNT(*) AS plans_count FROM todo.tasks a inner join todo.user_tasks b on a.taskID=b.taskID WHERE LOWER(a.task_day) = LOWER(DAYNAME(NOW())) and b.userID = '{}' and a.task_status=1;".format(_id)
    cursor.execute(query)
    data = cursor.fetchall()
    print(data[0][0])
    return data[0][0]

def stats_all(cursor, _id):
    query = "SELECT COUNT(*) AS plans_count FROM todo.tasks a inner join todo.user_tasks b on a.taskID=b.taskID WHERE  b.userID = '{}';".format(_id)
    cursor.execute(query)
    data = cursor.fetchall()
    print(data[0][0])
    return data[0][0]

def stats_done(cursor, _id):
    query = "SELECT COUNT(*) AS plans_count FROM todo.tasks a inner join todo.user_tasks b on a.taskID=b.taskID WHERE b.userID = '{}' and a.task_status=1;".format(_id)
    cursor.execute(query)
    data = cursor.fetchall()
    print(data[0][0])
    return data[0][0]