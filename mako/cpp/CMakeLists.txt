cmake_minimum_required(VERSION 3.14)
project(${project_name})
SET(CMAKE_CXX_COMPILER      "ccache")
SET(CMAKE_CXX_COMPILER_ARG1 "g++")
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS
    -ggdb)
aux_source_directory(api API_SRCS)
aux_source_directory(service SERVICE_SRCS)
aux_source_directory(config CONFIG_SRCS)
aux_source_directory(network NETWORK_SRCS)
% for framework in frameworks:
aux_source_directory(${framework.service_name} ${framework.service_name.upper()}_SRCS)
% endfor
# aux_source_directory(websocket_example WEBSOCKETEXAMPLE_SRCS)
# ${'$'}{WEBSOCKETEXAMPLE_SRCS}
set(SOURCES
    ${'$'}{API_SRCS}
    ${'$'}{SERVICE_SRCS}
    ${'$'}{CONFIG_SRCS}
    ${'$'}{NETWORK_SRCS}
% for framework in frameworks:
    ${'$'}{${framework.service_name.upper()}_SRCS}
% endfor
    main/main.cpp)

add_executable(${project_name} ${'$'}{SOURCES})
## target_include_directories(example PUBLIC api)
target_include_directories(${project_name} PUBLIC .)
# target_include_directories(example PUBLIC service)
target_link_libraries(${project_name} pthread)


# add_subdirectory(service)
# add_subdirectory(main)
# add_subdirectory(api)
# target_include_directories(example main service api)
