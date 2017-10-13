import os
import sys
from flask import Flask, url_for, render_template
from flask_babelex import Babel
from flask_admin import helpers as admin_helpers
from flask_security import (Security,
                            SQLAlchemyUserDatastore)
from admin import admin
from config import choose_conf
from playhouse.db_url import connect
from apis import api
from model.peewee_models import database_proxys, init_db
from model.sql_models import User, Role, database, build_sample_db
from admin import add_db_views


def create_app(conf: str)->Flask:
    """
    用于创建flask的app
    """
    static_folder = os.path.split(os.path.realpath(sys.argv[0]))[0] + "/static"
    template_folder = os.path.split(os.path.realpath(sys.argv[0]))[
        0] + "/templates"
    database_path = os.path.split(os.path.realpath(sys.argv[0]))[
        0] + "/admin_users.db"
    app = Flask(__name__, template_folder=template_folder,
                static_folder=static_folder)
    app.config.setdefault('MANAGE_TABLES', None)
    app.config.setdefault('MANAGE_PROJECT', 'Target')
    conf = choose_conf(conf)
    app.config.from_object(conf)
    conf.init_app(app)
    db_urls = app.config.get("DB_URL")
    for k, v in db_urls.items():
        if k in database_proxys.keys():
            database_proxys.get(k).initialize(connect(v))
            init_db(database_proxys.get(k))
        else:
            print(f"找不到{k}对应的代理")

    database.init_app(app)
    database.app = app
    admin.init_app(app)
    user_datastore = SQLAlchemyUserDatastore(database, User, Role)
    security = Security(app, datastore=user_datastore)
    babel = Babel(app)
    add_db_views(admin, app, database)

    if conf not in ("testing", "test", "production"):
        database.drop_all(bind="admin_users")
        database.create_all(bind="admin_users")
        build_sample_db(database, app, user_datastore)

    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )
    api.init_app(app)
    return app


__all__ = ["create_app"]
