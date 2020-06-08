cmake_minimum_required(VERSION 3.14)
project(${project_name})
SET(CMAKE_CXX_COMPILER      "ccache")
SET(CMAKE_CXX_COMPILER_ARG1 "g++")
add_compile_options(
    -pipe
    -ggdb3
    -std=c++1z
    )
add_definitions(-DFMT_HEADER_ONLY)
aux_source_directory(api API_SRCS)
aux_source_directory(service SERVICE_SRCS)
aux_source_directory(config CONFIG_SRCS)
aux_source_directory(network NETWORK_SRCS)
% for module in modules:
aux_source_directory(${module.module_name} ${module.module_name.upper()}_SRCS)
% endfor
# aux_source_directory(websocket_example WEBSOCKETEXAMPLE_SRCS)
# ${'$'}{WEBSOCKETEXAMPLE_SRCS}
set(SOURCES
    ${'$'}{API_SRCS}
    ${'$'}{SERVICE_SRCS}
    ${'$'}{CONFIG_SRCS}
    ${'$'}{NETWORK_SRCS}
% for module in modules:
    ${'$'}{${module.module_name.upper()}_SRCS}
% endfor
    main/main.cpp)

add_executable(${project_name} ${'$'}{SOURCES})
target_include_directories(${project_name} PUBLIC .)
target_link_libraries(${project_name} pthread)
