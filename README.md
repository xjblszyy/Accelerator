# Accelerator
A robot that can automatically send preferential merchandise.

1: create database wx_robot charset=utf8;
2: create table goods( id int not null auto_increment, title varchar(200), price varchar(100), srcurl varchar(200), sn int, content varchar(1000), creat_time datetime null default current_timestamp);
3: set crontab