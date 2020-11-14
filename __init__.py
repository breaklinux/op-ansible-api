"""
@author:lijx
@contact: 360595252@qq.com
@site: http://blog.51cto.com/breaklinux
@version: 1.0
"""
from flask import Flask
from tools.config import MysqlConfig
from ansibleManage.view  import ansibleUrl
def create_app():
    app = Flask(__name__)
    app.config.from_object(MysqlConfig)
    from models import db
    db.init_app(app)
    app.register_blueprint(ansibleUrl,url_prefix='/ansible')
    return app


