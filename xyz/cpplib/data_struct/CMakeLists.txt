project("data_struct")

file(GLOB_RECURSE files src/*.cpp include/*.h include/*.hpp )

include_directories(include ${PROJECT_SOURCE_DIR}/include)

add_library(${PROJECT_NAME} SHARED ${files})

add_definitions(-D DATASTRUCT_LIBRARY)