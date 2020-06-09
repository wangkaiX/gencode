#pragma once

#include <memory>
#include <map>
#include <spdlog/spdlog.h>
#include "${module.name}/types.h"
## % for include in include_list:
## #include "${include}"
## % endfor

#include "config/config.h"
#include "net/tcp_connection.h"

// constexpr size_t buffer_length = 4096;
// constexpr size_t max_buffer_length = 4 * 1024 * 1024;
#define buffer_length 4096
#define max_buffer_length (4 * 1024 * 1024)

class ${module.class_impl_name}: public std::enable_shared_from_this<${module.class_impl_name}>
{
public:
    ${module.class_impl_name}(net::io_context &io_context, std::shared_ptr<TcpConnection> connection_ptr);
    ${module.class_impl_name}(net::io_context &io_context, const net::ip::tcp::endpoint &ep);
    ${module.class_impl_name}(std::shared_ptr<TcpConnection> connection_ptr);
    ${module.class_impl_name}(const net::ip::tcp::endpoint &ep);
    ~${module.class_impl_name}();

    void init();
    // 处理请求
    % for api in module.response_apis:
    % if module.no_resp:
    void ${api.name}(const ${api.req.type.name} &req);
    % else:
    ${api.resp.type.name} ${api.name}(const ${api.req.type.name} &req);
    % endif
    % endfor

    // 发送请求
    % for api in module.request_apis:
        % if module.no_resp:
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
    % if module.no_resp:
    using CallbackType = std::function<void(const nlohmann::json&)>;
    using MemberCallbackType = void (${module.class_impl_name}::*)(const nlohmann::json&);
    % else:
    using CallbackType = std::function<nlohmann::json (const nlohmann::json&)>;
    using MemberCallbackType = nlohmann::json (${module.class_impl_name}::*)(const nlohmann::json&);
    % endif
    std::map<CommandType, CallbackType> _callbacks;
private:

    % if module.no_resp:
    void receive_callback(const nlohmann::json &j);
    % else:
    nlohmann::json receive_callback(const nlohmann::json &j);
    % endif

    // 处理请求
    % for api in module.response_apis:
        % if module.no_resp:
    void ${api.name}_json(const nlohmann::json &j);
        % else:
    nlohmann::json ${api.name}_json(const nlohmann::json &j);
        % endif
    % endfor
public:
    % if module.no_resp:
    using ReceiveCallback = std::function<void(const nlohmann::json &)>;
    % else:
    using ReceiveCallback = std::function<nlohmann::json(const nlohmann::json &)>;
    % endif

    void init_adapt();

    % if module.no_resp:
    void request(const nlohmann::json &j);
    % else:
    nlohmann::json request(const nlohmann::json &j);
    % endif

private:
    int receive_length(std::shared_ptr<std::byte[]> buffer, const TcpConnection::ErrorCode &ec, size_t length);

    void receive_body(std::shared_ptr<std::byte[]> buffer, const TcpConnection::ErrorCode &ec, size_t length);

    void read_some(std::shared_ptr<std::byte[]> buffer, const TcpConnection::ErrorCode &ec, size_t s);
private:
    std::vector<std::byte> write_buffer;
    std::vector<std::byte> read_buffer;
    std::shared_ptr<TcpConnection> _connection_ptr;
    net::io_context _inner_ctx;
    net::io_context &_io_context;
    ReceiveCallback _callback;
    tcp::endpoint _remote_ep;
    size_t _buffer_length{0};

private:
    void default_read_handler(const TcpConnection::ErrorCode &ec, size_t s);
    void default_write_handler(const TcpConnection::ErrorCode &ec, size_t s);

};
