"""
@author:lijx
@contact: 360595252@qq.com
@site: http://blog.51cto.com/breaklinux
@version: 1.0
"""
# -*- coding: utf-8 -*-
import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class bmc_ansible(db.Model):
    __tablename__ = 'bmc_ansible'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键自增长
    run_ip = db.Column(db.String(1024), nullable=False)  ###不能为空
    command_name = db.Column(db.String(64), nullable=False)  ###不能为空
    run_agrs = db.Column(db.Text, nullable=False)  ###不能为空
    ansible_callback = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime(timezone=False), default=datetime.datetime.now())

    def to_dict(self):
        return {"id": self.id, "run_ip": self.run_ip, "command_name": self.command_name, "run_agrs": self.run_agrs,
                "ansible_callback": self.ansible_callback}


class bmclog(db.Model):
    __tablename__ = 'bmc_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descname = db.Column(db.String(128), nullable=True)  #########模块名称###########
    source = db.Column(db.String(64), nullable=True)  ########ip源地址###########
    request = db.Column(db.Text, nullable=True)  #######请求参数##########
    response = db.Column(db.Text, nullable=True)  ########返回参数###########
    opsmethod = db.Column(db.String(64), nullable=True)  ########返回方法##########
    run_time = db.Column(db.DateTime(timezone=False), default=datetime.datetime.now())

    def to_dict(self):
        return {"id": self.id, "descname": self.descname, "source": self.source,
                "request": self.request, "response": self.response, "opsmethod": self.opsmethod, "run_time":
                    self.run_time}
    
class channel(db.Model):  ########认证code##########
    __tablename__ = 'bmc_channel'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(64), nullable=True)
    desc = db.Column(db.String(128), nullable=True)  ########这个uuid 给谁用###########
    owner = db.Column(db.String(64), nullable=True)
    uuid_use = db.Column(db.String(64), nullable=True)  #######这个uuid 给那个系统使用(用途)
    create_time = db.Column(db.DateTime(timezone=False), default=datetime.datetime.now())

    def to_dict(self):
        return {"id": self.id, "uuid": self.uuid, "desc": self.desc, "uuid_use": self.uuid_use,
                "owner": self.owner}

    

class bmc_ansible_hosts(db.Model):
    __tablename__ = 'bmc_ansible_hosts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键自增长
    host = db.Column(db.String(16), nullable=False)  ###不能为空
    username = db.Column(db.String(32), nullable=False)  ###不能为空
    password = db.Column(db.String(64), nullable=False)  ###不能为空
    port = db.Column(db.String(8), nullable=False)
    group = db.Column(db.String(24), nullable=False)
    createtime = db.Column(db.DateTime(timezone=False), default=datetime.datetime.now())

    def to_dict(self):
        return {"id": self.id, "host": self.host, "username": self.username, "password": self.password,
                "port": self.port, "group": self.group,"createtime": str(self.cratetime)}
