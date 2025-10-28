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
if uri:
    # Heroku 互換の古い形式なら正規化
    if uri.startswith('postgres://'):
        uri = uri.replace('postgres://', 'postgresql+psycopg2://', 1)
    # SSL 必須なら追記（既にクエリがあれば & 、無ければ ?）
    if 'sslmode=' not in uri:
        uri = uri + ('?sslmode=require' if '?' not in uri else '&sslmode=require')
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
else:
    # ローカル開発用のフォールバック
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:ryota1231@localhost/postgres'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///migrate_tmp.db'


# if uri:
#     if uri.startswith('postgres://'):
#         uri=uri.replace('postgres://','postgresql://',1)
#         app.config['SQLALCHEMY_DATABASE_URI']=uri
# else:
#     app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:ryota1231@localhost'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
db= SQLAlchemy(app)
migrate = Migrate (app,db)
# print('bbbbbbbbbb')
# print(migrate)


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

from company_blog.models import User, BlogPost, BlogCategory, Inquiry

from company_blog.main.views import main
from company_blog.users.views import users
from company_blog.error_pages.handlers import error_pages

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(error_pages)
print('aaaaaaaaaaaaaaaa')
with app.app_context():
    print("tables:", db.metadata.tables.keys())

from sqlalchemy import inspect
from company_blog.models import BlogPost

with app.app_context():
    insp = inspect(db.engine)
    print("columns blog_post:", [c["name"] for c in insp.get_columns("blog_post")])
    try:
        print("BlogPost count:", db.session.query(BlogPost).count())
    except Exception as e:
        import traceback; print("COUNT FAILED:", e); traceback.print_exc()

# --- 一時デバッグ（終わったら消す） ---
import sqlalchemy as sa
with app.app_context():
    insp = sa.inspect(db.engine)
    print("schemas:", insp.get_schema_names())
    print("tables(public):", insp.get_table_names(schema="public"))
    try:
        cols = [c["name"] for c in insp.get_columns("blog_post", schema="public")]
        print("columns blog_post:", cols)
    except Exception as e:
        print("columns blog_post FAILED:", e)
# --- /デバッグ ---