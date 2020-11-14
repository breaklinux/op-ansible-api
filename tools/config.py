"""
@author:lijx
@contact: 360595252@qq.com
@site: http://blog.51cto.com/breaklinux
@version: 1.0
"""
import os
ENVS = "dev,test,testone,ontest,prod"
class MysqlConfig(object):
    DIALECT = "mysql"
    DRIVER = "pymysql"
    USERNAME = "root"
    PASSWORD = "123456"
    HOST = "192.168.1.1"
    PORT = "3306"
    DATABASE = "op_bmc"
    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                                           PORT, DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

 ##########Ansible 认证授权UUID表头模板###############
ChanneUuidHeader=[{"name": "id", "alias":"唯一标识"},{"name": "uuid","alias":"授权uuid"},{"name":"desc","alias":"备注说明"},{"name":"owner","alias":"使用方"}, {"name":"uuid_use","alias":"用途"}]

ChanneIpHeader=[{"name": "id", "alias":"唯一标识"},{"name": "ip","alias":"授权IP地址"},{"name":"desc","alias":"备注说明"},{"name":"owner","alias":"使用方"}]


WhilteIpField = [
    {"name": "ip", "label": "授权IP地址", "fieldType": "TextInput","disabled": False, "cols": 8},
    {"name": "owner", "label": "使用方", "fieldType": "TextInput","disabled": False, "cols": 8},
    {"name": "desc", "label": "备注说明", "fieldType": "TextInput","disabled": False, "cols": 8}
]


WhilteUuidField = [
    {"name": "owner", "label": "使用方", "fieldType": "TextInput","disabled": False, "cols": 8},
    {"name": "uuid_use", "label": "用途", "fieldType": "TextInput", "disabled": False, "cols": 8},
    {"name": "desc", "label": "备注说明", "fieldType": "TextInput","disabled": False, "cols": 8}
]   
    
    

DynamicHostHeader=[
    {"name":"id","alias":"唯一标识"},{"name":"instanceip","alias":"主机IP"},
    {"name":"password","alias":"密码"},{"name":"username","alias":"用户"},
    {"name":"port","alias":"端口"},{"name":"group","alias":"主机组"},
    {"name":"createtime","alias":"创建时间"}]
