cmake_minimum_required(VERSION 3.14)
project(${service_name})
SET(CMAKE_CXX_COMPILER      "ccache")
SET(CMAKE_CXX_COMPILER_ARG1 "g++")
add_compile_options(
    -pipe
    -ggdb3
    -std=c++1z
    )
add_definitions(-DFMT_HEADER_ONLY)
aux_source_directory(config CONFIG_SRCS)
aux_source_directory(../../common/net NET_SRCS)
aux_source_directory(../../common/net/common NET_COMMON_SRCS)
% for module in modules:
aux_source_directory(../../module/${module.name} ${module.name.upper()}_SRCS)
% endfor
# aux_source_directory(websocket_example WEBSOCKETEXAMPLE_SRCS)
# ${'$'}{WEBSOCKETEXAMPLE_SRCS}
set(SOURCES
    ${'$'}{NET_SRCS}
    ${'$'}{CONFIG_SRCS}
    ${'$'}{NET_COMMON_SRCS}
% for module in modules:
    ${'$'}{${module.name.upper()}_SRCS}
% endfor
    main/main.cpp)

add_executable(${service_name} ${'$'}{SOURCES})
target_include_directories(${service_name} PUBLIC .)
target_include_directories(${service_name} PUBLIC ../../common)
target_include_directories(${service_name} PUBLIC ../../module)
target_link_libraries(${service_name} pthread)
