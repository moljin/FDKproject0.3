from flask import g, render_template
from flask_login import current_user


def related_app(app):
    from flask_www.configs import db

    """ === Request hook === """
    @app.errorhandler(404)
    def page_404(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(401)
    def page_401(error):
        return render_template('errors/401.html'), 401

    @app.template_filter('daytime')
    def _format_datetime(value, _type=None):  # 템플릿단 얘시: what_date|daytime("full")
        if _type == "full":
            _format = '%Y-%m-%d %H:%M:%S %p'
        elif _type == "medium":
            _format = '%Y-%m-%d %H:%M %p'
        else:
            _format = '%Y-%m-%d'
        return value.strftime(_format)

    @app.context_processor
    def inject_profile():
        from flask_www.accounts.models import Profile
        try:
            if current_user.is_authenticated:
                profile_obj = db.session.query(Profile).filter_by(user_id=current_user.id).first()
                return dict(profile=profile_obj)
            else:
                return dict(current_user=g.user)
        except Exception as e:
            print(e)

