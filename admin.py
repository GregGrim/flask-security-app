from flask import request, url_for, redirect
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_login import current_user
from wtforms.fields.simple import BooleanField
from wtforms.widgets.core import CheckboxInput

from models import User, db, Role


class AccessController:

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('admin'))

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class AdminUserModelView(AccessController, ModelView):
    column_list = ['id', 'first_name', 'last_name', 'email', 'active', 'roles']
    column_exclude_list = ['password']
    form_excluded_columns = ['password']
    column_editable_list = ['active', 'roles']
    column_searchable_list = ['email']
    column_filters = ['email', 'active', 'roles']

    def scaffold_form(self):
        form_class = super(AdminUserModelView, self).scaffold_form()
        form_class.active = BooleanField('Active', widget=CheckboxInput())
        return form_class


class AdminRoleModelView(AccessController, ModelView):
    column_searchable_list = ['name']
    column_filters = ['name']


class LogoutMenuLink(AccessController, MenuLink):
    pass


class MyAdminIndexView(AccessController, AdminIndexView):

    @expose('/')
    def index(self):
        return redirect('/admin/user')


admin = Admin(name='Admin', template_mode='bootstrap3', index_view=MyAdminIndexView())


admin.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))
admin.add_view(AdminUserModelView(User, db.session))
admin.add_view(AdminRoleModelView(Role, db.session))
