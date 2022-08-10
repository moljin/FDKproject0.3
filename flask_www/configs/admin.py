from flask import abort, redirect, url_for, request
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class AdminModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_admin:
            return current_user.is_authenticated
        else:
            return abort(404)
            # return "관리자 모드 접근 불가"

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        # return redirect(url_for('accounts.login', next=request.url))
        # def not_auth(self):
        return "관리자 모드 접근 불가"
        # return redirect(url_for('accounts.dashboard', next=request.url))


class NotificationsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/notify.html')


def add_views(admin):
    from flask_www.configs import db
    admin.add_view(NotificationsView(name='공지사항', endpoint='notify'))
    from flask_www.accounts.models import User, Profile
    admin.add_view(AdminModelView(User, db.session, name='이용자', menu_icon_type="fa", menu_icon_value="fa-users"))
    admin.add_view(AdminModelView(Profile, db.session, name='프로필', menu_icon_type="fa", menu_icon_value="fa-address-card"))