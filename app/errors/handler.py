from flask import request, render_template
from app import db
from app.errors import bp

def wants_jason_response():
    return request.accept_mimetypes['application/json']>= request.accept_mimetypes['txt/html']

@bp.app_errorhandler(404)
def not_found_error(error):
    if wants_jason_response():
        return render_template('errors/404.html'), 404
    return  render_template('errors/404.html'),404

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if wants_jason_response():
        return render_template('errors/500.html'),500
    return render_template('errors/500.html'),500
