from flask import render_template
from app import db
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(not_found_404):
    return render_template('404.html'), not_found_404.code


@bp.app_errorhandler(500)
def internal_error(internal_server_error_500):
    db.session.rollback()
    return render_template('500.html'), internal_server_error_500.code
