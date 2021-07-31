from flask import Blueprint
from flask import render_template

main_bp = Blueprint(
    "main_bp", __name__, template_folder="templates", static_folder="static"
)


@main_bp.route("/", methods=["GET"])
def dashboard():
    return render_template(
        "dashboard.jinja2",
        title="Flask-Session Tutorial.",
        template="dashboard-template",
        body="You are now logged in!",
    )


@main_bp.route("/session", methods=["GET"])
def session_view():
    return render_template(
        "session.jinja2",
        title="Flask-Session Tutorial.",
        template="dashboard-template",
    )
