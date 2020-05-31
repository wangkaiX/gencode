#include <csignal>
#include <unistd.h>
#include <chrono>
using namespace std;
#include <boost/asio.hpp>
#include <spdlog/spdlog.h>
#include <spdlog/sinks/daily_file_sink.h>

% for framework in frameworks:
    % if framework.is_server:
#include "${framework.service_name}/${framework.service_name}_tcp_server.h"
    % else:
#include "${framework.service_name}/api.h"
    % endif
% endfor
#include "config/config.h"

<% from code_framework.common import type_set %>

void sigsegv(int x)
{
    auto pid = getpid();
    char buf[32] = {}; 
    snprintf(buf, sizeof(buf), "gcore %d", pid);
    spdlog::shutdown();
    SPDLOG_INFO("sigsegv");
    system(buf);
}

void init_log()
{
    auto daily = spdlog::daily_logger_mt("daily", "logs/app.log", 0, 0); 
    spdlog::set_default_logger(daily);
    spdlog::set_level(spdlog::level::info);
    spdlog::set_pattern("[%Y-%m-%d %H:%M:%S.%e][%l][%s:%#]%v");
    // spdlog::flush_every(0s);
    spdlog::flush_every(1s);
}

int main()
{
    init_log();
    signal(SIGSEGV, sigsegv);
    signal(SIGABRT, sigsegv);
    using namespace boost;
    asio::io_context io_context;
    % for framework in frameworks:
        % if framework.is_server:
            % if framework.network == type_set.asio_tcp_async:
    auto ${framework.service_name}_ptr = std::make_shared<${framework.service_network_class_name}>(io_context, asio::ip::tcp::endpoint(asio::ip::tcp::v4(), getCfg().${framework.service_name}.port));
            % elif framework.network == type_set.beast_websocket_async:
    auto ${framework.service_name}_ptr = std::make_shared<${framework.service_network_class_name}>(io_context, asio::ip::tcp::endpoint(asio::ip::tcp::v4(), getCfg().${framework.service_name}.port));
            % endif
    // ${framework.service_name}_ptr->init();
        % else:
            % if framework.network == type_set.asio_tcp_async:
    auto ${framework.service_name}_ptr = std::make_shared<${framework.service_api_class_name}>(io_context, asio::ip::tcp::endpoint(asio::ip::tcp::v4(), getCfg().${framework.service_name}.port));
            % elif framework.network == type_set.beast_websocket_async:
    auto ${framework.service_name}_ptr = std::make_shared<${framework.service_api_class_name}>(io_context, asio::ip::tcp::endpoint(asio::ip::tcp::v4(), getCfg().${framework.service_name}.port));
            % endif
        % endif

    % endfor
    SPDLOG_INFO("service start!");
    io_context.run();
}
