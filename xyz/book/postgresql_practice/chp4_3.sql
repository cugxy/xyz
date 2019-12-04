create table if not exists test_r1 (id serial, flag char(1));

insert into test_r1(flag) values ('a') returning *;
insert into test_r1(flag) values ('b') returning id;
