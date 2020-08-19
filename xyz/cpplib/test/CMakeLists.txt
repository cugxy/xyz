project("test")

SET(EXECUTABLE_OUTPUT_PATH ${PROJECT_INCLUDE}/bin)

file(GLOB_RECURSE files *.cpp *.h)

include_directories(include ${PROJECT_INCLUDE}/data_struct/include)

link_directories(${PROJECT_INCLUDE}/bin)

add_executable(${PROJECT_NAME} ${files})

target_link_libraries(${PROJECT_NAME} data_struct)
target_link_libraries(${PROJECT_NAME} algorithm)

SET_TARGET_PROPERTIES(${PROJECT_NAME} PROPERTIES LINKER_LANGUAGE CXX)

INSTALL(TARGETS ${PROJECT_NAME} RUNTIME DESTINATION ${PROJECT_INCLUDE}/bin)

add_dependencies(${PROJECT_NAME} data_struct algorithm)