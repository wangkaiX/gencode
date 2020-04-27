#include "${framework.service_name}/${framework.service_name}_tcp_server.h"

${framework.service_network_class_name}::${framework.service_network_class_name}(boost::asio::io_context& io_context,
    const boost::asio::ip::tcp::endpoint& endpoint)
  : _io_context(io_context)
  , acceptor_(io_context, endpoint)
{
    do_accept();
}

void ${framework.service_network_class_name}::do_accept()
{
    acceptor_.async_accept(
        [this](boost::system::error_code ec, boost::asio::ip::tcp::socket socket)
        {
            if (!ec) {
              auto connection_ptr = std::make_shared<TcpConnection>(_io_context, std::move(socket));
              auto adapt_ptr = std::make_shared<${framework.service_api_class_name}>(_io_context, connection_ptr);
              // adapt_ptr->run();
            }

            do_accept();
        });
}
