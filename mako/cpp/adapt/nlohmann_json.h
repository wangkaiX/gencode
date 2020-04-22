#include <functional>
#include <map>
#include <boost/beast.hpp>
#include <nlohmann/json.hpp>
#include <iostream>
#include <memory>
#include <spdlog/spdlog.h>

#include "network/tcp_connection.h"
#include "common/types.h"
#include "common/common_api.h"

% for include in include_list:
#include "${include}"
% endfor

constexpr size_t buffer_length = 4096;
// thread_local std::vector<char> write_buffer(buffer_length);
thread_local std::vector<char> write_buffer;
thread_local std::vector<char> read_buffer;


template <typename Connection>
class ${adapt_class_name}
{
    void write_cb(std::shared_ptr<Connection> connection_ptr, size_t size, const Connection::ErrorCode &ec)
    {
        if (ec) {
            SPDLOG_ERROR("已发送[{}]字节, 失败原因[{}]", size, ec.message());
            SPDLOG_ERROR("断开与[{}]的连接", connection_ptr->remote_endpoint());
            return;
        }
    }
    
    void read_cb(std::shared_ptr<Connection> connection_ptr, size_t size, const Connection::ErrorCode &ec)
    {
        if (ec) {
            SPDLOG_ERROR("已收到[{}]字节, 失败原因[{}]", size, ec.message());
            SPDLOG_ERROR("断开与[{}]的连接", connection_ptr->remote_endpoint());
            return;
        }
    }

public:
    ${adapt_class_name}()
    {
        init();
    }
    std::string request(const char *data, size_t length)
    {
        try {
            std::string msg(data, length);
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
        _write_cb = std::bind(&${adapt_class_name}::write_cb, this, _connection_ptr, std::placeholders::_1, std::placeholders::_2);
        _read_cb = std::bind(&${adapt_class_name}::read_cb, this, _connection_ptr, std::placeholders::_1, std::placeholders::_2);

        % for api in framework.server_apis:
        _callbacks[${api.command_code}] = std::bind(&${adapt_class_name}::${api.name}, this, std::placeholders::_1);
        % endfor
    }

    // 发送请求
    % for api in framework.client_apis:
    % if api.no_resp:
    void ${api.name}(const ${api.req.type.name} &req)
    % else:
    ${api.resp.type.name} ${api.name}(const ${api.req.type.name} &req)
    % endif
    {
        nlohmann::json j = req;
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
        _connection_ptr->read(read_buffer.data(), getCfg().${framework.service_name}.length_length);
        len = stoi(std::string(read_buffer.data(), getCfg().${framework.service_name}.length_length));
        _connection_ptr->read(read_buffer.data(), len);
        j = nlohmann::json::parse(std::string(read_buffer.data(), len));
        return j;
            % endif
        % else:
            print("未完善的逻辑")
            assert False
        % endif
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
    std::shared_ptr<${framework.service_class_name}> _server_api_ptr;
    std::shared_ptr<Connection> _connection_ptr;
    Connection::WriteCallback _write_cb;
    Connection::ReadCallback _read_cb;

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
