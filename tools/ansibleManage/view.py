"""
@author:lijx
@contact: 360595252@qq.com
@site: http://blog.51cto.com/breaklinux
@version: 1.0
"""
from flask import Blueprint
from flask import request, Response
from ansibleManage.ansibleApi import AnsibleApi

import os

HERE = os.path.abspath(__file__)
HOME_DIR = os.path.split(os.path.split(HERE)[0])[0]
script_path = os.path.join(HOME_DIR, "tools")
os.sys.path.append(script_path)
from tools.ansibleInventory import HostApi
from tools.auth import Check
ansibleUrl = Blueprint('ansible', __name__)


@ansibleUrl.route('/api/v1', methods=['GET', 'POST'])
@Check
def ansibleRun():
    import json
    from tools.bmc_log import bmcLogInster
    from ansibleManage.ansibleApi import AnsibleApi
    if request.method == "GET":
        return ansibleSelect()
    elif request.method == "POST":
        Data = request.get_json()
        inenory_ip = Data.get('instance_ip', None)
        command = Data.get('command', None)
        args = Data.get('args', None)
        becomeUser = Data.get("user", "ops")
        data = {"code": 1, "message": "instance_ip or command error"}
        if inenory_ip:
            t = HostApi()
            Ansible_run = AnsibleApi(script_path + "/inventory_static_hosts", "ops", becomeUser)
            Ansible_run.run(inenory_ip, command, args)
            reults = Ansible_run.get_result()
            if command == "shell":
                reults = ansibleCallbackFilter(reults)

            if ansibleInsert(inenory_ip, command, args, json.dumps(reults)):
                print("成功")
            else:
                print("失败")
            bmcLogInster("ansibleRun", request, reults)
            data = {"code": 0, "data": reults, "message": "success"}
        return Response(json.dumps(data), mimetype='application/json')
    elif request.method == "DELETE":
        pass

    else:
        parameterInfo = "参数错误,请检查"
        return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')

@Check
@ansibleUrl.route('/api/v2', methods=['GET', 'POST'])
def ansibleRun_v2():
    import json
    from tools.bmc_log import bmcLogInster
    from ansibleManage.ansibleApi import AnsibleApi
    if request.method == "GET":
        return ansibleSelect()
    elif request.method == "POST":
        Data = request.get_json()
        inenory_ip = Data.get('instance_ip', None)
        command = Data.get('command', None)
        args = Data.get('args', None)
        becomeUser = Data.get("user", "ops")
        if inenory_ip:

            t = HostApi()
            Ansible_run = AnsibleApi(script_path + "/inventory_static_hosts", "ops", becomeUser)
            Ansible_run.run(inenory_ip, command, args)
            reults = Ansible_run.get_result_v2()

            # reults = inenory_ops.Performer_Ansible(inenory_ip, command, args)
            if command == "shell":
                reults = ansibleCallbackFilter_v2(reults)

            if ansibleInsert(inenory_ip, command, args, json.dumps(reults)):
                print("成功")
            else:
                print("失败")
            bmcLogInster("ansibleRun", request, reults)
            return Response(json.dumps({"code": 0, "data": reults}), mimetype='application/json')
    elif request.method == "DELETE":
        pass

    else:
        parameterInfo = "参数错误,请检查"
        return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')
    
    
@ansibleUrl.route('/env/v1', methods=['GET', 'POST'])
def ansibleEnv():
    instanceModule = ansibelBase()
    data = instanceModule.Ansible_env()
    return Response(data, mimetype='application/json')

@ansibleUrl.route('/module/v1', methods=['GET', 'POST'])
def ansibleModule():
    instanceModule = ansibelBase()
    data = instanceModule.Ansible_module()
    return Response(data, mimetype='application/json')


def ansibleInsert(ip, command, args, callback):
    from models import db
    from models import bmc_ansible
    try:
        ansibleDataInsert = bmc_ansible(run_ip=ip, command_name=command, run_agrs=args, ansible_callback=callback)
        db.session.add(ansibleDataInsert)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False


def ansibleSelect():
    import json
    from models import bmc_ansible
    queryData = bmc_ansible.query.all()
    return Response(json.dumps({"code": 0, "total": len(queryData), "data": [i.to_dict() for i in queryData]}),
                    mimetype='application/json')


def ansibleCallbackFilter(callback):
    callbackData = dict()
    for i in callback:
        callbackData[i] = list()
        for x in callback[i]:
            if isinstance(callback[i][x], dict):
                callbackData[i].append({x: {"status": callback[i][x]["changed"],
                                            "messages": callback[i][x]["stdout"] or callback[i][x]["stderr"]}})
            else:
                callbackData[i].append({x: {"status": True, "messages": callback[i][x]}})
    return callbackData


def ansibleCallbackFilter_v2(callback):
    callbackData = dict()
    for i in callback:
        callbackData[i] = list()
        for x in callback[i]:
            print(x)
            callbackData[i].append({"status": x["result"]["changed"],
                                    "messages": x["result"]["stdout"] or x["result"]["stderr"],
                                    "ip": x["ip"]})
    return callbackData

class ansibelBase(object):
    def Ansible_module(self):
        import json
        #Commands_list = ["shell", "command", "script", "telnet", "raw", "expect", "psexec"]
        #File_list = ["copy", "fetch", "find", "stat", "file", "synchronize", "patch"]
        #Pckaging_list = ["yum", "yum_repository ", "maven", "npm", "gem", "pip", "bundler"]
        #Service_list = ["service"]
        #return json.dumps({"code": 0, "data": list(Command=Commands_list, File=File_list, Package=Pckaging_list,
        # 
        #                                      Service=Service_list)})
        name = ["shell"]
        used=["常用模块"]
        D = dict(zip(name,used))
        return json.dumps({"code": 0, "data": [{"name": x, "used": D[x]} for x in D]})

    def Ansible_env(self):
        import json
        key = ["dev","test","pre","pro"]
        display_name=["开发环境","测试环境","预发布环境","生产环境"]
        D = dict(zip(key, display_name))
        return json.dumps({"code": 0, "data":[{"key": x, "display_name": D[x]} for x in D]})


""""
1.ansible主机管理入口方法;
"""
@ansibleUrl.route('/host/v1', methods=['GET', 'POST','DELETE','PUT'])
def ansibleHostRun():
    try:
        if request.method == "GET":
            return ansibleHostSelect()
        elif request.method == "POST":
            return ansibleInsterHost()
        elif request.method == "DELETE":
            return hostDelete()
        elif request.method == "PUT":
            return updateHost()
        else:
            data = "方法不存在"
            return data
    except Exception as e:
        print(e)


"""
1.ansible 查询内部动态主机机器方法;
2.数据库查询
"""
def ansibleHostSelect():
    import json
    from models import bmc_ansible_hosts
    pagesize = request.args.get('page_size', 5, type=int)
    page = request.args.get('page', 1, type=int)
    from tools.config import DynamicHostHeader
    queryData = bmc_ansible_hosts.query.all()
    print(queryData)
    if page and pagesize:
          pagination = bmc_ansible_hosts.query.order_by(bmc_ansible_hosts.createtime.desc()).paginate(page, per_page=pagesize,
                                                                                          error_out=False)
          hostData = pagination.items
    else:
          parameterInfo = "参数不足或错误,请检查"
          return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')  
    return Response(json.dumps({"code": 0, "total": len(queryData), "data": [i.to_dict() for i in hostData],"columns":DynamicHostHeader,}, ),
        mimetype='application/json')
"""
1.删除主机ip地址
"""

def updateHost():
    import json
    try:
        Data = request.get_json()
        id = Data.get("id")
        host_ip = Data.get('instanceip', None)
        username = Data.get('username', None)
        password = Data.get('password', None)
        port = Data.get('port', None)
        group = Data.get("group")
        print(Data)
        data = ansibleUpdateHost(host_ip,username,password,port,group,id)
    except Exception as e:
        data = {"code": 500, "data": "必传参数不能为空", "message": str(e)}
    return Response(json.dumps(data), mimetype='application/json')

def hostDelete():
    import json
    try:
      Data = request.get_json()
      hostId = Data.get('id', None)
      data = anisbleDeleteHost(hostId)
      return Response(json.dumps(data), mimetype='application/json')
    except Exception as e:
        msg="参数不匹配"
    return Response(json.dumps({"code": 1, "message":msg}),
        mimetype='application/json')

""""
1.ansible 自管机器地址插入方法
2.支持多个IP地址进行插入;
"""
def ansibleInsterHost():
    import json
    from flask import Response
    from models import db
    from models import bmc_ansible_hosts
    import datetime
    Data = request.get_json()
    host_ip = Data.get('instanceip', None)
    username = Data.get('username', None)
    password = Data.get('password', None)
    port = Data.get('port', None)
    group = Data.get("group")
    print(Data)
    create_time = datetime.datetime.now()
    try:

        if host_ip and group and port and username and password:
            for i in host_ip:
                ansibleHostDataInsert = bmc_ansible_hosts(instanceip=i, username=username, password=password, port=port,
                                              group=group, createtime=create_time)
                db.session.add(ansibleHostDataInsert)
                db.session.commit()
            msg = "Insert Success"
            return Response(json.dumps({"code": 1, "data": msg}), mimetype='application/json')
        else:
            data = "参数缺少,不允许添加"
            return Response(json.dumps({"code": 1, "data": data}), mimetype='application/json')
    except Exception  as e:
        print(e)
        return Response(json.dumps({"code": 1, "data": "error"}), mimetype='application/json')
"""
1.ansible host机器删除
"""

def anisbleDeleteHost(IPID):
    from models import db
    from models import bmc_ansible_hosts
    try:
        deleteData = bmc_ansible_hosts.query.get(IPID)
        db.session.delete(deleteData)
        db.session.commit()
        data = "删除成功"
    except Exception as e:
        data = {"code": 1, "data": "删除主机失败", "message": str(e)}
    return {"code": 0, "data": data, "message": "success"}

"""
1.ansible host 更新
"""
def ansibleUpdateHost(host,username,password,port,group,id):
    from models import db
    from models import bmc_ansible_hosts
    import datetime
    create_time = datetime.datetime.now()

    print(create_time)
    try:
        bmc_ansible_hosts.query.filter_by(id=id).update({"instanceip":host , "username": username,
                                               "password": password,"port":port,
                                               "group":group})
        msg = "Update Success"
        db.session.commit()
        return {"code": 0,  "message": msg}
    except Exception as e:
        print(e)
        return {"code": 1, "data": None, "message": str(e)}
