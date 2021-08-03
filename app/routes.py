from flask import Blueprint
from flask import session, url_for
from flask_login import current_user, login_required, logout_user
import simplejson as json
from flask import request, Response, redirect
from flask import render_template

from app import mysql

home_bp = Blueprint(
    "home_bp", __name__, template_folder="templates", static_folder="static"
)


@home_bp.route('/', methods=['GET'])
@login_required
def index():
    user = {'username': 'Letter Frequency Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM letter_frequency')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, city=result[0])


@home_bp.route('/view/<int:city_id>', methods=['GET'])
@login_required
def record_view(city_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM letter_frequency WHERE id=%s', city_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', city=result[0])


@home_bp.route('/edit/<int:city_id>', methods=['GET'])
@login_required
def form_edit_get(city_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM letter_frequency WHERE id=%s', city_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', city=result[0])


@home_bp.route('/edit/<int:city_id>', methods=['POST'])
@login_required
def form_update_post(city_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Letter'), request.form.get('Frequency'), request.form.get('Percentage'), city_id)
    sql_update_query = """UPDATE letter_frequency t SET t.Letter = %s, t.Frequency = %s, t.Percentage = %s WHERE t.id 
    = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@home_bp.route('/cities/new', methods=['GET'])
@login_required
def form_insert_get():
    return render_template('new.html', title='New Form')


@home_bp.route('/cities/new', methods=['POST'])
@login_required
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Letter'), request.form.get('Frequency'), request.form.get('Percentage'))
    sql_insert_query = """INSERT INTO letter_frequency (Letter,Frequency,Percentage) VALUES (%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@home_bp.route('/delete/<int:city_id>', methods=['POST'])
@login_required
def form_delete_post(city_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM letter_frequency WHERE id = %s """
    cursor.execute(sql_delete_query, city_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@home_bp.route('/api/v1/cities', methods=['GET'])
@login_required
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM letter_frequency')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@home_bp.route('/api/v1/cities/<int:city_id>', methods=['GET'])
@login_required
def api_retrieve(city_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM letter_frequency WHERE id=%s', city_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@home_bp.route('/api/v1/cities/<int:city_id>', methods=['PUT'])
@login_required
def api_edit(city_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['Letter'], content['Frequency'], content['Percentage'], city_id)
    sql_update_query = """UPDATE letter_frequency t SET t.Letter = %s, t.Frequency = %s, t.Percentage = %s WHERE t.id 
    = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@home_bp.route('/api/v1/cities', methods=['POST'])
@login_required
def api_add() -> str:
    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['Letter'], content['Frequency'], content['Percentage'])
    sql_insert_query = """INSERT INTO letter_frequency (Letter,Frequency,Percentage) VALUES (%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@home_bp.route('/api/v1/cities/<int:city_id>', methods=['DELETE'])
@login_required
def api_delete(city_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM letter_frequency WHERE id = %s """
    cursor.execute(sql_delete_query, city_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@home_bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    session["redis_test"] = "This is a session variable."
    return render_template(
        "dashboard.jinja2",
        title="Flask-Session Tutorial.",
        template="dashboard-template",
        current_user=current_user,
        body="You are now logged in!",
    )


@home_bp.route("/session", methods=["GET"])
@login_required
def session_view():
    return render_template(
        "session.jinja2",
        title="Flask-Session Tutorial.",
        template="dashboard-template",
        session_variable=str(session["redis_test"]),
    )


@home_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_bp.login"))



