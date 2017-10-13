import os
basedir = os.path.abspath(os.path.dirname("."))


class Config:
    SECRET_KEY = ""
    DB_URL = {"test": 'sqlite:///' + os.path.join(basedir, 'test.db')}
    SQLALCHEMY_BINDS = {
        'admin_users': 'sqlite:///' + os.path.join(basedir, 'admin.db')
    }
    SECRET_KEY = '123456790'

    # Create in-memory database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_ECHO = True

    # Flask-Security config
    SECURITY_URL_PREFIX = "/admin"
    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
    SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

    # Flask-Security URLs, overridden because they don't put a / at the end
    SECURITY_LOGIN_URL = "/login/"
    SECURITY_LOGOUT_URL = "/logout/"
    SECURITY_REGISTER_URL = "/register/"

    SECURITY_POST_LOGIN_VIEW = "/admin/"
    SECURITY_POST_LOGOUT_VIEW = "/admin/"
    SECURITY_POST_REGISTER_VIEW = "/admin/"

    # Flask-Security features
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # flask_babelex
    BABEL_DEFAULT_LOCALE = 'zh_CN'

    @staticmethod
    def init_app(app):
        pass
