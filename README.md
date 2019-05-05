1、生成独立的接口文件
2、生成服务端和客户端
3、支持http1.1(beast), tcp(epoll, asio), grpc, udp(epoll, asio)
4、支持多线程
5、生成测试服务及对应的测试案例
6、配置格式为key value, key的完整格式为[key, necessary, comment, type] 除key外为可选如"name|||string"
   如:
   {
     "interfacename1|注释":{
         "请求":{
            // "arg1|是否必传|注释|指定类型":{
             "arg1|Y|这是一个请求参数|TypeA":"value1",
             "arg2":{
                 "a22","value2",
                 "a23","value3"
             }
         }
         "应答":123
     },
     "interacename2":{     
         "a1":"b",
         "r1":"b1"
     },
     "enumType|||ENUM":
          ["ENUM1", "ENUM2","枚举值:注释","enum4"]
    }
7、在生成目录中直接执行scons即可编译，需要本地有对scons的支持
8、对于go可以同时生成支持grpc, graphql, restful, 基于tcp的json, 即一个服务可以同时支持多个类型的接口，以及对应的单元测试文件


sudo apt install python3
pip3 install mako -i https://pypi.tuna.tsinghua.edu.cn/simple
export PYTHONPATH=$PYTHONPATH:${HOME}/gencode

