# Tinyhttpd 学习

> https://github.com/EZLippi/Tinyhttpd

## 环境搭建

由于该项目只能在 Linux 下运行, 所以我们准备采用 Windows-CLion-WSL 方式进行远程调试, 关于 CLion 配置 WSL 远程调试教程如下,

> https://www.jetbrains.com/help/clion/how-to-use-wsl-development-environment-in-clion.html

这里不再赘述

## 编译

由于该项目只提供了 Makefile, 而 CLion 目前仅支持 CMake, 当然可以通过 Makefile support 插件支持 Makefile, 但由于该插件不支持 WSL,
无法识别到 WSL 的 make 文件, 导致无法生成 Compiledb, 而且生成后也无法调试运行, 当然如果仅仅是想阅读代码的话, 可以在 WSL 中先生成
compile_commands.json 文件, 再清除项目缓存重新加载项目, 也可以完成代码补全, 静态分析, 跳转 和 重构功能来阅读代码. 

CMakeLists.txt 如下:
```
cmake_minimum_required(VERSION 3.4.1)
project(Tinyhttpd)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_VERBOSE_MAKEFILE 1)

ADD_EXECUTABLE(${PROJECT_NAME} httpd.c)

target_link_libraries(${PROJECT_NAME} pthread)
```

```
cmake_minimum_required(VERSION 3.4.1)
project(Tinyhttpd)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_VERBOSE_MAKEFILE 1)

ADD_EXECUTABLE(${PROJECT_NAME} simpleclient.c)
```

完成 CMakeLists.txt 后, 重新加载项目即可编译通过.
