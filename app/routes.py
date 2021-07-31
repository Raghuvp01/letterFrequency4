from flask import current_app as app
from flask import render_template


@app.route('/')
def dashboard():
    return render_template(
        'dashboard.jinja2',
        title="Login Page",
        description="Smarter page templates with Flask & Jinja."
    )
