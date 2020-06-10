-- with 查询, 批量插入
with recursive t (x) as (
	select 1
	union 
	select x + 1
	from t
	where x < 5
)

-- union 合并结果集合
select * from t;

create table if not exists test_area (
 id smallint,
 name varchar(64),
 fatherid smallint
);

delete from test_area;

insert into test_area values (1, '中国', 0), (2, '辽宁', 1), (3, '山东', 1), (4, '沈阳', 2), (5, '大连', 2), (6, '济南', 3), (7, '和平区', 4), (8, '沈河区', 4);

with recursive r as (
	select * from test_area where id = 7
	union all
	select test_area.* from test_area, r where test_area.id = r.fatherid
)
select string_agg(name, '') from (select name from r order by id) n;

-- 4.3 returning 返回数据 
create table if not exists test_r1 (id serial, flag char(1));
insert into test_r1(flag) values ('a') returning *;
insert into test_r1(flag) values ('b') returning id;


-- 4.5 数据抽样
create table if not exists test_sample (id int4, message text, create_time timestamp(6) without time zone default clock_timestamp());
insert into test_sample(id, message) select n, md5(random()::text) from generate_series(1, 1500000) n;

select * from test_sample limit 1;

explain analyze select * from test_sample order by random() limit 15;

explain analyze select * from test_sample tablesample system(0.01);

select relname, relpages from pg_class where relname='test_sample';

select ctid, * from test_sample tablesample system(0.01);

explain analyze select * from test_sample tablesample bernoulli(0.01);

select ctid, * from test_sample tablesample bernoulli(0.01);


-- 4.6 聚合函数
create table if not exists city(country character varying(64), city character varying(64));
insert into city values ('中国', '台北'), ('中国', '香港'), ('中国', '上海'), ('日本', '东京'), ('日本', '大阪');

select country, string_agg(city, ',') from city group by country;
select country, array_agg(city) from city group by country;


-- 4.7 窗口函数
create table if not exists score(id serial primary key, 
								 subject character varying(32), 
								 stu_name character varying(32), 
								 score numeric(3, 0));
insert into score (subject, stu_name, score) values
('chinese', 'francs', 70),
('chinese', 'matiler', 70),
('chinese', 'tutu', 80),
('english', 'matiler', 75),
('english', 'francs', 90),
('english', 'tutu', 60),
('math', 'matiler', 99),
('math', 'tutu', 65),
('math', 'francs', 80);

select s.subject, s.stu_name, s.score, tmp.avgscore from score as s 
left join (select subject, avg(score) avgscore from score group by subject) tmp on s.subject = tmp.subject;

select subject, stu_name, score, avg(score) over (partition by subject) from score;

select row_number() over (partition by subject order by score desc), * from score;

select rank() over (partition by subject order by score), * from score;

select dense_rank() over (partition by subject order by score), * from score;

select lag(id, 1) over(), * from score;
select lag(id, 2, 1000) over(), * from score;

select first_value(score) over(partition by subject), * from score;
select first_value(score) over(partition by subject order by score desc), * from score;
select last_value(score) over(partition by subject), * from score;
select last_value(score) over(partition by subject order by score desc), * from score;
select nth_value(score, 2) over(partition by subject), * from score;

select avg(score) over(r), sum(score) over(r), * from score window r as (partition by subject);




