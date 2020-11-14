    page = request.args.get('page', 1, type=int)
    if page and pagesize: 
       pagination = bmc_ansible.query.order_by(bmc_ansible.create_time.desc()).paginate(page, per_page=pagesize,                                                                                              error_out=False)
       resultQueryData = pagination.items
       return Response(json.dumps({"code": 0, "total": len(queryData), "data": [i.to_dict() for i in resultQueryData],"columns":AdhistoryHeader}),mimetype='application/json')
    else:
        parameterInfo = "请输入分页参数,请检查"
        return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json') 
		
		
