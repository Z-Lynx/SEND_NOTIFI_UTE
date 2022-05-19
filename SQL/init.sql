CREATE DATABASE DAOTAO;
USE DAOTAO;
CREATE TABLE THONGBAO(
    id int(40) not null,
    title longtext CHARSET utf8,
    content longtext CHARSET utf8,
    primary key(id)
);