#pragma once

#include <memory>
#include <map>
#include <spdlog/spdlog.h>
#include "${framework.service_name}/types.h"
% for include in include_list:
#include "${include}"
% endfor

#include "config/config.h"

constexpr size_t buffer_length = 4096;
constexpr size_t max_buffer_length = 4 * 1024 * 1024;

class ${framework.service_api_class_name}: public std::enable_shared_from_this<${framework.service_api_class_name}>
{
public:
    ${framework.service_api_class_name}(boost::asio::io_context &io_context, std::shared_ptr<${connection_class_name}> connection_ptr);
    ~${framework.service_api_class_name}();

    void init();
    // 处理请求
    % for api in framework.server_apis:
    % if framework.no_resp:
    void ${api.name}(const ${api.req.type.name} &req);
    % else:
    ${api.resp.type.name} ${api.name}(const ${api.req.type.name} &req);
    % endif
    % endfor

    // 发送请求
    % for api in framework.client_apis:
        % if framework.no_resp:
    void ${api.name}(const ${api.req.type.name} &req);
        % else:
    ${api.resp.type.name} ${api.name}(const ${api.req.type.name} &req);
        % endif
    % endfor

private:

    % if isinstance(api.command_code, int):
    using CommandType = int;
    % elif isinstance(api.command_code, str):
    using CommandType = std::string;
    % else:
        <%  
        print("不支持的类型" % type(api.command_code))
        assert False
        %>  
    % endif
    % if framework.no_resp:
    using CallbackType = std::function<void(std::shared_ptr<char[]>)>;
    % else:
    using CallbackType = std::function<std::shared_ptr<char[]> (std::shared_ptr<char[]>)>;
    % endif
    std::map<CommandType, CallbackType> _callbacks;
private:

    % if framework.no_resp:
    void receive_callback(std::shared_ptr<char[]>);
    % else:
    std::shared_ptr<char[]> receive_callback(std::shared_ptr<char[]> data_ptr);
    % endif

    // 处理请求
    % for api in framework.server_apis:
        % if framework.no_resp:
    void ${api.name}_binary(std::shared_ptr<char[]> data_ptr);
        % else:
    std::shared_ptr<char[]> ${api.name}_binary(std::shared_ptr<char[]> data_ptr);
        % endif
    % endfor
public:
    % if framework.no_resp:
    using ReceiveCallback = std::function<void(std::shared_ptr<char[]>)>;
    % else:
    using ReceiveCallback = std::function<std::shared_ptr<char[]> (std::shared_ptr<char[]>)>;
    % endif

    void init_adapt();

    % if framework.no_resp:
    void request(std::shared_ptr<char[]> data_ptr);
    % else:
    std::shared_ptr<char[]> request(std::shared_ptr<char[]> data_ptr);
    % endif

private:
    int receive_header(std::shared_ptr<char[]> buffer, const TcpConnection::ErrorCode &ec, size_t length);

    void receive_body(std::shared_ptr<char[]> buffer, const TcpConnection::ErrorCode &ec, size_t length);

    void read_some(std::shared_ptr<char[]> buffer, const TcpConnection::ErrorCode &ec, size_t s);
private:
    std::vector<char> write_buffer;
    std::vector<char> read_buffer;
    std::shared_ptr<TcpConnection> _connection_ptr;
    boost::asio::io_context &_io_context;
    ReceiveCallback _callback;
    boost::asio::ip::tcp::endpoint _remote_ep;
    size_t _buffer_length{0};

private:
    void default_read_handler(const TcpConnection::ErrorCode &ec, size_t s);
    void default_write_handler(const TcpConnection::ErrorCode &ec, size_t s);

};
