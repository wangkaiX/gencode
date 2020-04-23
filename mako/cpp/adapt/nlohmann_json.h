#include <functional>
#include <map>
#include <boost/beast.hpp>
#include <nlohmann/json.hpp>
#include <iostream>
#include <memory>
#include <spdlog/spdlog.h>

#include "${framework.service_name}/types.h"
#include "${framework.service_name}/api.h"
#include "config/config.h"

% for include in include_list:
#include "${include}"
% endfor

constexpr size_t buffer_length = 4096;
constexpr size_t max_buffer_length = 4 * 1024 * 1024;
// thread_local std::vector<char> write_buffer(buffer_length);
thread_local std::vector<char> write_buffer;
thread_local std::vector<char> read_buffer;


template <typename Connection>
class ${framework.adapt_class_name}
{
    void write_cb(std::shared_ptr<Connection> connection_ptr, size_t size, const typename Connection::ErrorCode &ec)
    {
        if (ec) {
            SPDLOG_ERROR("已发送[{}]字节, 失败原因[{}]", size, ec.message());
            SPDLOG_ERROR("断开与[{}]的连接", connection_ptr->remote_endpoint());
            return;
        }
    }
    
    void read_cb(std::shared_ptr<Connection> connection_ptr, size_t size, const typename Connection::ErrorCode &ec)
    {
        if (ec) {
            SPDLOG_ERROR("已收到[{}]字节, 失败原因[{}]", size, ec.message());
            SPDLOG_ERROR("断开与[{}]的连接", connection_ptr->remote_endpoint());
            return;
        }
    }

public:
    ${framework.adapt_class_name}(boost::asio::io_context &io_context, const boost::asio::ip::tcp::endpoint &ep)
        % if framework.is_server:
        : _server_ptr(std::make_shared<Server>(io_context, ep))
        % else:
        : _connection_ptr(std::make_shared<Connection>(io_context, ep))
        % endif
    {
        init();
    }
    int receive_length(std::shared_ptr<char[]> buffer, size_t length, const typename Connection::ErrorCode &ec)
    {
        if (ec) {
            SPDLOG_ERROR("receive length error[{}]", ec.message());
            return -1;
        }
        auto len = stoi(std::string(buffer.get(), getCfg().${framework.service_name}.length_length));
        size_t new_buffer_length = _buffer_length;
        // TODO 接收完body后是否需要缩小空间, 是否需要设置一个接收上限，防止过大长度
        if (len > max_buffer_length) {
            SPDLOG_ERROR("长度过大[{}]", len);
            // TODO 丢弃并返回失败原因
            // _connection_ptr->async_write(write_buffer.get(), write_buffer.size(), this->_write_cb)
            _connection_ptr->async_read(buffer.get(), getCfg().${framework.service_name}.length_length,
                    std::bind(&${framework.adapt_class_name}::receive_length, this, buffer, std::placeholders::_1, std::placeholders::_2));
            return -1;
        }
        while (len >= new_buffer_length) {
            new_buffer_length += buffer_length;
        }
        if (new_buffer_length != _buffer_length) {
            buffer.reset(new char[new_buffer_length]);
            _buffer_length = new_buffer_length;
        }
        _connection_ptr->async_read(buffer.get(), getCfg().${framework.service_name}.length_length,
                std::bind(&${framework.adapt_class_name}::receive_body, this, buffer, std::placeholders::_1, std::placeholders::_2));
    }
    std::string receive_body(std::shared_ptr<char[]> buffer, size_t length, const typename Connection::ErrorCode &ec)
    {
        if (ec) {
            SPDLOG_ERROR("receive body error[{}]", ec.message());
            return "";
        }
        _connection_ptr->async_read(buffer.get(), getCfg().${framework.service_name}.length_length,
                std::bind(&${framework.adapt_class_name}::receive_length, this, buffer, std::placeholders::_1, std::placeholders::_2));
        try {
            std::string msg(buffer.get(), length);
            auto json = nlohmann::json::parse(msg);
            int command = json["${framework.command_name}"];
            return _callbacks[command](json).dump();
        }
        catch (std::exception &e) {
            nlohmann::json j;
            j["code"] = -1; 
            j["msg"] = "解析接口类型失败";
            SPDLOG_ERROR("解析接口类型失败[{}]", j.dump(4));
            return j.dump();
        }
    }
private:
    void init()
    {
        _write_cb = std::bind(&${framework.adapt_class_name}::write_cb, this, _connection_ptr, std::placeholders::_1, std::placeholders::_2);
        _read_cb = std::bind(&${framework.adapt_class_name}::read_cb, this, _connection_ptr, std::placeholders::_1, std::placeholders::_2);

        % for api in framework.server_apis:
        _callbacks[${api.command_code}] = std::bind(&${framework.adapt_class_name}::${api.name}, this, std::placeholders::_1);
        % endfor
        % if len(framework.server_apis) > 0:
        std::shared_ptr<char[]> buffer(new char[buffer_length]);
        _buffer_length = buffer_length;
        _connection_ptr->async_read(buffer.get(), getCfg().${framework.service_name}.length_length,
                std::bind(&${framework.adapt_class_name}::receive_length, this, buffer, std::placeholders::_1, std::placeholders::_2));
        % endif 
    }

    % if framework.no_resp:
    void request(const nlohmann::json &j)
    % else:
    nlohmann::json request(const nlohmann::json &j)
    % endif
    {
        auto msg = j.dump();
        % if framework.length_length:
        auto len = getCfg().${framework.service_name}.length_length + msg.size();
        if (len > write_buffer.size()) {
            write_buffer.resize(len);
        }
        snprintf(write_buffer.data(), getCfg().${framework.service_name}.length_length+1, "%d", len);
        memcpy(write_buffer.data() + getCfg().${framework.service_name}.length_length, msg.c_str(), msg.size());
            % if framework.no_resp:
        _connection_ptr->async_write(write_buffer.data(), write_buffer.size(), this->_write_cb)
            % else:
        _connection_ptr->write(write_buffer.data(), write_buffer.size());
        // 接收长度
        if (getCfg().${framework.service_name}.length_length > read_buffer.size()) {
            read_buffer.resize(getCfg().${framework.service_name}.length_length);
        }
        _connection_ptr->read(read_buffer.data(), getCfg().${framework.service_name}.length_length);
        len = stoi(std::string(read_buffer.data(), getCfg().${framework.service_name}.length_length));

        if (len > read_buffer.size()) {
            read_buffer.resize(len);
        }
        _connection_ptr->read(read_buffer.data(), len);
        return nlohmann::json::parse(std::string(read_buffer.data(), len));
            % endif
        % else:
            print("未完善的逻辑")
            assert False
        % endif
    }
    // 发送请求
    % for api in framework.client_apis:
    % if api.no_resp:
    void ${api.name}(const ${api.req.type.name} &req)
    % else:
    ${api.resp.type.name} ${api.name}(const ${api.req.type.name} &req)
    % endif
    {
        return request(req);
    }

    % endfor

    // 处理请求
    % for api in framework.server_apis:
    % if framework.no_resp:
    void ${api.name}(const nlohmann::json &json)
    % else:
    nlohmann::json ${api.name}(const nlohmann::json &json)
    % endif
    {
        try {
            return _server_ptr->${api.name}(json);
        }
        catch (std::exception &e) {
            % if framework.no_resp:
            SPDLOG_ERROR("[{}]", e.what());
            % else:
            ${api.resp.type.name} resp{};
            resp.code = -1;
            resp.msg = e.what();
            SPDLOG_ERROR("[{}]", e.what());
            return resp;
            % endif
        }
    }

    % endfor
private:
    std::shared_ptr<${framework.service_class_name}Api> _server_api_ptr;
    % if framework.is_server:
    std::shared_ptr<Connection> _server_ptr;
    % else:
    std::shared_ptr<Connection> _connection_ptr;
    % endif
    typename Connection::WriteCallback _write_cb;
    typename Connection::ReadCallback _read_cb;
    boost::asio::ip::tcp::endpoint _remote_ep;
    size_t _buffer_length{0};

    % if isinstance(api.command_code, int):
    std::map<int, std::function<nlohmann::json (nlohmann::json)>> _callbacks;
    % elif isinstance(api.command_code, str):
    std::map<std::string, std::function<nlohmann::json (nlohmann::json)>> _callbacks;
    % else:
        <%
        print("不支持的类型" % type(api.command_code))
        assert False
        %>
    % endif
};
