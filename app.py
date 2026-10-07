"""启动入口：python app.py。首次启动自动建表，无需安装 MySQL。"""
import os
import secrets
from pathlib import Path
from datetime import timedelta
from flask import Flask, session, request, jsonify, render_template
from werkzeug.exceptions import HTTPException
from config import Config, ROOT
from services.post_service import PostError
import database


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    if not app.config.get('SECRET_KEY'):
        key_path = ROOT / 'instance' / 'secret.key'
        key_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            fd = os.open(key_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            pass
        else:
            with os.fdopen(fd, 'w') as f:
                f.write(secrets.token_hex(32))
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or key_path.read_text()
    app.permanent_session_lifetime = timedelta(days=365)
    Path(app.config['DATABASE']).parent.mkdir(parents=True, exist_ok=True)
    Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
    database.init_app(app)
    from routes import register_routes
    register_routes(app)

    @app.before_request
    def identify_browser():
        if 'visitor_id' not in session:
            session['visitor_id'] = secrets.token_hex(24)
            session['csrf_token'] = secrets.token_hex(24)
            session.permanent = True
        if request.method in {'POST', 'PATCH', 'DELETE', 'PUT'}:
            token = request.headers.get('X-CSRF-Token', '')
            if not secrets.compare_digest(token, session['csrf_token']):
                return jsonify(error='页面已过期，请刷新后重试'), 403

    @app.context_processor
    def shared():
        return {'csrf_token': session.get('csrf_token', '')}

    @app.errorhandler(PostError)
    def post_error(error):
        if request.path.startswith('/api/'):
            return jsonify(error=str(error)), error.status
        return render_template('error.html', message=str(error)), error.status

    @app.errorhandler(HTTPException)
    def http_error(error):
        messages = {404: '没有找到这条信息', 413: '上传内容过大，请选择 5MB 以内的图片', 403: '无权进行此操作'}
        message = messages.get(error.code, error.description)
        if request.path.startswith('/api/'):
            return jsonify(error=message), error.code
        return render_template('error.html', message=message), error.code

    @app.after_request
    def headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'same-origin'
        response.headers['Content-Security-Policy'] = "default-src 'self'; img-src 'self' blob:; style-src 'self'; script-src 'self'; base-uri 'self'; frame-ancestors 'none'; form-action 'self'"
        if not request.path.startswith('/static/'):
            response.headers['Cache-Control'] = 'no-store'
        return response
    return app


if __name__ == '__main__':
    create_app().run(host='127.0.0.1', port=5000, debug=False)
