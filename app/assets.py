from flask_assets import Bundle, Environment


def compile_auth_assets(app):
    assets = Environment(app)
    Environment.auto_build = True
    Environment.debug = False
    less_bundle = Bundle(
        "src/less/account.less",
        filters="less,cssmin",
        output="dist/css/account.css",
        extra={"rel": "stylesheet/less"},
    )
    js_bundle = Bundle("src/js/main.js", filters="jsmin", output="dist/js/main.min.js")
    assets.register("less_all", less_bundle)
    assets.register("js_all", js_bundle)
    if app.config["FLASK_ENV"] != "production":
        less_bundle.build(force=True)
        js_bundle.build()


def compile_main_assets(app):
    assets = Environment(app)
    Environment.auto_build = True
    Environment.debug = False
    less_bundle = Bundle(
        "src/less/dashboard.less",
        filters="less,cssmin",
        output="dist/css/dashboard.css",
        extra={"rel": "stylesheet/less"},
    )
    assets.register("less_all", less_bundle)
    if app.config["FLASK_ENV"] != "production":
        less_bundle.build(force=True)


def compile_static_assets(app):
    compile_auth_assets(app)
    compile_main_assets(app)
