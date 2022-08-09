def routes_init(app):
    from flask_www.commons import common
    app.register_blueprint(common.common_bp)