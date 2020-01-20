# 事务与并发控制
数据库的并发控制系统引入了 基于锁的并发控制机制(Lock-Based Concurrency Control) 和 基于多版本的并发控制机制 MVCC(Multi-Version Concurrency Control)

## 事务与并发概念
事务时数据库系统执行过程中最小的逻辑单位. 当事务被提交时, 数据库管理系统药确保一个事务中的所有操作都成功完成, 并且在数据库中永久保存操作结果. 如果一个事务中的一部分操作没有成功完成, 则数据库管理系统会把数据库回滚到操作执行之前的状态.

- 原子性: 一个事务的所有操作, 要么全部执行, 要么全部不执行, 由事务管理器和 MVCC 控制
- 一致性: 执行事务时保存数据库从一个一致的状态变更到另一个一致的状态, 由主键,外键这类约束保证
- 隔离性: 即使每个事务都能确保一致性和原子性, 如果并发执行时, 由于它们的操作以人们不希望的方式交叉运行, 就会导致不一致的情况发生. 确保事务与事务并发执行时, 每个事务都感觉不到有其他事务在并发的执行,  由事务管理器和 MVCC 控制
- 持久性: 一个事务完成后, 即使数据库发生故障, 他对数据库的改变应该永久保存在数据库中, 由预写日志和数据库管理系统的恢复子系统保证

### 并发引起现象
- 脏读: Dirty read 当事务A 读取了事务B 中已经修改但还未提交的数据, 包括 insert, update, delete, 当事务B 不提交并执行 rollback 后, 事务A 所读到的数据时不正确的, 即为 脏读.
- 不可重复读: Non-repeatable read 当事务A 第一次读取数据之后, 被读取的数据被已提交的事务B 进行了修改, 事务A 再次读取这些数据时发现数据已被事务B 修改, 两次查询结果不一致, 即为 不可重复读
- 幻读: Phantom read 指一个事务两次查询的结果集记录数不一致, 如 事务A 根据范围条件查询一些数据, 事务B 却在此时插入或删除了部分数据, 事务A 在接下来的查询中, 会发现有些数据与之前查询结果不一致, 即为 幻读, 幻读可以认为是受 INSERT 和 DELETE 影响的 不可重复读 的一种特殊场景.
- 序列化异常: Serialization anomaly 指成功提交的一组事务的执行结果与这些事务按照串行执行方式的执行结果不一致.

### ANSI SQL 标准的事务隔离级别

为了避免事务之间并发执行的副作用, ANSI SQL 标准定义了四类隔离级别.

- Read Uncommitted: 所有事务都可以看到其他未提交事务的执行结果. 
- Read Committed: 满足一个事务只能看见已经提交事务对关联数据所做的改变的隔离需求.
- Repeatable Read: 确保同一事务的多个实例在并发读取数据时, 会看到同样的数据行.
- Serializable: 每个读取数据上加上共享锁.

## PostgreSQL 事务隔离级别
SQL 标准定义的四种隔离级别只定义了哪种现象不能发送, 描述了每种隔离级别必须提供的最小保护, 但是没有定义哪种现象必须发生. 因此在PostgreSQL 中只实现了三种不同的隔离级别:
- Read Uncommitted 与 Read Committed 一致
- Repeatable Read 不允许出现幻读
- Serializable 不允许序列化异常

### PostgreSQL 事务隔离级别查看设置
- 查看全局事务隔离级别
```
select name, setting from pg_settings where name='default_transaction_isolation';

select current_setting('default_transaction_isolation');
```
- 设置全局事务隔离级别
```
alter system set default_transaction_isolation to 'REPEATABLE READ';

select pg_reload_conf();
```
- 查看当前会话事务隔离级别
```
show transaction_isolation;

select current_setting('transaction_isolation');
```
- 设置当前会话事务隔离级别
```
set session characteristics as transaction isolation level read uncommitted;
```
- 设置当前事务事务隔离级别
```
start transaction isolation level read committed;
...
end;

begin isolation read committed;
...
end;
```

## PostgreSQL 并发控制
数据库管理系统中并发控制的任务便是确保在多个事务同时存取数据库中同一数据时不破坏事务的隔离性, 数据的一致性以及数据库的一致性, 即解决 丢失更新, 脏读, 不可重复读, 幻读, 序列化异常的问题.

并发控制模型:
- 基于锁的并发控制: Lock-Based Concurrency Control
- 基于多版本的并发控制: Multi-Version Concurrency Control

并发控制手段:
- 乐观锁: 乐观并发控制
- 悲观锁: 悲观并发控制

### 基于锁的并发控制
- 排它锁(Exclusive locks X锁): 被加锁的对象只能被持有锁的事务读取和修改, 其他事务无法在该对象上加其他锁, 也不能读取和修改该对象.
- 共享锁(Share locks S锁): 被加锁的对象可以被持锁事务读取, 但不能被修改, 其他事务也可以在上面加共享锁.
- 封锁粒度: 封锁对象大小. 可以是 属性值, 属性值集合, 元组, 关系, 索引项, 整个索引, 整个数据库, 页, 物理记录

### 基于多版本的并发控制
MVCC(基于多版本并发控制)通过保存数据在某个时间点的快照, 并控制元组的可见性来实现并发控制, 快照记录 READ COMMITED 事务隔离级别的事务中的每条 SQL 语句的开头和 SERIAIZABLE 事务隔离级别的事务开始时的元组的可见性. 一个事务无论运行多长时间, 在同一个事务里都能够看到一致的数据. PostgreSQL 为每一个事务分配一个递增的, int32 整形数作为事务 ID, 称为 xid, 创建一个新的快照时, 将收集当前正在执行的事务 id 和已提交的最大事务 id.

PostgreSQL 还在系统里的每一行记录上都存储了事务相关信息, 这被用来判断某一行记录对于当前事务是否可见. PostgreSQL 内部数据结构中, 每个元组(行记录)有 4 个与事务可见性相关的隐藏列, 分别时 xmin, xman, cmin, cmax, 其中 cmin, cmax 分别是插入和删除该元组的命令在事务中的命令序列标识, xmin, xmax 与事务对其他事务的可见性相关, 用于同一个事务中的可见性判断.

- xmin 决定元组对事务的可见性
  - 由回滚的事务或未提交的事务创建的元组, 对于其他任何事务都是不可见的.
  - 无论事务提交或是回滚, xid 都会递增, 对于 Repeatable Read 和 Serializable 隔离级别的事务 A, 如果其 xid 小于事务 B 的 xid, 也就是说事务 A 创建的元组的 xmin 小于事务 B 的xid, 则元组对于事务 B 不可见.

- xmax 决定事务的可见性 ()
  - 如果没有 xmax 值, 则元组对其他事务可见.
  - 如果被设置为 ROLLBACK 或正在运行且未 COMMIT 的事务的 xid, 则元组对其他事务可见.
  - 如果被设置未一个已 COMMIT 的事务的 xid, 则该元组对 xid 大于该事务的事务不可见.

### 使用 pageinspect 观察 MVCC
```
-- 创建扩展
CREATE EXTENSION pageinspect;

-- 创建视图
DROP VIEW IF EXISTS v_pageinspect;
CREATE VIEW v_pageinspect AS 
SELECT '(0, ' || lp || ')' AS ctid,
    CASE lp_flags
        WHEN 0 THEN 'Unused'
        WHEN 1 THEN 'Normal'
        WHEN 2 THEN 'Redirect to ' || lp_off
        WHEN 3 THEN 'Dead'
    END;
FROM heap_page_items(get_raw_page('tb1_mvcc', 0))
ORDER BY lp;

```