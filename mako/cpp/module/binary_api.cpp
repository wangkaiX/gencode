#include "${module.name}/api.h"
#include <cassert>

${module.service_api_class_name}::${module.service_api_class_name}(boost::asio::io_context &io_context, std::shared_ptr<${connection_class_name}> connection_ptr)
    : _io_context(io_context)
    , _connection_ptr(connection_ptr)
{
}

${module.service_api_class_name}::~${module.service_api_class_name}()
{   
    SPDLOG_INFO("destroy ${module.service_api_class_name}");
}

void ${module.service_api_class_name}::init_adapt()
{   
    std::shared_ptr<char[]> buffer(new char[buffer_length]);
    _buffer_length = buffer_length;

    % if len(module.request_apis) > 0:
    _connection_ptr->async_read(buffer.get(), sizeof(CommandHeader),
            std::bind(&${module.service_api_class_name}::receive_header, this->shared_from_this(), buffer, std::placeholders::_1, std::placeholders::_2));
    % else:
    // 防止释放
    _connection_ptr->async_read_some(buffer.get(), _buffer_length,
            std::bind(&${module.service_api_class_name}::read_some, this->shared_from_this(), buffer, std::placeholders::_1, std::placeholders::_2));
    % endif
}

% if module.no_resp:
void ${module.service_api_class_name}::request(std:::shared_ptr<char[]> data_ptr, size_t size)
% else:
std::vector<char> ${module.service_api_class_name}::request(std:::vector<char> data, size_t size)
% endif
{   
        % if module.no_resp:
    _connection_ptr->async_write(data.data(), size,
            std::bind(&${module.service_api_class_name}::default_write_handler, this->shared_from_this(), std::placeholders::_1, std::placeholders::_2));
        % else:
    _connection_ptr->write(data_ptr.get(), size);
    // 接收长度
    if (sizeof(CommandHeader) > read_buffer.size()) {
        read_buffer.resize(sizeof(CommandHeader));
    }
    _connection_ptr->read(read_buffer.data(), sizeof(CommandHeader));
    len = static_cast<CommandHeader*>(read_buffer.data())->data_length;

    if (len > read_buffer.size()) {
        read_buffer.resize(len);
    }
    _connection_ptr->read(read_buffer.data()+sizeof(CommandHeader), len);
    return std::shared_ptr<char[]>::parse(std::string(read_buffer.data(), len));
        % endif
    % else:
        print("未完善的逻辑")
        assert False
    % endif
}

int ${module.service_api_class_name}::receive_header(std::shared_ptr<char[]> buffer, const TcpConnection::ErrorCode &ec, size_t length)
{
    if (ec) {
        SPDLOG_ERROR("receive length error[{}]", ec.message());
        SPDLOG_ERROR("connect ref [{}]", _connection_ptr.use_count());
        return -1;
    }
    SPDLOG_INFO("received length [{}]", length);
    std::string str_len(buffer.get(), getCfg().${module.name}.length_length);
    int len;
    try {
        len = std::stoi(str_len);
    }
    catch (std::exception &e) {
        SPDLOG_ERROR("接收长度失败[{}][{}]", e.what(), str_len);
        % if not module.no_resp:
        std::shared_ptr<char[]> j;
        j["code"] = -1;
        j["msg"] = "解析数据长度失败";
        auto msg = j.dump();
        SPDLOG_INFO("send msg[{}]", msg);
        _connection_ptr->async_write(msg.c_str(), msg.size(),
                std::bind(&${module.service_api_class_name}::default_write_handler, this->shared_from_this(), std::placeholders::_1, std::placeholders::_2));
        % endif
        return -1;
    }
    size_t new_buffer_length = _buffer_length;
    // TODO 接收完body后是否需要缩小空间, 是否需要设置一个接收上限，防止过大长度
    if (len > max_buffer_length) {
        SPDLOG_ERROR("长度过大[{}]", len);
        // TODO 丢弃并返回失败原因
        // _connection_ptr->async_write(write_buffer.get(), write_buffer.size(), this->_write_cb)
        _connection_ptr->async_read(buffer.get(), getCfg().${module.name}.length_length,
                std::bind(&${module.service_api_class_name}::receive_length, this->shared_from_this(), buffer, std::placeholders::_1, std::placeholders::_2));
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
            std::bind(&${module.service_api_class_name}::receive_body, this->shared_from_this(), buffer, std::placeholders::_1, std::placeholders::_2));
    return len;
}

void ${module.service_api_class_name}::receive_body(std::shared_ptr<char[]> buffer, const TcpConnection::ErrorCode &ec, size_t length)
{   
    if (ec) {
        SPDLOG_ERROR("receive body error[{}]", ec.message());
        return;
    }
    SPDLOG_INFO("received body length[{}]", length);
    _connection_ptr->async_read(buffer.get(), getCfg().${module.name}.length_length,
            std::bind(&${module.service_api_class_name}::receive_length, this->shared_from_this(), buffer, std::placeholders::_1, std::placeholders::_2));
    std::string msg(buffer.get(), length);
    SPDLOG_INFO("received msg[{}]", msg);
    try {
        auto json = std::shared_ptr<char[]>::parse(msg);
        % if module.no_resp:
        return receive_callback(json);
        % else:
        msg = receive_callback(json).dump();
        % endif
    }
    catch (std::exception &e) {
        std::shared_ptr<char[]> j;
        j["code"] = -1; 
        j["msg"] = "解析接口类型失败";
        msg = j.dump();
        SPDLOG_ERROR("解析接口类型失败[{}][{}]", j.dump(4), e.what());
    } 
    % if not module.no_resp: 
    SPDLOG_INFO("send msg[{}]", msg);
    _connection_ptr->async_write(msg.c_str(), msg.size(),
            std::bind(&${module.service_api_class_name}::default_write_handler, this->shared_from_this(), std::placeholders::_1, std::placeholders::_2));
    % endif
}


void ${module.service_api_class_name}::read_some(std::shared_ptr<char[]> buffer, const TcpConnection::ErrorCode &ec, size_t s)
{
    if (ec) {
        SPDLOG_ERROR("read_some error[{}]", ec.message());
        return;
    }
    SPDLOG_INFO("receive[{}]", std::string(buffer.get(), s));
    _connection_ptr->async_read_some(buffer.get(), _buffer_length,
            std::bind(&${module.service_api_class_name}::read_some, this->shared_from_this(), buffer, std::placeholders::_1, std::placeholders::_2));
}

void ${module.service_api_class_name}::default_read_handler(const TcpConnection::ErrorCode &ec, size_t s)
{
    if (ec) {
        SPDLOG_ERROR("read byte [{}] error[{}]", s, ec.message());
        return;
    }
}

void ${module.service_api_class_name}::default_write_handler(const TcpConnection::ErrorCode &ec, size_t s)
{
    if (ec) {
        SPDLOG_ERROR("write byte [{}] error[{}]", s, ec.message());
        return;
    }
}


void ${module.service_api_class_name}::init()
{
    % for api in module.request_apis:
    _callbacks[${api.command_code}] = std::bind(&${module.service_api_class_name}::${api.name}_json, this, std::placeholders::_1);
    % endfor

    init_adapt();

## % if len(module.request_apis) > 0:
## _adapt_ptr->set_callback(std::bind(&${module.service_api_class_name}::receive_callback, this->shared_from_this(), std::placeholders::_1));
## % endif
}

% if module.no_resp:
void ${module.service_api_class_name}::receive_callback(std:::shared_ptr<char[]> data_ptr)
% else:
std::shared_ptr<char[]> ${module.service_api_class_name}::receive_callback(std:::shared_ptr<char[]> data_ptr)
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
void ${module.service_api_class_name}::${api.name}_binary(std:::shared_ptr<char[]> data_ptr)
% else:
std::shared_ptr<char[]> ${module.service_api_class_name}::${api.name}_binary(std:::shared_ptr<char[]> data_ptr)
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
