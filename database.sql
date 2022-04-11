drop database if exists twitter;

create database twitter;

use twitter;

create table cailian (
    `id` int not null,
    `content` mediumtext not null,
    `ctime` real not null,
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;