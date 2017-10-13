from flask_admin import Admin
from model.sql_models import Role, User, reflect_db
from .modelview import MyModelView

admin = Admin(name='后台管理系统', base_template='my_master.html')


def add_db_views(admin, app, db):
    admin.add_view(MyModelView(Role, db.session))
    admin.add_view(MyModelView(User, db.session))
    classes = reflect_db(app, db)
    for k, v in classes.items():
        admin.add_view(MyModelView(v, db.session))


__all__ = ["admin", "add_db_views"]
