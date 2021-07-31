from flask import Flask
from flask import render_template

app = Flask(__name__, instance_relative_config=False)


@app.route('/')
def dashboard():
    return render_template(
        "dashboard.jinja2",
        title="Flask-Session Tutorial.",
        template="dashboard-template",
        body="You are now logged in!",
    )


@app.route('/')
def session_view():
    return render_template(
        "session.jinja2",
        title="Flask-Session Tutorial.",
        template="dashboard-template",
    )
