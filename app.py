import MySQLdb
from flask import render_template, request, jsonify, json, redirect, url_for, session
from flask import Flask
from flask_mysqldb import MySQL

import check
import data
import database

app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1022'
app.config['MYSQL_DB'] = 'todo'

mysql = MySQL(app)
connection = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="1022",
    db="todo"
)
cursor = connection.cursor()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        _email = request.form['email']
        _password = request.form['password']
        print(_email, _password)
        if _email and _password:
            data = database.log_in_user(cursor, _email, _password)
            if len(data) >= 1:
                session['user'] = data[0][0]
                session['username'] = data[0][1]
                session['email'] = data[0][2]
                session['password'] = data[0][3]
                connection.commit()
                return redirect(url_for('index'))
            else:
                msg = 'incorrect email or password'
                return render_template('login.html', msg=msg)
    elif request.method == 'POST':
        msg = 'please fill the form'
        return render_template('login.html', msg=msg)
    return render_template('login.html')

@app.route('/settings',  methods=['GET', 'POST'])
def settings():
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form:
        _email = request.form['email']
        _name = request.form['username']
        _password = request.form['password']
        if _name and _email and _password:
            error_msg_email = ''
            error_msg_password = ''
            if not (check.check_email(_email)):
                error_msg_email = 'incorrect email address'
            if not (check.check_password(_password)):
                error_msg_password = 'your password must be at least 10 characters, and include at least one lowercase letter, one uppercase letter, a number, and a special character'
            if error_msg_email == error_msg_password:
                data = database.update_user_info(cursor, session.get('user'), _name, _email, _password)
                if len(data) is 0:
                    connection.commit()
                    session['username'] = _name
                    session['email'] = _email
                    session['password'] = _password
                    return redirect(url_for('settings'))
                else:
                    msg = 'user already exists'
                    return render_template('settings.html', msg1=msg)
            else:
                return render_template('settings.html', msg1=error_msg_email, msg2=error_msg_password)
    elif request.method == 'POST':
        msg = 'please fill the form'
        return render_template('settings.html', msg1=msg)
    return render_template('settings.html', done_today=database.stats_done_today(cursor, session.get('user')), all_today=database.stats_all_today(cursor, session.get('user')),
                           done=database.stats_done(cursor, session.get('user')), all=database.stats_all(cursor, session.get('user')),
    user_name=session.get('username'), user_password=session.get('password'), user_email=session.get('email'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form:
        _email = request.form['email']
        _name = request.form['username']
        _password = request.form['password']
        print(_name, _email, _password)
        if _name and _email and _password:
            error_msg_email = ''
            error_msg_password = ''
            if not(check.check_email(_email)):
                error_msg_email = 'incorrect email address'
            if not(check.check_password(_password)):
                error_msg_password = 'your password must be at least 10 characters, and include at least one lowercase letter, one uppercase letter, a number, and a special character'
            if error_msg_email == error_msg_password:
                data = database.sign_up_new_user(cursor, _name, _email, _password)
                if len(data) is 0:
                    connection.commit()
                    user = database.log_in_user(cursor, _email, _password)
                    print(user)
                    session['user'] = user[0][0]
                    session['username'] = user[0][1]
                    session['email']=user[0][2]
                    session['password']=user[0][3]
                    return redirect(url_for('index'))
                else:
                    msg = 'user already exists'
                    return render_template('signup.html', msg=msg)
            else:
                return render_template('signup.html', msg1=error_msg_email, msg2=error_msg_password)
    elif request.method == 'POST':
        msg = 'please fill the form'
        return render_template('signup.html', msg=msg)
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('username', None)
    session.pop('email', None)
    session.pop('password', None)

    return redirect(url_for('login'))

@app.route('/')
def index():
    if session.get('user'):
        items = database.fetch_todo(cursor, session.get('user'))

        return render_template('index.html', items=items, user_name=session.get('username'), data=data.get_data())
    else:
        return redirect(url_for('login'))


@app.route("/create", methods=['POST'])
def create():
    data = request.get_json()
    if data['description'] !='':
        database.insert_new_task(cursor, data['description'], data['day'], session.get('user'))
        connection.commit()
        result = {'success': True, 'response': 'Done'}
    else:
        result = {'success': False, 'response': 'Undone'}
    return jsonify(result)


@app.route("/edit/<int:task_id>", methods=['POST'])
def update(task_id):
    data = request.get_json()
    try:
        if "status" in data:
            database.update_status_entry(cursor, task_id, data["status"])
            connection.commit()
            result = {'success': True, 'response': 'Status Updated'}
        elif "description" in data:
            database.update_task_entry(cursor, task_id, data["day"], data["description"])
            connection.commit()
            result = {'success': True, 'response': 'Task Updated'}
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/delete/<int:task_id>", methods=['POST'])
def delete(task_id):
    try:
        database.remove_task_by_id(cursor, task_id)
        connection.commit()
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


if __name__ == "__main__":
    app.run()
