1、生成独立的接口文件
2、生成服务端和客户端
3、支持http1.1(beast), tcp(epoll, asio), grpc, udp(epoll, asio)
4、支持多线程
5、生成测试服务及对应的测试案例
6、配置格式为key value, key的完整格式为[key, necessary, description, type] 除key外为可选如"name|||string"
7、在生成目录中直接执行scons即可编译，需要本地有对scons的支持

export PYTHONPATH=$PYTHONPATH:${HOME}/gencode
