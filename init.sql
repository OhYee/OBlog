create table posts(
    url         text    not null,   -- 链接
    title       text    not null,   -- 标题
    abstruct    text    not null,   -- 摘要
    raw         text    not null,   -- 源内容
    html        text,               -- 渲染后内容
    tags        text,               -- 标签
    keywords    text,               -- 关键字
    time        text    not null,   -- 发布时间
    updatetime  text    not null,   -- 更新时间
    view        text    not null,   -- 阅读量
    published   text    not null,   -- 是否已发布 1：发布，0：未发布
    searchdict1 text    not null,   -- 搜索用字典1
    searchdict2 text    not null,   -- 搜索用字典2
    primary key(url)
);

create table discuss(
    id          text    not null,   -- 序号
    username    text    not null,   -- 显示的用户名
    email       text,               -- 邮箱
    sendemail   text,               -- 是否发送邮件
    url         text    not null,   -- 帖子链接
    raw         text    not null,   -- 评论原文
    html        text    not null,   -- 渲染后的评论
    time        text    not null,   -- 发布时间
    show        text    not null,   -- 是否显示
    ip          text    not null,   -- ip
    primary key(id)
);

create table nav(
    idx     text    not null,   -- 序号
    name    text    not null,   -- 名称
    url     text    not null,   -- 链接
    icon    text,               -- 图标
    primary key(name)
);

create table friends(
    idx     text    not null,   -- 序号
    name    text    not null,   -- 名称
    url     text    not null,   -- 链接
    primary key(name)
);

create table SiteConfig(
    name    text    not null,
    value   text    not null,
    primary key(name)
);

create table GlobalVariable(
    name    text    not null,
    value   text    not null,
    primary key(name)
);


create table pages(
    urlpath     text    not null,
    filepath    text    not null,
    primary key(urlpath)
);

create table tags(
    chinese text    not null,   -- 中文
    english text    not null,   -- 英文
    cnt     text    not null,   -- 计数
    img     text,               -- 图像
    class   text,               -- 样式
    primary key(chinese)
);

insert into SiteConfig(name,value) values("Password","21232f297a57a5a743894a0e4a801fc3");
insert into SiteConfig(name,value) values("Record","");
insert into SiteConfig(name,value) values("view","0");
insert into SiteConfig(name,value) values("smtp","0");
insert into SiteConfig(name,value) values("smtpemail","");
insert into SiteConfig(name,value) values("smtpservice","");
insert into SiteConfig(name,value) values("smtpuser","");
insert into SiteConfig(name,value) values("smtppassword","");
insert into SiteConfig(name,value) values("smtpport","");
insert into SiteConfig(name,value) values("author","");
insert into SiteConfig(name,value) values("blogname","");
insert into SiteConfig(name,value) values("email","");
insert into SiteConfig(name,value) values("rooturl","");