
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