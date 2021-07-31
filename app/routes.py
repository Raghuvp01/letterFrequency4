from flask import Flask
from flask import render_template

app = Flask(__name__, instance_relative_config=False)


@app.route('/')
def dashboard():
    return render_template(
        'dashboard.jinja2',
        title="Login Page",
        description="Smarter page templates with Flask & Jinja."
    )
