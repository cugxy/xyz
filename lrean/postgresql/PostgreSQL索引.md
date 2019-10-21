# 简单查询和代价模型
## EXPLAIN
- 示例:
```
# 创建表 和插入数据
CREATE TABLE t_test (id serial, name text);

INSERT INTO t_test (name) SELECT 'hans' FROM generate_series(1, 2000000);
INSERT INTO t_test (name) SELECT 'paul' FROM generate_series(1, 2000000);

# EXPLAIN 作用与查询语句
EXPLAIN SELECT * FROM t_test WHERE id = 432332;
# 结果如下
                               QUERY PLAN
-------------------------------------------------------------------------
 Gather  (cost=1000.00..43455.43 rows=1 width=9)
   Workers Planned: 2
   ->  Parallel Seq Scan on t_test  (cost=0.00..42455.33 rows=1 width=9)
         Filter: (id = 432332)
(4 行记录)
```
- 官方说明:
```
命令：       EXPLAIN
描述：       显示一个语句块的执行计划
语法：
EXPLAIN [ ( 选项 [, ...] ) ] 语句
EXPLAIN [ ANALYZE ] [ VERBOSE ] 语句

选项可以是下列内容之一:

    ANALYZE [ 布尔 ]
    VERBOSE [ 布尔 ]
    COSTS [ 布尔 ]
    BUFFERS [ 布尔 ]
    TIMING [ 布尔 ]
    SUMMARY [ 布尔 ]
    FORMAT { TEXT | XML | JSON | YAML }
```
- 解释
  - 除第一行以外每个->表示一个子动作
  - 执行计划的阅读顺序都是从后至前
  - width=0是表示只获取行的位置,没有读取数据.开始读数据后width肯定大于0

## 代价模型
EXPLAIN 中将给出预计操作所会花费的代价, 代价计算如下:
- pg_relation_size: 返回表以字节为单位的大小, 读取 IO　所花的代价由其决定．
- cpu_tuple_cost　和　cpu_operator_cost：　cpu 应用过滤条件的代价.

## 使用简单索引
- 示例
```
 CREATE INDEX idx_id ON t_test (id);
```
Postgresql 使用 Lehman-Yao 的高并发性 B-Tree 作为标准索引, 同时进行了 Postgresql 专门优化. Lehman-Yao 让用户能够在同一时间在同一个索引上运行很多操作(读和写), 这有助于提升吞吐量.
但同时索引会占用磁盘空间, 会使写入变慢, 因为要保持索引同步.

- 使用索引
```
EXPLAIN SELECT * FROM t_test WHERE id = 432332;         # 查找
EXPLAIN SELECT * FROM t_test ORDER BY id DESC LIMIT 10; # 排序
EXPLAIN SELECT min(id), max(id) FROM t_test;            # min 和 max
``` 

## 使用多个索引
### 位图扫描
- 先扫描第一个索引, 收集含有数据块的一个列表. 然后第二个索引被扫描并且同样得到一块列表, 有多少个索引就会这样做多少次. 在 OR 的情况下, 这些列表会被统一, 留给我们一个由含有数据的块构成的大列表. 最后才会使用这个列表来扫描以检索出那些块.
- 位图扫描用例:
  - 避免反复的使用同一块
  - 组合相对不太好的条件


# 使用聚簇表改善速度
当数据以一种有组织的并且顺序的方式被装载到一个空表中, 那么这些数据将以连续的顺序存放在磁盘上.
上例中就是如此, 那如何建立一个混乱的呢? 如下:

```
postgresql_test=# CREATE TABLE t_random AS SELECT * FROM t_test ORDER BY random();
SELECT 4000000
postgresql_test=# CREATE INDEX idx_random ON t_random(id);
CREATE INDEX
```
- pg_stats: 是一个包含了所有有关列内容统计信息的系统视图.
```
SELECT tablename, attname, correlation FROM pg_stats WHERE tablename IN ('t_test', 't_random') ORDER BY 1, 2;
```
- ANALYZE: 收集数据库的统计信息

通常会有一个所谓的 autovacuum 守护进程在后台自动执行 ANALYZE.

```
SELECT tablename, attname, correlation FROM pg_stats WHERE tablename IN ('t_test', 't_random') ORDER BY 1, 2;

 tablename | attname | correlation
-----------+---------+-------------
 t_random  | id      |  0.00220119
 t_random  | name    |    0.499462
 t_test    | id      |           1
 t_test    | name    |           1
```
从以上可以看出, 对于 t_test.id 关联度是 1, 表示下一个值有些依赖于前一个值.就是因为 t_random 中较低的关联度, 导致了需要更多的块来提取等量的信息, 进而导致糟糕的性能.

## 聚簇表
- CLUSTER: 让我们能够以一种想要的顺序重写一个表, 可以指定一个索引并按该索引的顺序来存储数据, 即聚簇表
```
命令：       CLUSTER
描述：       按照索引进行表的聚集
语法：
CLUSTER [VERBOSE] 表名 [ USING 索引名称 ]
CLUSTER [VERBOSE]
```
  - CLUSTER 命令在运行时将锁住表, 在 CLUSTER 运行期间, 不能插入数据或则修改数据, 这对于生产系统可能时无法接受的.
  - 数据只能被按照一个索引进行组织. 用户不能同时通过 邮编, 姓名, ID, 生日等排序同一个表, 这意味着如果存在一个大部分时间都会被使用的搜索条件, CLUSTER就更有意义.
  - 实际上, 一个聚簇表和一个未聚簇表之间的性能差异将取决于负载, 接收到的数据量, 缓存命中率等很多因素
  - 如果一个表在正常操作时被更改, 它的聚簇状态将无法维持, 随着时间的流逝, 关联度可能恶化.
```
CLUSTER t_random USING idx_random
```
聚簇所需时间会根据表的尺寸而变化.

## 只用索引扫描
```
postgresql_test=# EXPLAIN SELECT * FROM t_test WHERE id=1234;
                             QUERY PLAN
---------------------------------------------------------------------
 Index Scan using idx_id on t_test  (cost=0.43..8.45 rows=1 width=9)
   Index Cond: (id = 1234)
(2 行记录)

postgresql_test=# EXPLAIN SELECT id FROM t_test WHERE id=1234;
                                QUERY PLAN
--------------------------------------------------------------------------
 Index Only Scan using idx_id on t_test  (cost=0.43..8.45 rows=1 width=4)
   Index Cond: (id = 1234)
(2 行记录)
```
上例中, 只搜索 id 列时, 计划从索引扫描边长了只用索引扫描, 因为 id 列已经被建立索引, 所以它的内容就应该存在与该索引中. 如果所有数据到可以从索引中取出, 那么在大部分情况下就没必要去表中取. 
实际上, 甚至可以在一个索引中包括额外列来享受这一特性, 在 MySQL 中, 增加额外列被称为 **覆盖索引** . PostgreSQL 也能实现类型形为.

# 理解另外的 B-Tree 特性
## 组合索引与个体索引
- 一般规则为: 如果单个索引能够回答用户的问题, 它通常就是最好的选择. 不过, 不可能在人们过滤域


