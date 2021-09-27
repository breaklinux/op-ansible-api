"""
@author:lijx
@contact: 360595252@qq.com
@site: http://blog.51cto.com/breaklinux
@version: 1.0
"""
from flask import Flask
from tools.config import MysqlConfig
from ansibleManage.view  import ansibleUrl
from channelAuth.view  import channelUrl
from flask_cors import CORS
def create_app():
    app = Flask(__name__)
    app.config.from_object(MysqlConfig)
    CORS(app, supports_credentials=True)
    from models import db
    db.init_app(app)
    app.register_blueprint(ansibleUrl,url_prefix='/ansible')
    app.register_blueprint(channelUrl,url_prefix='/channel')
    return app


