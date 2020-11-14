CREATE TABLE `nginxManager_dj_nginx_conf` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_user` varchar(128) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `last_modified_time` datetime(6) NOT NULL,
  `last_modified_user` varchar(128) NOT NULL,
  `run_type` varchar(32) NOT NULL,
  `upstreamname` varchar(32) DEFAULT NULL,
  `front_listen` varchar(200) DEFAULT NULL,
  `domain_name` varchar(200) DEFAULT NULL,
  `backend_ip` varchar(128) DEFAULT NULL,
  `nginx_server` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=397 DEFAULT CHARSET=utf-8


# 删除所有数据
delete from user;
# 重置自增序列
alter table user auto_increment=1;