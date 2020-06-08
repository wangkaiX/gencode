#include "${module.module_name}/api.h"
#include <cassert>

${module.module_class_impl_name}::${module.module_class_impl_name}(boost::asio::io_context &io_context, std::shared_ptr<TcpConnection> connection_ptr)
    : _io_context(io_context)
    , _connection_ptr(connection_ptr)
{
}

${module.module_class_impl_name}::${module.module_class_impl_name}(boost::asio::io_context &io_context, const boost::asio::ip::tcp::endpoint &ep)
    : _io_context(io_context)
    , _connection_ptr(std::make_shared<TcpConnection>(io_context, ep))
{
}

${module.module_class_impl_name}::~${module.module_class_impl_name}()
{   
    SPDLOG_INFO("destroy ${module.module_class_impl_name}");
}

void ${module.module_class_impl_name}::init_adapt()
{   
    // _write_cb = std::bind(&${module.module_class_impl_name}::write_cb, this, _connection_ptr, std::placeholders::_1, std::placeholders::_2);
    // _read_cb = std::bind(&${module.module_class_impl_name}::read_cb, this, _connection_ptr, std::placeholders::_1, std::placeholders::_2);

    std::shared_ptr<char[]> buffer(new char[buffer_length]);
    _buffer_length = buffer_length;

    % if len(module.request_apis) > 0:
    _connection_ptr->async_read(buffer.get(), getCfg().${module.module_name}.length_length,
            std::bind(&${module.module_class_impl_name}::receive_length, this->shared_from_this(), buffer, std::placeholders::_1, std::placeholders::_2));
    % else:
    // 防止释放
    _connection_ptr->async_read_some(buffer.get(), _buffer_length,
            std::bind(&${module.module_class_impl_name}::read_some, this->shared_from_this(), buffer, std::placeholders::_1, std::placeholders::_2));
    % endif
}

% if module.no_resp:
void ${module.module_class_impl_name}::request(const nlohmann::json &j)
% else:
nlohmann::json ${module.module_class_impl_name}::request(const nlohmann::json &j)
% endif
{   
    auto msg = j.dump();
    int len = getCfg().${module.module_name}.length_length + msg.size();
    if (len > write_buffer.size()) {
        write_buffer.resize(len);
    }
    snprintf(write_buffer.data(), getCfg().${module.module_name}.length_length+1, "%d", len);
    memcpy(write_buffer.data() + getCfg().${module.module_name}.length_length, msg.c_str(), msg.size());
    % if module.no_resp:
    _connection_ptr->async_write(write_buffer.data(), write_buffer.size(),
            std::bind(&${module.module_class_impl_name}::default_write_handler, this->shared_from_this(), std::placeholders::_1, std::placeholders::_2));
    % else:
    _connection_ptr->write(write_buffer.data(), write_buffer.size());
    // 接收长度
    if (getCfg().${module.module_name}.length_length > read_buffer.size()) {
        read_buffer.resize(getCfg().${module.module_name}.length_length);
    }
    _connection_ptr->read(read_buffer.data(), getCfg().${module.module_name}.length_length);
    len = std::stoi(std::string(read_buffer.data(), getCfg().${module.module_name}.length_length));

    if (len > read_buffer.size()) {
        read_buffer.resize(len);
    }
    _connection_ptr->read(read_buffer.data(), len);
    return nlohmann::json::parse(std::string(read_buffer.data(), len));
    % endif
}

int ${module.module_class_impl_name}::receive_length(std::shared_ptr<char[]> buffer, const TcpConnection::ErrorCode &ec, size_t length)
{
    if (ec) {
        SPDLOG_ERROR("receive length error[{}]", ec.message());
        SPDLOG_ERROR("connect ref [{}]", _connection_ptr.use_count());
        return -1;
    }
    SPDLOG_INFO("received length [{}]", length);
    std::string str_len(buffer.get(), getCfg().${module.module_name}.length_length);
    int len;
    try {
        len = std::stoi(str_len);
    }
    catch (std::exception &e) {
        SPDLOG_ERROR("接收长度失败[{}][{}]", e.what(), str_len);
        % if not module.no_resp:
        nlohmann::json j;
        j["code"] = -1;
        j["msg"] = "解析数据长度失败";
        auto msg = j.dump();
        SPDLOG_INFO("send msg[{}]", msg);
        _connection_ptr->async_write(msg.c_str(), msg.size(),
                std::bind(&${module.module_class_impl_name}::default_write_handler, this->shared_from_this(), std::placeholders::_1, std::placeholders::_2));
        % endif
        return -1;
    }
    size_t new_buffer_length = _buffer_length;
    // TODO 接收完body后是否需要缩小空间, 是否需要设置一个接收上限，防止过大长度
    if (len > max_buffer_length) {
        SPDLOG_ERROR("长度过大[{}]", len);
        // TODO 丢弃并返回失败原因
        // _connection_ptr->async_write(write_buffer.get(), write_buffer.size(), this->_write_cb)
        _connection_ptr->async_read(buffer.get(), getCfg().${module.module_name}.length_length,
                std::bind(&${module.module_class_impl_name}::receive_length, this->shared_from_this(), buffer, std::placeholders::_1, std::placeholders::_2));
        return -1;
    }
    while (len >= new_buffer_length) {
        new_buffer_length += buffer_length;
    }
    if (new_buffer_length != _buffer_length) {
        buffer.reset(new char[new_buffer_length]);
        _buffer_length = new_buffer_length;
    }
    _connection_ptr->async_read(buffer.get(), len,
            std::bind(&${module.module_class_impl_name}::receive_body, this->shared_from_this(), buffer, std::placeholders::_1, std::placeholders::_2));
    return len;
}

void ${module.module_class_impl_name}::receive_body(std::shared_ptr<char[]> buffer, const TcpConnection::ErrorCode &ec, size_t length)
{   
    if (ec) {
        SPDLOG_ERROR("receive body error[{}]", ec.message());
        return;
    }
    SPDLOG_INFO("received body length[{}]", length);
    _connection_ptr->async_read(buffer.get(), getCfg().${module.module_name}.length_length,
            std::bind(&${module.module_class_impl_name}::receive_length, this->shared_from_this(), buffer, std::placeholders::_1, std::placeholders::_2));
    std::string msg(buffer.get(), length);
    SPDLOG_INFO("received msg[{}]", msg);
    try {
        auto json = nlohmann::json::parse(msg);
        // int command = json["${module.command_name}"];
        % if module.no_resp:
        return receive_callback(json);
        % else:
        msg = receive_callback(json).dump();
        % endif
    }
    catch (std::exception &e) {
        nlohmann::json j;
        j["code"] = -1; 
        j["msg"] = "解析接口类型失败";
        msg = j.dump();
        SPDLOG_ERROR("解析接口类型失败[{}][{}]", j.dump(4), e.what());
    } 
    % if not module.no_resp: 
    SPDLOG_INFO("send msg[{}]", msg);
    _connection_ptr->async_write(msg.c_str(), msg.size(),
            std::bind(&${module.module_class_impl_name}::default_write_handler, this->shared_from_this(), std::placeholders::_1, std::placeholders::_2));
    % endif
}


void ${module.module_class_impl_name}::read_some(std::shared_ptr<char[]> buffer, const TcpConnection::ErrorCode &ec, size_t s)
{
    if (ec) {
        SPDLOG_ERROR("read_some error[{}]", ec.message());
        return;
    }
    SPDLOG_INFO("receive[{}]", std::string(buffer.get(), s));
    _connection_ptr->async_read_some(buffer.get(), _buffer_length,
            std::bind(&${module.module_class_impl_name}::read_some, this->shared_from_this(), buffer, std::placeholders::_1, std::placeholders::_2));
}

void ${module.module_class_impl_name}::default_read_handler(const TcpConnection::ErrorCode &ec, size_t s)
{
    if (ec) {
        SPDLOG_ERROR("read byte [{}] error[{}]", s, ec.message());
        return;
    }
}

void ${module.module_class_impl_name}::default_write_handler(const TcpConnection::ErrorCode &ec, size_t s)
{
    if (ec) {
        SPDLOG_ERROR("write byte [{}] error[{}]", s, ec.message());
        return;
    }
}


void ${module.module_class_impl_name}::init()
{
    % for api in module.request_apis:
    _callbacks[${api.command_code}] = std::bind(&${module.module_class_impl_name}::${api.name}_json, this, std::placeholders::_1);
    % endfor

    init_adapt();

## % if len(module.request_apis) > 0:
## _adapt_ptr->set_callback(std::bind(&${module.module_class_impl_name}::receive_callback, this->shared_from_this(), std::placeholders::_1));
## % endif
}

% if module.no_resp:
void ${module.module_class_impl_name}::receive_callback(const nlohmann::json &j)
% else:
nlohmann::json ${module.module_class_impl_name}::receive_callback(const nlohmann::json &j)
% endif
{
    CommandType command = j["${module.command_name}"];
    auto iter = _callbacks.find(command);
    if (iter == _callbacks.end()) {
        SPDLOG_ERROR("invalid command[{}]", command);
        assert(false);
    }
    return iter->second(j);
    // return _callbacks[command](j);
}

// 处理请求
% for api in module.request_apis:
% if module.no_resp:
void ${module.module_class_impl_name}::${api.name}_json(const nlohmann::json &j)
% else:
nlohmann::json ${module.module_class_impl_name}::${api.name}_json(const nlohmann::json &j)
% endif
{
    try {
        ${api.req.type.name} req = j;
        return ${api.name}(req);
    }
    catch (std::exception &e) {
        % if module.no_resp:
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
