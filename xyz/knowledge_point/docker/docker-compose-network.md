# Networking in Compose

> By default Compose sets up a single network for your app. Each container for a service joins the default network and 
> is both reachable by other containers on that network, and discoverable by them at a hostname identical to the container name.

## 默认使用
Docker-Compose 会给你的 docker-compose.yml app 生成一个默认的网络, app 中每个容器默认都加入这个网络, 容器之间彼此互通. 并且可以使用容器的名字识别.
网络名称默认情况下为 project name_default( project name 即 docker-compose.yml所在的文件夹名称, 
你可以使用 --project-name 或 COMPOSE_PROJECT_NAME 环境变量修改),如 server_default.

栗子:

`docker-compose.yml` 文件:
```
version: "3"
services:
  web:
    build: .
    ports:
      - "8000:8000"
  db:
    image: postgres
    ports:
      - "8001:5432"
```
假设上述文件放置在 `xy_app` 目录, 那么, 当使用 `docker-compose up -d` 命令启动之后
- 一个叫 `xy_app_default` 的网络被创建;
- 一个使用 `web` 配置的容器会被创建, 它以 `web` 的名字加入了 `xy_app_default` 网络;
- 一个使用 `db` 配置的容器会被创建, 它以 `db` 的名字加入了 `xy_app_default` 网络;

每个容器都可以查找主机名 `web` 或 `db`, 并获取相应的容器的 IP 地址, 如 `web` 应用的代码可以使用 URL `postgres://db:5432` 连接数据库并使用它.

需要注意的是 `HOST_PORT` 和 `CONTAINER_PORT` 之间的区别. 前者是指宿主机的端口, 后者是指容器端口. 容器网络中的服务间使用的是 `CONTAINER_PORT` 通信.
`HOST_PORT` 定义了是为了容器网络外被调用的。所以，前面才使用的是 `postgres://db:5432` 而不是 `postgres://db:8001`。因为他们属于同一个容器网络中。

## 指定网络

services 下级的服务中 networks 指定的网络不是指要创建的网络，而是这个服务要加入的网络。

所以说，这时候如果你指定了一个没有的网络，就会报错啦，类似这种：

栗子:
```
version: "2"
services:
    mongodb:
        image: mongo:4
        container_name: devops-mongo # 容器名
        ports:
            - "27017:27017"
        volumes:
            - "/data/docker_local/mongo/configdb:/data/configdb"
            - "/data/docker_local/mongo/data/db:/data/db"
        command: --auth # 开启授权验证
        networks:
            - mongo_net
```

如果 `mongo_net` 网络不存在, 则会报错
```
ERROR: Service "mongodb" uses an undefined network "mogo_net"
```

## 创建网络
 
使用 top-level 的 networks 定义一下网络，运行时，会自动创建网络

栗子:
```
version: "2"
services:
    mongodb:
        image: mongo:4
        container_name: devops-mongo # 容器名
        ports:
            - "27017:27017"
        volumes:
            - "/data/docker_local/mongo/configdb:/data/configdb"
            - "/data/docker_local/mongo/data/db:/data/db"
        command: --auth # 开启授权验证
        networks:
            - mongo_net
networks:
  mongo_net:
```

但是它自动创建的网络好像也不叫 mong_net 而是根据规则，创建的 db_mongo_net 的网络。虽然不报错，但是我觉得有点别扭，查看了一下，可以利用 name 的标签定义一下网络。

```
version: "2.1"
services:
    mongodb:
        image: mongo:4
        container_name: devops-mongo # 容器名
        ports:
            - "27017:27017"
        volumes:
            - "/data/docker_local/mongo/configdb:/data/configdb"
            - "/data/docker_local/mongo/data/db:/data/db"
        command: --auth # 开启授权验证
        networks:
            - mongo_net
networks:
  mongo_net:
    name: mongo_net
```

## 重命名网络

如果我 name 指定想要的值，上一层，有必要一致吗?

栗子:
```
version: "2.1"
services:
    mongodb:
        image: mongo:4
        container_name: devops-mongo # 容器名
        ports:
            - "27017:27017"
        volumes:
            - "/data/docker_local/mongo/configdb:/data/configdb"
            - "/data/docker_local/mongo/data/db:/data/db"
        command: --auth # 开启授权验证
        networks:
            - mongo_net
networks:
  default:
    name: mongo_net
```

上面的这种改法会报错：ERROR: Service "mongodb" uses an undefined network "mongo_net"。所以，顶层的 networks 下一层及的网络名称，
要和服务中要加入的名称保持一致才行。这样一试，貌似对上面创建的 db_mongo_net 的网络而不报错的现象理解了。
省略了 name, 那么 name 就按照默认规则创建网络了，其实就是类似于：

```
version: "2.1"
services:
    mongodb:
        image: mongo:4
        container_name: devops-mongo # 容器名
        ports:
            - "27017:27017"
        volumes:
            - "/data/docker_local/mongo/configdb:/data/configdb"
            - "/data/docker_local/mongo/data/db:/data/db"
        command: --auth # 开启授权验证
        networks:
            - mongo_net
networks:
  mongo_net:
    name: db_mongo_net
```

## 网络操作
通过 docker network ls/rm/create .. 等命令，可以查看或操作容器的网络。

### links
通过链接，您可以给某个 service 定义别名，通过该别名可以从其他服务访问服务。默认情况下，任何服务都可以通过该服务的名称访问任何其他服务。

栗子: 

db 是一个服务名，在 web 服务中，给 db 定义了一个别名 database。那么，在 web 服务中，既可以通过 db 又可以通过 databse 查找到主机名了。

```
version: "3"
services:

  web:
    build: .
    links:
      - "db:database"
  db:
    image: postgres
```

### Specify custom networks
为了不使用默认的网络，你可以使用 compsose 文件的 top-level 关键字 networks 自定义网络。
这让你可以创建更复杂的拓扑并指定自定义网络驱动程序和选项。 你还可以使用它将服务连接到不由 Compose 管理的外部创建的网络。

栗子:
```
version: "3"
services:

  proxy:
    build: ./proxy
    networks:
      - frontend
  app:
    build: ./app
    networks:
      - frontend
      - backend
  db:
    image: postgres
    networks:
      - backend

networks:
  frontend:
    # Use a custom driver
    driver: custom-driver-1
  backend:
    # Use a custom driver which takes special options
    driver: custom-driver-2
    driver_opts:
      foo: "1"
      bar: "2"
```

### external
external: true 加上这行表示我这个服务用的网络是用外部的网络，不用自动创建。否则，会按照规则默认创建网络的，例如 db_default、sonarqube_default 这些网络就是默认创建的。如果这个时候没有对应的外部网络，会弹出如下的提示：
```
Creating network "db_default" with the default driver
ERROR: Network mysql_net declared as external, but could not be found. Please create the network manually using `docker network create mysql_net` and try again.
```