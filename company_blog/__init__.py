import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY']='mysecretkey'
basedir =os.path.abspath(os.path.dirname(__file__))

# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+ os.path.join(basedir,'data.sqlite')
uri=os.environ.get('DATABASE_URL')

def normalize_db_url(url: str) -> str:
    # psycopg3 方言に統一
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    # SSL 必須
    if "sslmode=" not in url:
        url += ("&" if "?" in url else "?") + "sslmode=require"
    return url

if uri:
    app.config["SQLALCHEMY_DATABASE_URI"] = normalize_db_url(uri)
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

# if uri:
#     if uri.startswith('postgres://'):
#         uri=uri.replace('postgres://','postgresql://',1)
#         app.config['SQLALCHEMY_DATABASE_URI']=uri
# else:
#     app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:ryota1231@localhost'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
db= SQLAlchemy(app)
Migrate (app,db)


login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='users.login'  #loginしないとこれによりloginに飛ばされる

# 飛ばされたときに出るメッセージ
def localize_callback(*args,**kwargs):
    return 'このページにアクセスするには、ログインが必要です'
login_manager.localize_callback=localize_callback

# from sqlalchemy.engine import Engine
# from sqlalchemy import event

# @event.listens_for(Engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()

from company_blog.main.views import main
from company_blog.users.views import users
from company_blog.error_pages.handlers import error_pages

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(error_pages)

