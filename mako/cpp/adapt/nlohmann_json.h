#pragma once
#include <functional>
#include <map>
#include <boost/beast.hpp>
#include <nlohmann/json.hpp>
#include <iostream>
#include <memory>
#include <spdlog/spdlog.h>

// #include "${framework.service_name}/types.h"
#include "config/config.h"

% for include in include_list:
#include "${include}"
% endfor

constexpr size_t buffer_length = 4096;
constexpr size_t max_buffer_length = 4 * 1024 * 1024;
// thread_local std::vector<char> write_buffer(buffer_length);


template <typename Connection>
class ${framework.adapt_class_name} : public std::enable_shared_from_this<${framework.adapt_class_name}<Connection>>
{
    // void write_cb(std::shared_ptr<Connection> connection_ptr, size_t size, const typename Connection::ErrorCode &ec)
    // {
    //     if (ec) {
    //         SPDLOG_ERROR("已发送[{}]字节, 失败原因[{}]", size, ec.message());
    //         SPDLOG_ERROR("断开与[{}]的连接", connection_ptr->remote_endpoint());
    //         return;
    //     }
    // }
    // 
    // void read_cb(std::shared_ptr<Connection> connection_ptr, size_t size, const typename Connection::ErrorCode &ec)
    // {
    //     if (ec) {
    //         SPDLOG_ERROR("已收到[{}]字节, 失败原因[{}]", size, ec.message());
    //         SPDLOG_ERROR("断开与[{}]的连接", connection_ptr->remote_endpoint());
    //         return;
    //     }
    // }

public:
    % if framework.no_resp:
    using ReceiveCallback = std::function<void(const nlohmann::json &)>;
    % else:
    using ReceiveCallback = std::function<nlohmann::json(const nlohmann::json &)>;
    % endif

## % if framework.is_server:
## ${framework.adapt_class_name}(boost::asio::io_context &io_context, std::shared_ptr<Connection> connection_ptr)
##: _connection_ptr(connection_ptr)
##        % else:
##    ${framework.adapt_class_name}(boost::asio::io_context &io_context, const boost::asio::ip::tcp::endpoint &ep)
##        : _connection_ptr(std::make_shared<Connection>(io_context, ep))
##        % endif
    ${framework.adapt_class_name}(boost::asio::io_context &io_context, std::shared_ptr<Connection> connection_ptr)
        : _io_context(io_context)
        , _connection_ptr(connection_ptr)
    {
        init();
    }

    void set_callback(ReceiveCallback cb)
    {
        _callback = cb;
    }

    int receive_length(std::shared_ptr<char[]> buffer, const typename Connection::ErrorCode &ec, size_t length)
    {
        if (ec) {
            SPDLOG_ERROR("receive length error[{}]", ec.message());
            return -1;
        }
        int len = stoi(std::string(buffer.get(), getCfg().${framework.service_name}.length_length));
        size_t new_buffer_length = _buffer_length;
        // TODO 接收完body后是否需要缩小空间, 是否需要设置一个接收上限，防止过大长度
        if (len > max_buffer_length) {
            SPDLOG_ERROR("长度过大[{}]", len);
            // TODO 丢弃并返回失败原因
            // _connection_ptr->async_write(write_buffer.get(), write_buffer.size(), this->_write_cb)
            _connection_ptr->async_read(buffer.get(), getCfg().${framework.service_name}.length_length,
                    std::bind(&${framework.adapt_class_name}::receive_length, this->shared_from_this(), buffer, std::placeholders::_1, std::placeholders::_2));
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
                std::bind(&${framework.adapt_class_name}::receive_body, this->shared_from_this(), buffer, std::placeholders::_1, std::placeholders::_2));
    }

    void receive_body(std::shared_ptr<char[]> buffer, const typename Connection::ErrorCode &ec, size_t length)
    {
        if (ec) {
            SPDLOG_ERROR("receive body error[{}]", ec.message());
            return;
        }
        _connection_ptr->async_read(buffer.get(), getCfg().${framework.service_name}.length_length,
                std::bind(&${framework.adapt_class_name}::receive_length, this->shared_from_this(), buffer, std::placeholders::_1, std::placeholders::_2));
        std::string msg(buffer.get(), length);
        try {
            auto json = nlohmann::json::parse(msg);
            // int command = json["${framework.command_name}"];
            % if framework.no_resp:
            return _callback(json);
            % else:
            msg = _callback(json).dump();
            % endif
        }
        catch (std::exception &e) {
            nlohmann::json j;
            j["code"] = -1; 
            j["msg"] = "解析接口类型失败";
            msg = j.dump();
            SPDLOG_ERROR("解析接口类型失败[{}]", j.dump(4));
        }
        % if not framework.no_resp:
        _connection_ptr->async_write(msg.c_str(), msg.size(),
            [](const typename Connection::ErrorCode &ec, size_t)
            {
                if (ec) {
                    SPDLOG_ERROR("write error[{}]", ec.message());
                    return;
                }
            }
        );
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
        int len = getCfg().${framework.service_name}.length_length + msg.size();
        if (len > write_buffer.size()) {
            write_buffer.resize(len);
        }
        snprintf(write_buffer.data(), getCfg().${framework.service_name}.length_length+1, "%d", len);
        memcpy(write_buffer.data() + getCfg().${framework.service_name}.length_length, msg.c_str(), msg.size());
            % if framework.no_resp:
        _connection_ptr->async_write(write_buffer.data(), write_buffer.size(),
                [](const typename Connection::ErrorCode &ec, size_t)
                {
                    if (ec) {
                        SPDLOG_ERROR("write error[{}]", ec.message());
                        return;
                    }
                });
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
private:
    void init()
    {
        // _write_cb = std::bind(&${framework.adapt_class_name}::write_cb, this, _connection_ptr, std::placeholders::_1, std::placeholders::_2);
        // _read_cb = std::bind(&${framework.adapt_class_name}::read_cb, this, _connection_ptr, std::placeholders::_1, std::placeholders::_2);

        std::shared_ptr<char[]> buffer(new char[buffer_length]);
        _buffer_length = buffer_length;

        % if len(framework.server_apis) > 0:
        _connection_ptr->async_read(buffer.get(), getCfg().${framework.service_name}.length_length,
                std::bind(&${framework.adapt_class_name}::receive_length, this->shared_from_this(), buffer, std::placeholders::_1, std::placeholders::_2));
        % else:
        // 防止释放
        _connection_ptr->async_read_some(buffer.get(), _buffer_length,
                std::bind(&${framework.adapt_class_name}::read_some, this->shared_from_this(), buffer, std::placeholders::_1, std::placeholders::_2));
        % endif 
    }

    void read_some(std::shared_ptr<char[]> buffer, const typename Connection::ErrorCode &ec, size_t s)
    {
        SPDLOG_DEBUG("receive[{}]", std::string(buffer.get(), s));
        _connection_ptr->async_read_some(buffer.get(), _buffer_length,
                std::bind(&${framework.adapt_class_name}::read_some, this->shared_from_this(), buffer, std::placeholders::_1, std::placeholders::_2));
    }
private:
    std::vector<char> write_buffer;
    std::vector<char> read_buffer;
    std::shared_ptr<Connection> _connection_ptr;
    boost::asio::io_context &_io_context;
    ReceiveCallback _callback;
    // typename Connection::WriteCallback _write_cb;
    // typename Connection::ReadCallback _read_cb;
    boost::asio::ip::tcp::endpoint _remote_ep;
    size_t _buffer_length{0};
};
