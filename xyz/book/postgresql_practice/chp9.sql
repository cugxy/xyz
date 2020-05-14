
-- 创建 jsonb GIN索引
CREATE INDEX idx_gin ON tbl_user_jsonb USING GIN(user_info);
-- 创建 jsonb 数据键值索引
CREATE INDEX idx_gin_user_infob_user_name ON tbl_user_jsonb USING btree((user_info ->> 'user_name'));

-- json, jsonb 读写性能测试
CREATE TABLE IF NOT EXISTS user_ini (id int4, user_id int8, user_name character varying(64),
									 create_time timestamp(6) with time zone default clock_timestamp());
									 
CREATE TABLE IF NOT EXISTS tbl_user_json(id serial, user_info json);
CREATE TABLE IF NOT EXISTS tbl_user_jsonb(id serial, user_info jsonb);


INSERT INTO user_ini(id, user_id, user_name) 
SELECT r, round(random() * 2000000), r || '_francs'
FROM generate_series(1, 2000000) AS r;

-- INSERT 0 2000000

-- Query returned successfully in 29 secs 553 msec.
INSERT INTO tbl_user_json(user_info) 
SELECT row_to_json(user_ini) 
FROM user_ini;

-- Query returned successfully in 36 secs 369 msec.
INSERT INTO tbl_user_jsonb(user_info) 
SELECT row_to_json(user_ini)::jsonb 
FROM user_ini;

-- 使用索引前 456ms, 使用索引后0.12ms
EXPLAIN ANALYZE SELECT * FROM tbl_user_jsonb WHERE user_info->>'user_name'='1_francs';

CREATE INDEX idx_gin_user_infob_user_id ON tbl_user_jsonb USING btree((user_info ->> 'user_id'));
CREATE INDEX idx_gin_user_info_user_id ON tbl_user_json USING btree((user_info ->> 'user_id'));

-- 结论
-- json 写入比 jsonb 快, jsonb 读取比 json 快



