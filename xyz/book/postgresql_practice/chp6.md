# 并行查询
9.6 及其之后版本支持

## 并行扫描
### 并行顺序扫描

- 创建测试表
    ```
    create table if not exists test_big1(id int4, name character varying(32), create_time timestamp without time zone default clock_timestamp());

    insert into test_big1(id, name) select n, n||'_test' from generate_series(1, 50000000) n;
    ```
- 结果对比
    ```
    chp6=# set max_parallel_workers_per_gather = 0;
    SET
    chp6=# explain analyze select * from test_big1 where name = '1_test';
                                                    QUERY PLAN
    ------------------------------------------------------------------------------------------------------------
    Seq Scan on test_big1  (cost=0.00..991638.65 rows=1 width=25) (actual time=0.517..5385.317 rows=1 loops=1)
    Filter: ((name)::text = '1_test'::text)
    Rows Removed by Filter: 49999999
    Planning time: 0.051 ms
    Execution time: 5385.328 ms
    (5 行记录)


    chp6=# set max_parallel_workers_per_gather = 4;
    SET
    chp6=# explain analyze select * from test_big1 where name = '1_test';
                                                            QUERY PLAN

    ------------------------------------------------------------------------------------------------------------------------------
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
- 结果对比
    ```
    chp6=# set max_parallel_workers_per_gather = 0;                                              
    SET                                                                                                                                                               
    chp6=# explain analyze select count(name) from test_big1 where id < 10000000;               
    QUERY PLAN                                                                                   
    --------------------------------------------------------------------------------------------
    Aggregate  (cost=380583.48..380583.50 rows=1 width=8) (actual time=2672.560..2672.560 rows=1 loops=1)                                                                     
    ->  Index Scan using idx_test_big1_id on test_big1  (cost=0.56..355742.37 rows=9936446 width=13) (actual time=0.103..1997.040 rows=9999999 loops=1)                     
            Index Cond: (id < 10000000)            
    Planning time: 0.059 ms                                                                      
    Execution time: 2672.593 ms                                                                                                                                               
    (5 行记录) 

    chp6=# set max_parallel_workers_per_gather = 4;                                           
    SET 
    chp6=# explain analyze select count(name) from test_big1 where id < 10000000;                
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
    ```
    chp6=# set max_parallel_workers_per_gather = 0;
    SET

    chp6=# explain analyze select count(*) from test_big1 where id < 10000000;
    QUERY PLAN
    ---------------------------------------------------------------------------------------------
    Aggregate  (cost=380583.48..380583.50 rows=1 width=8) (actual time=2692.676..2692.677 rows=1 loops=1)
    ->  Index Only Scan using idx_test_big1_id on test_big1  (cost=0.56..355742.37 rows=9936446 width=0) (actual time=0.416..2186.206 rows=9999999 loops=1)
            Index Cond: (id < 10000000)
            Heap Fetches: 9999999
    Planning time: 0.214 ms
    Execution time: 2692.723 ms
    (6 行记录)


    chp6=# set max_parallel_workers_per_gather = 4;
    SET


    chp6=# explain analyze select count(*) from test_big1 where id < 10000000;
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
    ```
    chp6=# set max_parallel_workers_per_gather = 0;
    SET

    chp6=# explain analyze select * from test_big1 where id = 1 or id = 2;
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

    chp6=# set max_parallel_workers_per_gather = 4;
    SET

    chp6=# explain analyze select * from test_big1 where id = 1 or id = 2;
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
