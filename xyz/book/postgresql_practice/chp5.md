# 逻辑和物理存储结构

PostgreSQL 中有一个重要的概念 **Database Cluster(数据库集簇)**
- 它是指由单个 PostgreSQL 服务器实例管理的数据库集合, 组成数据库集簇的这些数据库使用相同的全局配置文件和监听端口
, 公用进程和内存结构, 并不是指"一组数据库服务器构成的集群".

## 逻辑存储结构

## 物理存储结构

数据库文件默认保存在 initdb 时创建的目录中, 包含 数据文件, 参数文件, 控制文件, 运行日志, 预写日志等

1. 数据目录结构

```
 10/data
       |--base
       |--pg_tblspc
       |--...
       |--...
       |--...
       |--pg_wal
       |--global
```

| 目录| 用途 |
| -- | -- |
| base | 包含每个数据库对应的目录和子目录 |
| global | 包含集簇范围的表的子目录, 如 pg_database |
| pg_commit_ts | 包含事务提交时间戳数据的子目录 |
| pg_xact | 包含事务提交状态数据的子目录 |
| pg_dynshmem | 包含被动态共享内存子系统所使用文件的子目录 |
| pg_logical | 包含用于逻辑复制的状态数据的子目录 |
| pg_multixact | 包含多事务状态数据的子目录 |
| pg_notify | 包含 LISTEN/NOTIFY 状态数据的子目录 |
| pg_repslot | 包含复制槽数据的子目录 |
| pg_serial | 包含已提交的可序列化事务信息的子目录 |
| pg_snapshots | 包含导出的快照的子目录 |
| pg_stat | 包含用于统计子系统的永久文件的子目录 |
| pg_stat_tmp | 包含用于统计信息子系统临时文件的子目录 |
| pg_subtrans | 包含子事务状态数据的目录 |
| pg_tblspc | 包含指向表空间的符号链接的子目录 |
| pg_twophase | 包含预备事务状态文件的子目录 |
| pg_wal | 保存预写日志 |
| pg_xact | 记录事务提交状态数据 |
| 文件 | 用途 |
| PG_VERSION | PostgreSQK 主版本号文件 |
| pg_hba.conf | 客户端认证控制文件 |
| postgresql.conf | 参数文件 |
| posrgresql.auto.conf | 参数文件, 只保存 ALTER SYSTEM 命令修改的参数  |
| postmaster.opts | 记录服务器最后一次启动时使用的命令行参数 |

2. 数据文件布局
   1. OID
   
      PostgreSQL 中所有的数据库对象都由各自的对象标识符 (OID) 进行内部管理, 他们是无符号的 4 字节整数 (uint4). 数据库对象和各个 OID 之间的关系存储在适当的系统目录中, 可以通过 `SELECT oid, datname FROM pg_database WHERE datname = 'test_db';` 查询.
      - 数据库 OID 存储在 pg_database 系统表中
      - 表, 索引, 序列 OID 存储在 pg_class 系统表中
   2. 表空间

      PostgreSQL 中最大的逻辑存储单位是**表空间**, 数据库中创建的对象都是保存在表空间中.初始化数据库目录时会自动创建 pg_default 和 pg_global 两个表空间, 使用 `\db` 可查看表空间.使用自定义表空间典型场景:
      - 通过创建表空间解决已有表空间磁盘不住无法逻辑扩展问题
      - 将索引, WAL, 数据文件分配在性能不同磁盘上, 使硬件利用率和性能最大化.
      在创建数据库对象时, 会在当前表空间目录创建一个以数据库 OID 命名的目录, 该数据库的所有对象将保存在该目录中, 除非单独指定表空间.
   3. 数据文件命名

      在数据库中创建对象, 如表, 索引时首先会为表和索引分配段. 在 PostgreSQL 中, 每个表和索引都用一个或多个文件存储, 新创建的表文件以对象 OID 命名, 对于大小超出 1GB 的表数据文件, PostgreSQL 会自动将其切分为多个文件来存储, 切分出的文件用 OID.<顺序号> 来命名. 但表文件并不是总是 OID.<顺序号> 命名, 实际上真正管理表文件的是 pg_class 表中的 relfilenode 字段的值, 在新创建对象时会在 pg_class 系统表中插入该表的记录, 默认会以 OID 作为 relfilenode 的值, 但经过几次 VACUUM, TRUNCATE 操作后, relfilenode 的值会发生变化.  
      - 空闲空间映射表文件: 用来映射表文件中可用的空间. _fsm 结尾
      - 可见性映射表文件: 用来跟踪哪些页面只包含已知对所有活动事务可见的元组, 同时也跟踪哪些页面只包含未被冻结的元组, _vm 结尾
   4. 表文件内部结构

      PostgreSQL 中, 将保存在磁盘中的块称为 Page, 而将内存中的块称为 Buffer, 表和索引称为 Relation, 行称为 Tuple, 读写数据是以 Page 为最小单位, 每个 Page 默认大小为 8KB, 在编译时指定的 BLCKSZ 大小决定 Page 的大小. 每个表文件由多个 Page 组成, 每个 Page 包含若干条 Tuple, 对于 IO 性能较好的硬件, 并且以分析为主的数据库, 适当增加 BLCKSZ 大小可以小幅提升数据库性能.

      PageHeader 描述了一个数据页的页头信息, 其结构指针如下:
      - pd_lsn: 确定和记录了最后更改此页的 xlog 记录的 LSN, 把数据页和 WAL 日志关联, 用于恢复数据时校验日志文件和数据文件的一致性,  共 64 位, 高位为 xlogid, 低位为记录偏移量
      - pg_flags: 标识页面的数据存储情况
      - pd_special: 指向索引相关数据的开始位置, 该项在数据文件中为空, 主要是针对不同索引.
      - pd_lower: 指向空闲空间的起始位置
      - pd_upper: 指向空闲空间的结束位置
      - pd_pagesize_version: 不同的 PostgreSQL 版本的页的格式可能会不同
      - pg_linp: 行指针数据

      当从数据库中检索数据时, 有两种典型的访问方法: 顺序扫描和 B 树索引扫描
      - 顺序扫描: 通过扫描每个页面中的所有行指针顺序读取所有页面中的所有 Tuple
      - B 树索引扫描: 索引文件包含 索引 Tuple , 每个 Tuple 由索引键和指向目标堆元组的 TID 组成, 如果找到了正在查找的键的 索引 Tuple, PostgreSQL 使用获取的 TID 值读取所需的堆元组.
  
      每个 Tuple 包含两部分内容: HeapTupleHeader, HeapTuple
      - HeapTupleHeader: 用来保存 Tuple 元信息, OID, xmin, cmin, 
      - HeapTuple: 保存数据



# 进程结构

- postmaster: 守护进程 启停数据库, 监听客户端连接, 为每个客户端连接 fork 单独的 posrgres 进程, 修复出错的服务进程, 管理数据文件, 管理与数据库运行相关的辅助进程
- postgres: 服务进程
  
辅助进程
- bgwriter: background writer, 搜索共享缓冲池找到被修改的页, 并刷出共享缓冲池. 
- autovacuum launcher: 自动清理回收垃圾进程
- archiver: WAL 归档进程
- checkpointer: 检查点进程
- walwriter: 定期将 WAL 缓冲区上的 WAL 数据写入磁盘
- logger collector: 日志进程, 将消息或错误写入日志

# 内存结构

## 本地内存
本地内存由每个后端服务进程分配使用, 由三部分组成:
- work_mem: 当使用 ORDER BY 或 DISTINCT 操作对元组进行排序操作时使用这部分内存
- maintenance_work_mem: 维护操作, 如 VACUUM, REINDEX, CREATE INDEX 使用这部分内存
- temp_buffers: 临时表相关操作使用这部分内存
## 共享内存
共享内存在 PostgreSQL 服务器启动时分配, 由所有后端进程共同使用.
- shared pool: PostgreSQL 将表和索引中的页面从持久存储装载到该内存, 并直接操作它们.
- WAL buffer: WAL 文件持久化之前的缓冲区
- commitLog buffer: PostgreSQL 在 commit log 中保存事务的状态, 并将这些状态保留在该共享内存中, 在整个事务处理过程中使用.