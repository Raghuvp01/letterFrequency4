from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect, session
from flask import render_template, url_for
# from flaskext.mysql import MySQL
from flask_mysqldb import MySQL
# from pymysql.cursors import DictCursor
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'raghu-key'
mysql = MySQL(app)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'letterData'
mysql.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return 'Logged in successfully!'
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'loggedin' in session:
        user = {'username': 'Letter Frequency Project'}
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM letter_frequency')
        result = cursor.fetchall()
        return render_template('index.html', title='Home', user=user, cities=result, username=session['username'])
    return redirect(url_for('login'))


@app.route('/view/<int:city_id>', methods=['GET'])
def record_view(city_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM letter_frequency WHERE id=%s', city_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', city=result[0])


@app.route('/edit/<int:city_id>', methods=['GET'])
def form_edit_get(city_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM letter_frequency WHERE id=%s', city_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', city=result[0])


@app.route('/edit/<int:city_id>', methods=['POST'])
def form_update_post(city_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    inputData = (request.form.get('Letter'), request.form.get('Frequency'), request.form.get('Percentage'), city_id)
    sql_update_query = """UPDATE letter_frequency t SET t.Letter = %s, t.Frequency = %s, t.Percentage = %s WHERE t.id 
    = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.connection.commit()
    return redirect("/", code=302)


@app.route('/cities/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Form')


@app.route('/cities/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    inputData = (request.form.get('Letter'), request.form.get('Frequency'), request.form.get('Percentage'))
    sql_insert_query = """INSERT INTO letter_frequency (Letter,Frequency,Percentage) VALUES (%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.connection.commit()
    return redirect("/", code=302)


@app.route('/delete/<int:city_id>', methods=['POST'])
def form_delete_post(city_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql_delete_query = """DELETE FROM letter_frequency WHERE id = %s """
    cursor.execute(sql_delete_query, city_id)
    mysql.connection.commit()
    return redirect("/", code=302)


@app.route('/api/v1/cities', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM letter_frequency')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:city_id>', methods=['GET'])
def api_retrieve(city_id) -> str:
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM letter_frequency WHERE id=%s', city_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:city_id>', methods=['PUT'])
def api_edit(city_id) -> str:
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    content = request.json
    inputData = (content['Letter'], content['Frequency'], content['Percentage'], city_id)
    sql_update_query = """UPDATE letter_frequency t SET t.Letter = %s, t.Frequency = %s, t.Percentage = %s WHERE t.id 
    = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.connection.commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities', methods=['POST'])
def api_add() -> str:
    content = request.json

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    inputData = (content['Letter'], content['Frequency'], content['Percentage'])
    sql_insert_query = """INSERT INTO letter_frequency (Letter,Frequency,Percentage) VALUES (%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.connection.commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:city_id>', methods=['DELETE'])
def api_delete(city_id) -> str:
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql_delete_query = """DELETE FROM letter_frequency WHERE id = %s """
    cursor.execute(sql_delete_query, city_id)
    mysql.connection.commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
