create table posts(
    url         text    not null,   -- 链接
    title       text    not null,   -- 标题
    abstruct    text    not null,   -- 摘要
    raw         text    not null,   -- 源内容
    html        text    not null,   -- 渲染后内容
    tags        text    not null,   -- 标签
    keywords    text    not null,   -- 关键字
    time        text    not null,   -- 发布时间
    updatetime  text    not null,   -- 更新时间
    view        text    not null,   -- 阅读量
    published   text    not null,   -- 是否已发布 1：发布，0：未发布
    searchdict1 text    not null,   -- 搜索用字典1
    searchdict2 text    not null,   -- 搜索用字典2
    img         text    not null,   -- 文章图片
    primary key(url)
);

create view posts_card as 
select url,title,abstruct,tags,updatetime,img
from posts;

create view posts_show as 
select url,title,abstruct,tags,time,updatetime,view,published,html,keywords,img
from posts;

create view posts_list as 
select url,title,abstruct,time,published
from posts;

create view posts_edit as 
select url,title,abstruct,tags,time,updatetime,view,published,raw,img
from posts;



create table comments(
    id          text    not null,   -- 序号
    username    text    not null,   -- 显示的用户名
    email       text    not null,   -- 邮箱
    sendemail   text    not null,   -- 是否发送邮件
    url         text    not null,   -- 帖子链接
    raw         text    not null,   -- 评论原文
    html        text    not null,   -- 渲染后的评论
    time        text    not null,   -- 发布时间
    show        text    not null,   -- 是否显示
    ip          text    not null,   -- ip
    ad          text    not null,
    primary key(id)
);


create table friends(
    idx     text    not null,   -- 序号
    name    text    not null,   -- 名称
    url     text    not null,   -- 链接
    primary key(name)
);

create table pages(
    url         text not null,
    title       text not null,
    idx         text not null,
    show        text not null,
    primary key(url)
);

create table tags(
    chinese text    not null,   -- 中文
    english text    not null,   -- 英文
    cnt     text    not null,   -- 计数
    img     text    not null,   -- 图像
    class   text    not null,   -- 样式
    primary key(chinese)
);

create table siteConfig(
    sid     text    not null,
    name    text    not null,
    value   text    not null,
    idx     text    not null,
    primary key(sid)
);

insert into siteConfig(idx,sid,name,value) values('1',"password",'密码',"21232f297a57a5a743894a0e4a801fc3");
insert into siteConfig(idx,sid,name,value) values('2',"beian","备案信息","");
insert into siteConfig(idx,sid,name,value) values('3',"view","全站访问量","0");
insert into siteConfig(idx,sid,name,value) values('4',"smtp",'是否启用smtp',"0");
insert into siteConfig(idx,sid,name,value) values('5',"smtpemail","smtp账户","");
insert into siteConfig(idx,sid,name,value) values('6',"smtpservice","smtp服务器","");
insert into siteConfig(idx,sid,name,value) values('7',"smtpuser","smtp用户名","");
insert into siteConfig(idx,sid,name,value) values('8',"smtppassword","smtp密码","");
insert into siteConfig(idx,sid,name,value) values('9',"smtpport","smtp端口号","");
insert into siteConfig(idx,sid,name,value) values('10',"author","站点作者","");
insert into siteConfig(idx,sid,name,value) values('11',"sitename","站点名称","");
insert into siteConfig(idx,sid,name,value) values('12',"email","邮箱","");
insert into siteConfig(idx,sid,name,value) values('13',"rooturl","根目录","");
insert into siteConfig(idx,sid,name,value) values('14',"recommend","推荐","");

insert into pages (url,title,idx,show) values("index","首页","1","true");
insert into pages (url,title,idx,show) values("archives","归档","2","true");