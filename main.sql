use movie_system;

create table user
(
    id            bigint primary key auto_increment,
    nickname      varchar(30)                        not null,
    sex           tinyint                            not null,
    email         varchar(128)                       not null,
    password_hash varchar(128)                       not null,
    create_time   datetime default CURRENT_TIMESTAMP not null comment '创建时间',
    update_time   datetime                           not null on update CURRENT_TIMESTAMP comment '更新时间',
    unique index email (email),
    index create_time (create_time)
);