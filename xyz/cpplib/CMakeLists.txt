cmake_minimum_required(VERSION 2.08)

project("cpplib")

set(PROJECT_INCLUDE ${PROJECT_SOURCE_DIR})
set(BUILD_SHARED_LIBS ON)

add_subdirectory("data_struct")
add_subdirectory(test)
