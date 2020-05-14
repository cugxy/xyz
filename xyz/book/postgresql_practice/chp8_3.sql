-- 内置分区表

-- 创建父表
-- 指定分区键为 create_time 分区策略为 range
CREATE TABLE IF NOT EXISTS log_par(
	id serial,
    user_id int4,
    create_time timestamp(0) without time zone
) PARTITION BY RANGE(create_time);

-- 创建分区
-- 必须指定父表和分区键取值范围, 注意不要有重叠
CREATE TABLE IF NOT EXISTS log_par_his 	PARTITION OF log_par FOR VALUES FROM ('1970-01-01') TO ('2017-01-01');
CREATE TABLE IF NOT EXISTS log_par_201701 PARTITION OF log_par FOR VALUES FROM ('2017-01-01') TO ('2017-02-01');
CREATE TABLE IF NOT EXISTS log_par_201702 PARTITION OF log_par FOR VALUES FROM ('2017-02-01') TO ('2017-03-01');
CREATE TABLE IF NOT EXISTS log_par_201703 PARTITION OF log_par FOR VALUES FROM ('2017-03-01') TO ('2017-04-01');
CREATE TABLE IF NOT EXISTS log_par_201704 PARTITION OF log_par FOR VALUES FROM ('2017-04-01') TO ('2017-05-01');
CREATE TABLE IF NOT EXISTS log_par_201705 PARTITION OF log_par FOR VALUES FROM ('2017-05-01') TO ('2017-06-01');
CREATE TABLE IF NOT EXISTS log_par_201706 PARTITION OF log_par FOR VALUES FROM ('2017-06-01') TO ('2017-07-01');
CREATE TABLE IF NOT EXISTS log_par_201707 PARTITION OF log_par FOR VALUES FROM ('2017-07-01') TO ('2017-08-01');
CREATE TABLE IF NOT EXISTS log_par_201708 PARTITION OF log_par FOR VALUES FROM ('2017-08-01') TO ('2017-09-01');
CREATE TABLE IF NOT EXISTS log_par_201709 PARTITION OF log_par FOR VALUES FROM ('2017-09-01') TO ('2017-10-01');
CREATE TABLE IF NOT EXISTS log_par_201710 PARTITION OF log_par FOR VALUES FROM ('2017-10-01') TO ('2017-11-01');
CREATE TABLE IF NOT EXISTS log_par_201711 PARTITION OF log_par FOR VALUES FROM ('2017-11-01') TO ('2017-12-01');
CREATE TABLE IF NOT EXISTS log_par_201712 PARTITION OF log_par FOR VALUES FROM ('2017-12-01') TO ('2018-01-01');

-- 分区创建索引
CREATE INDEX idx_log_par_his_create_time ON log_par_his USING btree(create_time);
CREATE INDEX idx_log_par_201701_create_time ON log_par_201701 USING btree(create_time);
CREATE INDEX idx_log_par_201702_create_time ON log_par_201702 USING btree(create_time);
CREATE INDEX idx_log_par_201703_create_time ON log_par_201703 USING btree(create_time);
CREATE INDEX idx_log_par_201704_create_time ON log_par_201704 USING btree(create_time);
CREATE INDEX idx_log_par_201705_create_time ON log_par_201705 USING btree(create_time);
CREATE INDEX idx_log_par_201706_create_time ON log_par_201706 USING btree(create_time);
CREATE INDEX idx_log_par_201707_create_time ON log_par_201707 USING btree(create_time);
CREATE INDEX idx_log_par_201708_create_time ON log_par_201708 USING btree(create_time);
CREATE INDEX idx_log_par_201709_create_time ON log_par_201709 USING btree(create_time);
CREATE INDEX idx_log_par_201710_create_time ON log_par_201710 USING btree(create_time);
CREATE INDEX idx_log_par_201711_create_time ON log_par_201711 USING btree(create_time);
CREATE INDEX idx_log_par_201712_create_time ON log_par_201712 USING btree(create_time);
-- 完成创建

-- 分区表使用
INSERT INTO log_par(user_id, create_time) 
SELECT round(100000000 * random()), generate_series('2016-11-01'::date, '2018-01-30'::date, '1 minute');

SELECT count(*) FROM log_par;
SELECT count(*) FROM ONLY log_par;

-- \d+log_par 元子命令可显示 log_par 表下得所有分区

-- 添加分区
CREATE TABLE IF NOT EXISTS log_par_201801 PARTITION OF log_par FOR VALUES FROM ('2018-01-01') TO ('2018-02-01');
CREATE INDEX idx_log_par_201801_create_time ON log_par_201801 USING btree(create_time);

-- 删除分区
-- 1. 直接删除分区表, 会丢失分区表内所有数据
DROP TABLE log_par_201801;

-- 2. 解绑分区, 只是将分区与父表关系断开, 数据保留, 再次连接分区即可恢复
ALTER TABLE log_par DETACH PARTITION log_par_201801;

-- 连接分区
ALTER TABLE log_par ATTACH PARTITION log_par_201801 FOR VALUES FROM ('2018-01-01') TO ('2018-02-01');


-- 性能测试
EXPLAIN ANALYZE SELECT * FROM log_par WHERE create_time > '2017-01-01' AND create_time < '2017-01-02';

CREATE INDEX idx_log_par_his_user_id ON log_par_his USING btree(user_id);
CREATE INDEX idx_log_par_201701_user_id ON log_par_201701 USING btree(user_id);
CREATE INDEX idx_log_par_201702_user_id ON log_par_201702 USING btree(user_id);
CREATE INDEX idx_log_par_201703_user_id ON log_par_201703 USING btree(user_id);
CREATE INDEX idx_log_par_201704_user_id ON log_par_201704 USING btree(user_id);
CREATE INDEX idx_log_par_201705_user_id ON log_par_201705 USING btree(user_id);
CREATE INDEX idx_log_par_201706_user_id ON log_par_201706 USING btree(user_id);
CREATE INDEX idx_log_par_201707_user_id ON log_par_201707 USING btree(user_id);
CREATE INDEX idx_log_par_201708_user_id ON log_par_201708 USING btree(user_id);
CREATE INDEX idx_log_par_201709_user_id ON log_par_201709 USING btree(user_id);
CREATE INDEX idx_log_par_201710_user_id ON log_par_201710 USING btree(user_id);
CREATE INDEX idx_log_par_201711_user_id ON log_par_201711 USING btree(user_id);
CREATE INDEX idx_log_par_201712_user_id ON log_par_201712 USING btree(user_id);

-- 结论
-- 1. 内置分区表根据非分区键查询相比普通表性能差距较大, 因为这种场景会会扫描所有分区
-- 2. 内置分区表根据分区键查询相比普通表性能有小幅降低, 而查询分区表子表性能相比普通表略有提升, 其他测试项分区表比普通表性能都低.
-- 3. 优点在于减少维护成本, 可数据动态扩容, 改变物理路径(磁盘盘符)

-- 更新分区数据
-- 内置分区表 update 操作目前不支持记录跨分区情况.

