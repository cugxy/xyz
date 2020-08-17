project("data_struct")
set(BUILD_SHARED_LIBS ON)

SET(LIBRARY_OUTPUT_PATH ${PROJECT_INCLUDE}/bin)

file(GLOB_RECURSE files src/*.cpp include/*.h include/*.hpp )

include_directories(include ${PROJECT_SOURCE_DIR}/include)

add_library(${PROJECT_NAME} SHARED ${files})

INSTALL(TARGETS ${PROJECT_NAME} RUNTIME DESTINATION ${PROJECT_INCLUDE}/bin)

add_definitions(-DDATASTRUCT_LIBRARY)