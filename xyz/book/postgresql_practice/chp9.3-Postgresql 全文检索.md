# PostgreSQL 全文检索
## 简介
对于大多数应用来说，全文检索很少在数据库中实现，一般使用单独的全文检索引擎，例如基于SQL的全文检索引擎 Sphinx. PostgreSQL支持全文检索，对于规模不大的应用如果不想搭建专门的索引引擎，PostgreSQL的全文检索也可以满足需求。如果没有使用专门的搜索引擎，大部分检索都需要通过数据库 like 操作匹配，其缺点在于：
- 不能很好地支持索引，通常需要全表扫描检索数据，数据量大时性能低下。
- 不提供检索结果排序，当输出结果数据量非常大时表现更加明显。
PostgreSQL全文检索能够有效地解决这个问题，PostgreSQL全文检索通过以下两种数据类型来实现。

### 1.tsvector
tsvector 代表一个被优化的可以基于搜索的文档。将字符串转换成 tsvector 代码如下
```
SELECT 'Hello,cat,how are u? cat is smiling!'::tsvector;
// 输出
'Hello,cat,how' 'are' 'cat' 'is' 'smiling!' 'u?'
```
可以看到，字符串被分隔成好几段，但通过`::tsvector`只是做数据类型转换，没有进行数据标准化处理，对于英文全文检索可以通过函数 `to_tsvector` 进行数据标转化：
```
SELECT to_tsvector('english','hello cat,');
// 输出
'cat':2 'hello':1
```

### 2.tsquery
tsquery 表示一个文本查询，存储用于搜索的词，并支持布尔操作 `& | !` 

将字符串转换成 tsquery 如下：
```
SELECT 'hello&cat'::tsquery;
// 输出
'hello' & 'cat'
```
但通过`::tsquery`只是做数据类型转换，没有进行数据标准化处理，对于英文全文检索可以通过函数 `to_tsquery` 进行数据标转化：
```
SELECT to_tsquery('hello&cat');
// 输出
'hello' & 'cat'
```

一个全文检索示例如下：
```
// 检索字符串中是否包含 "hello" 和 "cat" 字符
SELECT to_tsvector('english', 'Hello cat, how are u') @@ to_tsquery('hello&cat');
// 输出
true
// 检索字符串中是否包含 "hello" 和 "dog"
SELECT to_tsvector('english', 'Hello cat, how are u') @@ to_tsquery('hello&dog');
// 输出 
false
```

> `to_tsvector` 双参数格式如下
```
to_tsvector([config regconfig, ]document text);
```
上述例子中，指定了config参数为 english，如果不指定config参数，则默认使用`default_text_search_config`参数的配置。

### 3 英文全文检索示例

```
-- 创建数据
create table test_search(id int4, name text);
insert into test_search(id, name) select n, n||'_francs' from generate_series(1,2000000) n;

-- like 查询
explain analyze select * from test_search where name like '1_francs';
--"Gather  (cost=1000.00..24166.67 rows=200 width=18) (actual time=0.802..165.361 rows=1 loops=1)"
--"  Workers Planned: 2"
--"  Workers Launched: 2"
--"  ->  Parallel Seq Scan on test_search  (cost=0.00..23146.67 rows=83 width=18) (actual time=18.940..73.792 rows=0 loops=3)"
--"        Filter: (name ~~ '1_francs'::text)"
--"        Rows Removed by Filter: 666666"
--"Planning time: 0.091 ms"
--"Execution time: 170.762 ms"

-- 创建 gin 索引
create index idx_gin_search on test_search using gin(to_tsvector('english', name));

-- 使用索引查询
explain analyze select * from test_search where to_tsvector('english', name) @@ to_tsquery('english', '1_francs');
--"Bitmap Heap Scan on test_search  (cost=36.39..240.11 rows=50 width=18) (actual time=0.208..0.208 rows=1 loops=1)"
--"  Recheck Cond: (to_tsvector('english'::regconfig, name) @@ '''1'' & ''franc'''::tsquery)"
--"  Heap Blocks: exact=1"
--"  ->  Bitmap Index Scan on idx_gin_search  (cost=0.00..36.38 rows=50 width=0) (actual time=0.171..0.171 rows=1 loops=1)"
--"        Index Cond: (to_tsvector('english'::regconfig, name) @@ '''1'' & ''franc'''::tsquery)"
--"Planning time: 1.206 ms"
--"Execution time: 0.268 ms"

-- 不适用索引查询(创建索引时，使用两个参数创建，to_tsvector 函数必须与创建索引时一致)
explain analyze select * from test_search where to_tsvector(name) @@ to_tsquery('1_francs');
--"Gather  (cost=1000.00..440818.33 rows=50 width=18) (actual time=0.999..3342.357 rows=1 loops=1)"
--"  Workers Planned: 2"
--"  Workers Launched: 2"
--"  ->  Parallel Seq Scan on test_search  (cost=0.00..439813.33 rows=21 width=18) (actual time=2089.601..3203.254 rows=0 loops=3)"
--"        Filter: (to_tsvector(name) @@ to_tsquery('1_francs'::text))"
--"        Rows Removed by Filter: 666666"
--"Planning time: 0.071 ms"
--"Execution time: 3347.033 ms"

```