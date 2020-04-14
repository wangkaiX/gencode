#include <boost/asio.hpp>
using namespace boost;

% for framework in frameworks:
#include "service/${framework.service_name}.h"
#include "service/${framework.adapt_name}.h"
% endfor
#include "config/config.h"

int main()
{
    boost::asio::io_context io_context;
    % for framework in frameworks:
    auto ${framework.service_name}_ptr = std::make_shared<${framework.service_class_name}<${framework.adapt_class_name}>>(io_context, asio::ip::tcp::endpoint(asio::ip::tcp::v4(), getCfg().${framework.service_name}.port));
    ${framework.service_name}_ptr->run();
    % endfor
    io_context.run();
}
