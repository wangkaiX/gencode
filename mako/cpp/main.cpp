#include <boost/asio.hpp>
using namespace boost;

% for framework in frameworks:
    % if framework.is_server:
#include "${framework.service_name}/${framework.service_name}_tcp_server.h"
#include "${framework.service_name}/${framework.adapt_name}.h"
    % endif
% endfor
#include "config/config.h"

<% from code_framework.common import type_set %>

int main()
{
    boost::asio::io_context io_context;
    % for framework in frameworks:
        % if framework.is_server:
        % if framework.network == type_set.asio_tcp_async:
    auto ${framework.service_name}_ptr = std::make_shared<${framework.service_network_class_name}>(io_context, asio::ip::tcp::endpoint(asio::ip::tcp::v4(), getCfg().${framework.service_name}.port));
        % elif framework.network == type_set.beast_websocket_async:
    auto ${framework.service_name}_ptr = std::make_shared<${framework.service_network_class_name}>(io_context, asio::ip::tcp::endpoint(asio::ip::tcp::v4(), getCfg().${framework.service_name}.port));
        % endif
    // ${framework.service_name}_ptr->run();
        % endif

    % endfor
    io_context.run();
}
