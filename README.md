1、生成独立的接口文件
2、生成服务端和客户端
3、生成错误码
4、生成接口文档
5、生成测试服务及对应的测试案例
6、配置格式key value, 只有接口字段的key的完整格式为[key, required, note, type] 除key外为可选如"name|||string"
   key:字段名
   required:是否必传
   note:字段描述
   type:指定的字段类型
   linux参考[example.py]
   windows参考[example_win.py]
7、在生成目录中直接执行scons即可编译，需要本地有对scons的支持
8、对于go可以同时生成支持grpc, graphql, restful, 基于tcp的json, 即一个服务可以同时支持多个类型的接口，以及对应的单元测试文件

[ubuntu]
sudo apt install python3 python3-pip
sudo pip3 install mako markdown -i https://pypi.tuna.tsinghua.edu.cn/simple
在.bashrc中添加
export PYTHONPATH=$PYTHONPATH:${HOME}/gencode

[centos]
sudo yum install python3 python3-pip
sudo pip3 install mako markdown -i https://pypi.tuna.tsinghua.edu.cn/simple
在.bashrc中添加
export PYTHONPATH=$PYTHONPATH:${HOME}/gencode

[windows]
手动安装python3
添加环境变量[PYTHONPATH]为[gencode]的目录
pip3 install mako markdown -i https://pypi.tuna.tsinghua.edu.cn/simple

