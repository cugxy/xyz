# 分区表
PostgreSQL 10 之前的分区表一般通过继承加触发器方式实现, 步骤繁琐, 而 PostgreSQL10 版本支持内置分区表, 支持范围分区和列表分区.

## 分区表的意义
- 当查询或更新分区上的大部分数据时, 对分区进行索引扫描代价很大, 然而在分区上使用顺序扫描能够提升性能.
- 当需要删除一个分区数据是, 通过 DROP TABLE 删除一个分区, 远比 DELETE 删除数据高效.
- 由于一个表只能存储在一个表空间中, 使用分区表后, 可将分区分散到不同表空间.

## 传统分区表

### 继承表
示例:
```
-- 创建日志表
CREATE TABLE tb1_log(id INT4, create_date DATE, log_type TEXT);
-- 通过 inherits 创建 tb1_log_sql 继承自 tb1_log, 子表可定义额外字段, 且继承父表字段
CREATE TABLE tb1_log_sql(sql TEXT) INHERITS(tb1_log);

-- 插入数据
INSERT INTO tb1_log VALUES(1, '2020-01-19', null);
INSERT INTO tb1_log_sql VALUES(2, '2020-01-20', null, 'select 2');

-- 查询父表
select * from tb1_log;

 id | create_date | log_type
----+-------------+----------
  1 | 2020-01-19  |
  2 | 2020-01-20  |
(2 行记录)

-- 查询子表
select * from tb1_log_sql;
 id | create_date | log_type |   sql
----+-------------+----------+----------
  2 | 2020-01-20  |          | select 2
(1 行记录)

-- 可通过 OID 字段查询数据属于哪张表
select tableoid, * from tb1_log;
 tableoid | id | create_date | log_type
----------+----+-------------+----------
    92161 |  1 | 2020-01-19  |
    92167 |  2 | 2020-01-20  |
(2 行记录)

-- 使用 ONLY 关键字只查询父表
select * from only tb1_log;
 id | create_date | log_type
----+-------------+----------
  1 | 2020-01-19  |
(1 行记录)

```

### 创建分区表
1. 创建父表, 如果父表上定义了约束, 子表会继承, 因此除非是全局约束, 否则不应该在父表上定义约束, 另外, 父表不应该写入数据.
2. 通过 INHERITS 方式创建继承表, 也称之为子表或分区, 子表的字段定义应该和父表保持一致.
3. 给所有子表创建约束, 只有满足约束条件的数据才能写入对应分区, 注意分区约束范围不要有重叠.
4. 给所有子表创建索引, 由于继承操作不会继承父表上的索引, 因此需要手动创建索引.
5. 在父表上定义 INSERT, DELETE, UPDATE 触发器, 将 SQL 分发到对应分区.
6. 启用 constraint_exclusion 参数, 如果这个参数设置成 off, 则父表上的 SQL 性能会降低.

```
-- 创建表
CREATE TABLE if not exists log_ins(id SERIAL, user_id INT4, create_time TIMESTAMP(0) WITHOUT TIME ZONE);

create table if not exists log_ins_history(CHECK ( create_time < '2020-01-01')) inherits(log_ins);
create table if not exists log_ins_202001(CHECK ( create_time >= '2020-01-01' and create_time < '2020-02-01')) inherits(log_ins);
create table if not exists log_ins_202002(CHECK ( create_time >= '2020-02-01' and create_time < '2020-03-01')) inherits(log_ins);
create table if not exists log_ins_202003(CHECK ( create_time >= '2020-03-01' and create_time < '2020-04-01')) inherits(log_ins);
create table if not exists log_ins_202004(CHECK ( create_time >= '2020-04-01' and create_time < '2020-05-01')) inherits(log_ins);
create table if not exists log_ins_202005(CHECK ( create_time >= '2020-05-01' and create_time < '2020-06-01')) inherits(log_ins);
create table if not exists log_ins_202006(CHECK ( create_time >= '2020-06-01' and create_time < '2020-07-01')) inherits(log_ins);
create table if not exists log_ins_202007(CHECK ( create_time >= '2020-07-01' and create_time < '2020-08-01')) inherits(log_ins);
create table if not exists log_ins_202008(CHECK ( create_time >= '2020-08-01' and create_time < '2020-09-01')) inherits(log_ins);
create table if not exists log_ins_202009(CHECK ( create_time >= '2020-09-01' and create_time < '2020-10-01')) inherits(log_ins);
create table if not exists log_ins_202010(CHECK ( create_time >= '2020-10-01' and create_time < '2020-11-01')) inherits(log_ins);
create table if not exists log_ins_202011(CHECK ( create_time >= '2020-11-01' and create_time < '2020-12-01')) inherits(log_ins);
create table if not exists log_ins_202012(CHECK ( create_time >= '2020-12-01' and create_time < '2021-01-01')) inherits(log_ins);

-- 创建索引
create INDEX if not exists idx_his_ctime ON log_ins_history USING btree (create_time);
create INDEX if not exists idx_log_ins_202001_ctime ON log_ins_202001 USING btree (create_time);
create INDEX if not exists idx_log_ins_202002_ctime ON log_ins_202002 USING btree (create_time);
create INDEX if not exists idx_log_ins_202003_ctime ON log_ins_202003 USING btree (create_time);
create INDEX if not exists idx_log_ins_202004_ctime ON log_ins_202004 USING btree (create_time);
create INDEX if not exists idx_log_ins_202005_ctime ON log_ins_202005 USING btree (create_time);
create INDEX if not exists idx_log_ins_202006_ctime ON log_ins_202006 USING btree (create_time);
create INDEX if not exists idx_log_ins_202007_ctime ON log_ins_202007 USING btree (create_time);
create INDEX if not exists idx_log_ins_202008_ctime ON log_ins_202008 USING btree (create_time);
create INDEX if not exists idx_log_ins_202009_ctime ON log_ins_202009 USING btree (create_time);
create INDEX if not exists idx_log_ins_202010_ctime ON log_ins_202010 USING btree (create_time);
create INDEX if not exists idx_log_ins_202011_ctime ON log_ins_202011 USING btree (create_time);
create INDEX if not exists idx_log_ins_202012_ctime ON log_ins_202012 USING btree (create_time);

-- 创建触发器
CREATE OR REPLACE FUNCTION log_ins_insert_trigger()
    RETURNS trigger
	LANGUAGE plpgsql
AS $function$
BEGIN
   IF (NEW.create_time < '2020-01-01') THEN INSERT INTO log_ins_history VALUES (NEW.*);
   ELSIF (NEW.create_time >= '2020-01-01' and NEW.create_time < '2020-02-01') THEN INSERT INTO log_ins_202001 VALUES (NEW.*);
   ELSIF (NEW.create_time >= '2020-02-01' and NEW.create_time < '2020-03-01') THEN INSERT INTO log_ins_202002 VALUES (NEW.*);
   ELSIF (NEW.create_time >= '2020-03-01' and NEW.create_time < '2020-04-01') THEN INSERT INTO log_ins_202003 VALUES (NEW.*);
   ELSIF (NEW.create_time >= '2020-04-01' and NEW.create_time < '2020-05-01') THEN INSERT INTO log_ins_202004 VALUES (NEW.*);
   ELSIF (NEW.create_time >= '2020-05-01' and NEW.create_time < '2020-06-01') THEN INSERT INTO log_ins_202005 VALUES (NEW.*);
   ELSIF (NEW.create_time >= '2020-06-01' and NEW.create_time < '2020-07-01') THEN INSERT INTO log_ins_202006 VALUES (NEW.*);
   ELSIF (NEW.create_time >= '2020-07-01' and NEW.create_time < '2020-08-01') THEN INSERT INTO log_ins_202007 VALUES (NEW.*);
   ELSIF (NEW.create_time >= '2020-08-01' and NEW.create_time < '2020-09-01') THEN INSERT INTO log_ins_202008 VALUES (NEW.*);
   ELSIF (NEW.create_time >= '2020-09-01' and NEW.create_time < '2020-10-01') THEN INSERT INTO log_ins_202009 VALUES (NEW.*);
   ELSIF (NEW.create_time >= '2020-10-01' and NEW.create_time < '2020-11-01') THEN INSERT INTO log_ins_202010 VALUES (NEW.*);
   ELSIF (NEW.create_time >= '2020-11-01' and NEW.create_time < '2020-12-01') THEN INSERT INTO log_ins_202011 VALUES (NEW.*);
   ELSIF (NEW.create_time >= '2020-12-01' and NEW.create_time < '2021-01-01') THEN INSERT INTO log_ins_202012 VALUES (NEW.*);
   ELSE RAISE EXCEPTION 'create_time out of range. Fix the log_ins_insert_trigger() function!';
   END IF;
END;
$function$;

-- 定义父表 insert 触发器
CREATE TRIGGER insert_log_ins_trigger BEFORE INSERT ON log_ins FOR EACH ROW EXECUTE PROCEDURE log_ins_insert_trigger();

```

































