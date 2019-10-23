# docker -volumes
学会使用纯**数据容器**
```
# 启动数据容器, 并创建 somefile 文件后退出
docker run -v /shared-data --name dc busybox touch /shared-data/somefile

# 启动其他容器, 并使用 --volumes-from 链接到 数据容器
docker run -t -i --volumes-from dc busybox /bin/sh

cd /shared-data
```

# kill and stop

linux 中 kill 命令通常是发送 TERM(信号值 15), 其表示应用程序应该终止, 但是, 不要强迫程序终止, 当这个信号被处理时, 
大多数程序将执行清理操作, 但是该程序也可以执行其他操作, 包括忽略该信号. 相反 KILL(信号值 9)会强迫指定的程序终止.
但是在 docker 中, docker kill 命令发送的是 KILL 信号, 这将是的该进程没办法处理终止过程, 意味着一些诸如包含进程 ID 之类的文件可能
会残留在文件系统中, 如果再次启动容器, 可能会造成问题, 而 docker stop 命令发送的是 TERM 信号.
总而言之, 最好使用 dockers stop.

# 