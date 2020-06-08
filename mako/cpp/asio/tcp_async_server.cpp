#include "${module.module_name}/${module.module_name}_tcp_server.h"

${module.service_network_class_name}::${module.service_network_class_name}(boost::asio::io_context& io_context,
    const boost::asio::ip::tcp::endpoint& endpoint)
  : _io_context(io_context)
  , acceptor_(io_context, endpoint)
{
    do_accept();
}

void ${module.service_network_class_name}::do_accept()
{
    acceptor_.async_accept(
        [this](boost::system::error_code ec, boost::asio::ip::tcp::socket socket)
        {
            if (ec) {
                SPDLOG_ERROR("accept error [{}]", ec.message());
                return;
            }
            SPDLOG_INFO("new client [{}]", socket.remote_endpoint());
            auto connection_ptr = std::make_shared<TcpConnection>(_io_context, std::move(socket));
            auto api_ptr = std::make_shared<${module.service_api_class_name}>(_io_context, connection_ptr);
            api_ptr->init();

            do_accept();
        });
}
