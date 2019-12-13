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

