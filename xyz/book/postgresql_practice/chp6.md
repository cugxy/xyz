# 并行查询
9.6 及其之后版本支持

## 并行扫描

- 创建测试表
    ```
    create table if not exists test_big1(id int4, name character varying(32), create_time timestamp without time zone default clock_timestamp());

    insert into test_big1(id, name) select n, n||'_test' from generate_series(1, 50000000) n;
    ```

### 并行顺序扫描
- 查询语句
    ```
    explain analyze select * from test_big1 where name = '1_test';
    ```

- 结果对比
    ```
    # 非并行
    QUERY PLAN
    ---------------------------------------------------------------------------------------------
    Seq Scan on test_big1  (cost=0.00..991638.65 rows=1 width=25) (actual time=0.517..5385.317 rows=1 loops=1)
    Filter: ((name)::text = '1_test'::text)
    Rows Removed by Filter: 49999999
    Planning time: 0.051 ms
    Execution time: 5385.328 ms
    (5 行记录)

    # 并行
    QUERY PLAN
    ---------------------------------------------------------------------------------------------
    Gather  (cost=1000.00..523907.76 rows=1 width=25) (actual time=1.649..1890.737 rows=1 loops=1)
    Workers Planned: 4
    Workers Launched: 4
    ->  Parallel Seq Scan on test_big1  (cost=0.00..522907.66 rows=1 width=25) (actual time=1408.167..1785.954 rows=0 loops=5)
            Filter: ((name)::text = '1_test'::text)
            Rows Removed by Filter: 10000000
    Planning time: 0.044 ms
    Execution time: 1907.023 ms
    (8 行记录)
    ```

### 并行索引扫描

- 创建索引
    ```
    create index idx_test_big1_id on test_big1 using btree (id);
    ```
- 查询语句
    ```
    explain analyze select count(name) from test_big1 where id < 10000000;
    ```
- 结果对比
    ```
    # 非并行
    QUERY PLAN                                                                                   
    --------------------------------------------------------------------------------------------
    Aggregate  (cost=380583.48..380583.50 rows=1 width=8) (actual time=2672.560..2672.560 rows=1 loops=1)                                                                     
    ->  Index Scan using idx_test_big1_id on test_big1  (cost=0.56..355742.37 rows=9936446 width=13) (actual time=0.103..1997.040 rows=9999999 loops=1)                     
            Index Cond: (id < 10000000)            
    Planning time: 0.059 ms                                                                      
    Execution time: 2672.593 ms                                                                                                                                               
    (5 行记录) 

    # 并行            
    QUERY PLAN                                                                                 
    ---------------------------------------------------------------------------------------------
    Finalize Aggregate  (cost=288429.73..288429.74 rows=1 width=8) (actual time=947.498..947.498 rows=1 loops=1)                                                              
    ->  Gather  (cost=288429.31..288429.72 rows=4 width=8) (actual time=947.403..947.495 rows=5 loops=1)                                                                    
            Workers Planned: 4                                                                   
            Workers Launched: 4                                                                                                                                               
            ->  Partial Aggregate  (cost=287429.31..287429.32 rows=1 width=8) (actual time=833.994..833.994 rows=1 loops=5)                                                   
                ->  Parallel Index Scan using idx_test_big1_id on test_big1  (cost=0.56..281219.03 rows=2484112 width=13) (actual time=0.174..722.775 rows=2000000 loops=5) 
                        Index Cond: (id < 10000000)                                              
    Planning time: 1.282 ms                                                                     
    Execution time: 957.184 ms                                                                  
    (9 行记录)                  
    ```

### 并行 index-only 扫描
- 查询语句
    ```
    explain analyze select count(*) from test_big1 where id < 10000000;
    ```
- 结果对比
    ```
    # 非并行
    QUERY PLAN
    ---------------------------------------------------------------------------------------------
    Aggregate  (cost=380583.48..380583.50 rows=1 width=8) (actual time=2692.676..2692.677 rows=1 loops=1)
    ->  Index Only Scan using idx_test_big1_id on test_big1  (cost=0.56..355742.37 rows=9936446 width=0) (actual time=0.416..2186.206 rows=9999999 loops=1)
            Index Cond: (id < 10000000)
            Heap Fetches: 9999999
    Planning time: 0.214 ms
    Execution time: 2692.723 ms
    (6 行记录)

    # 并行
    QUERY PLAN
    ---------------------------------------------------------------------------------------------
    Finalize Aggregate  (cost=288429.73..288429.74 rows=1 width=8) (actual time=928.800..928.800 rows=1 loops=1)
    ->  Gather  (cost=288429.31..288429.72 rows=4 width=8) (actual time=928.697..928.796 rows=5 loops=1)
            Workers Planned: 4
            Workers Launched: 4
            ->  Partial Aggregate  (cost=287429.31..287429.32 rows=1 width=8) (actual time=812.421..812.421 rows=1 loops=5)
                ->  Parallel Index Only Scan using idx_test_big1_id on test_big1  (cost=0.56..281219.03 rows=2484112 width=0) (actual time=0.205..710.650 rows=2000000 loops=5)
                        Index Cond: (id < 10000000)
                        Heap Fetches: 2374755
    Planning time: 0.093 ms
    Execution time: 949.754 ms
    (10 行记录)
    ```

### 并行 bitmap heap 扫描
- 查询语句
    ```
    explain analyze select * from test_big1 where id = 1 or id = 2;
    ```
- 结果对比
    ```
    # 非并行
    QUERY PLAN
    ---------------------------------------------------------------------------------------------
    Bitmap Heap Scan on test_big1  (cost=9.15..17.16 rows=2 width=25) (actual time=0.014..0.015 rows=2 loops=1)
    Recheck Cond: ((id = 1) OR (id = 2))
    Heap Blocks: exact=1
    ->  BitmapOr  (cost=9.15..9.15 rows=2 width=0) (actual time=0.012..0.012 rows=0 loops=1)
            ->  Bitmap Index Scan on idx_test_big1_id  (cost=0.00..4.57 rows=1 width=0) (actual time=0.010..0.010 rows=1 loops=1)
                Index Cond: (id = 1)
            ->  Bitmap Index Scan on idx_test_big1_id  (cost=0.00..4.57 rows=1 width=0) (actual time=0.002..0.002 rows=1 loops=1)
                Index Cond: (id = 2)
    Planning time: 0.128 ms
    Execution time: 0.060 ms
    (10 行记录)

    # 并行
    QUERY PLAN
    ---------------------------------------------------------------------------------------------
    Bitmap Heap Scan on test_big1  (cost=9.15..17.16 rows=2 width=25) (actual time=0.089..0.103 rows=2 loops=1)
    Recheck Cond: ((id = 1) OR (id = 2))
    Heap Blocks: exact=1
    ->  BitmapOr  (cost=9.15..9.15 rows=2 width=0) (actual time=0.061..0.061 rows=0 loops=1)
            ->  Bitmap Index Scan on idx_test_big1_id  (cost=0.00..4.57 rows=1 width=0) (actual time=0.056..0.056 rows=1 loops=1)
                Index Cond: (id = 1)
            ->  Bitmap Index Scan on idx_test_big1_id  (cost=0.00..4.57 rows=1 width=0) (actual time=0.002..0.002 rows=1 loops=1)
                Index Cond: (id = 2)
    Planning time: 0.110 ms
    Execution time: 0.133 ms
    (10 行记录)
    ```

## 多表关联

- 创建测试表

    ```
    create table if not exists test_samll(id int4, name character varying(32));

    insert into test_samll(id, name) select n, n||'_samll' from generate_series(1, 8000000) n;

    create index idx_test_samll_id on test_samll using btree (id);
    ```
### Nested loop 多表关联

- 查询语句
    ```
    explain analyze select test_samll.name from test_big1, test_samll where test_big1.id = test_samll.id and test_samll.id < 10000;
    ```
- 结果对比
    ```
    # 非并行
    QUERY PLAN
    ---------------------------------------------------------------------------------------------
    Nested Loop  (cost=1.00..85597.76 rows=10153 width=13) (actual time=0.013..19.101 rows=9999 loops=1)
    ->  Index Scan using idx_test_samll_id on test_samll  (cost=0.43..358.11 rows=10153 width=17) (actual time=0.007..1.472 rows=9999 loops=1)
            Index Cond: (id < 10000)
    ->  Index Only Scan using idx_test_big1_id on test_big1  (cost=0.56..8.39 rows=1 width=4) (actual time=0.001..0.002 rows=1 loops=9999)
            Index Cond: (id = test_samll.id)
            Heap Fetches: 9999
    Planning time: 0.160 ms
    Execution time: 19.337 ms
    (8 行记录)

    # 并行
    QUERY PLAN
    ---------------------------------------------------------------------------------------------
    Gather  (cost=1191.68..54870.81 rows=10153 width=13) (actual time=1.500..149.400 rows=9999 loops=1)
    Workers Planned: 3
    Workers Launched: 3
    ->  Nested Loop  (cost=191.68..52855.51 rows=3275 width=13) (actual time=0.163..4.922 rows=2500 loops=4)
            ->  Parallel Bitmap Heap Scan on test_samll  (cost=191.12..25360.20 rows=3275 width=17) (actual time=0.158..0.434 rows=2500 loops=4)
                Recheck Cond: (id < 10000)
                Heap Blocks: exact=55
                ->  Bitmap Index Scan on idx_test_samll_id  (cost=0.00..188.58 rows=10153 width=0) (actual time=0.490..0.490 rows=9999 loops=1)
                        Index Cond: (id < 10000)
            ->  Index Only Scan using idx_test_big1_id on test_big1  (cost=0.56..8.39 rows=1 width=4) (actual time=0.001..0.002 rows=1 loops=9999)
                Index Cond: (id = test_samll.id)
                Heap Fetches: 9999
    Planning time: 0.221 ms
    Execution time: 163.449 ms
    (8 行记录)
    ```
### merge join 多表关联

- 查询语句
    ```
    explain analyze select test_samll.name from test_big1, test_samll where test_big1.id = test_samll.id and test_samll.id < 200000;
    ```
- 结果对比
    ```
    # 非并行
    QUERY PLAN
    ---------------------------------------------------------------------------------------------
    Merge Join  (cost=1.52..291649.59 rows=199448 width=13) (actual time=0.022..107.410 rows=199999 loops=1)
    Merge Cond: (test_big1.id = test_samll.id)
    ->  Index Only Scan using idx_test_big1_id on test_big1  (cost=0.56..1665063.56 rows=50000000 width=4) (actual time=0.010..32.047 rows=200000 loops=1)
            Heap Fetches: 200000
    ->  Index Scan using idx_test_samll_id on test_samll  (cost=0.43..6949.77 rows=199448 width=17) (actual time=0.010..29.740 rows=199999 loops=1)
            Index Cond: (id < 200000)
    Planning time: 0.162 ms
    Execution time: 112.318 ms
    (8 行记录)

    # 并行
    QUERY PLAN
    ---------------------------------------------------------------------------------------------
    Gather  (cost=1001.52..237199.38 rows=199448 width=13) (actual time=1.456..227.196 rows=199999 loops=1)
    Workers Planned: 4
    Workers Launched: 4
    ->  Merge Join  (cost=1.52..216254.58 rows=49862 width=13) (actual time=30.312..60.400 rows=40000 loops=5)
            Merge Cond: (test_big1.id = test_samll.id)
            ->  Parallel Index Only Scan using idx_test_big1_id on test_big1  (cost=0.56..1290063.56 rows=12500000 width=4) (actual time=0.091..6.733 rows=40001 loops=5)
                Heap Fetches: 166694
            ->  Index Scan using idx_test_samll_id on test_samll  (cost=0.43..6949.77 rows=199448 width=17) (actual time=0.029..35.046 rows=199999 loops=5)
                Index Cond: (id < 200000)
    Planning time: 0.206 ms
    Execution time: 236.606 ms
    (8 行记录)
    ```
### Hash join 多表关联
    当关联字段没有索引的情况下, 两表关联通常会进行 Hash join.
- 删除索引
    ```

    ```

- 查询语句
    ```
    explain analyze select test_samll.name from test_big1 join test_samll on (test_big1.id = test_samll.id) and test_samll.id < 100;
    ```
- 结果对比
    ```
    # 非并行
    QUERY PLAN
    ---------------------------------------------------------------------------------------------
    Hash Join  (cost=150875.75..1205047.75 rows=800 width=13) (actual time=4116.107..29980.084 rows=99 loops=1)
    Hash Cond: (test_big1.id = test_samll.id)
    ->  Seq Scan on test_big1  (cost=0.00..866664.00 rows=50000000 width=4) (actual time=0.021..22203.756 rows=50000000 loops=1)
    ->  Hash  (cost=150865.75..150865.75 rows=800 width=17) (actual time=4116.065..4116.065 rows=99 loops=1)
            Buckets: 1024  Batches: 1  Memory Usage: 13kB
            ->  Seq Scan on test_samll  (cost=0.00..150865.75 rows=800 width=17) (actual time=0.013..4116.044 rows=99 loops=1)
                Filter: (id < 100)
                Rows Removed by Filter: 7999901
    Planning time: 0.631 ms
    Execution time: 29980.131 ms

    # 并行
    QUERY PLAN
    ---------------------------------------------------------------------------------------------
    Gather  (cost=151875.75..690496.75 rows=800 width=13) (actual time=1149.288..3910.636 rows=99 loops=1)
    Workers Planned: 4
    Workers Launched: 4
    ->  Hash Join  (cost=150875.75..689416.75 rows=200 width=13) (actual time=3246.835..3799.086 rows=20 loops=5)
            Hash Cond: (test_big1.id = test_samll.id)
            ->  Parallel Seq Scan on test_big1  (cost=0.00..491664.00 rows=12500000 width=4) (actual time=0.016..2024.045 rows=10000000 loops=5)
            ->  Hash  (cost=150865.75..150865.75 rows=800 width=17) (actual time=1103.964..1103.964 rows=99 loops=5)
                Buckets: 1024  Batches: 1  Memory Usage: 13kB
                ->  Seq Scan on test_samll  (cost=0.00..150865.75 rows=800 width=17) (actual time=728.205..1103.934 rows=99 loops=5)
                        Filter: (id < 100)
                        Rows Removed by Filter: 7999901
    Planning time: 0.097 ms
    Execution time: 3926.640 ms
    ```
