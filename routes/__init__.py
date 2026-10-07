def register_routes(app):
    from routes.pages import bp as pages_bp
    from routes.posts import bp as posts_bp
    app.register_blueprint(pages_bp)
    app.register_blueprint(posts_bp)
