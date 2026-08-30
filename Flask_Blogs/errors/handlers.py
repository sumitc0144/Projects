from flask import Blueprint, render_template


errors = Blueprint("errors", __name__)


# Register a custom handler for 404 errors (Page Not Found)
@errors.app_errorhandler(404)
def error_404(error):
    # Render a custom 404 error template and return HTTP status code 404
    return render_template("errors/404.html", title="Page Not Found"), 404


# Register a custom handler for 500 errors (Internal Server Error)
@errors.app_errorhandler(500)
def error_500(error):
    # Render a custom 500 error template and return HTTP status code 500
    return render_template("errors/500.html", title="Server Error"), 500
