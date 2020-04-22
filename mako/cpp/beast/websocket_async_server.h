#include <boost/beast/core.hpp>
#include <boost/beast/websocket.hpp>
#include <boost/asio/dispatch.hpp>
#include <boost/asio/strand.hpp>
#include <algorithm>
#include <cstdlib>
#include <functional>
#include <iostream>
#include <memory>
#include <string>
#include <thread>
#include <vector>
#include "websocket_connection.h"
% if log == "spdlog":
#include <spdlog/spdlog.h>
% endif

<%
    service_class_name = framework.service_class_name
%>

// Accepts incoming connections and launches the WebsocketConnections
template <typename Adapt>
class ${service_class_name}: public std::enable_shared_from_this<${service_class_name}<Adapt>>
{
    boost::asio::io_context& ioc_;
    boost::asio::ip::tcp::acceptor acceptor_;
    std::shared_ptr<Adapt> adapt_ptr_;

public:
    ${gen_upper_camel(framework.service_name)}Server(
        boost::asio::io_context& ioc,
        boost::asio::ip::tcp::endpoint endpoint)
        : ioc_(ioc)
        , acceptor_(ioc)
        , adapt_ptr_(std::make_shared<Adapt>())
    {
        boost::beast::error_code ec;

        // Open the acceptor
        acceptor_.open(endpoint.protocol(), ec);
        if(ec) {
            SPDLOG_ERROR("acceptor open:[{}]", ec.message());
            return;
        }

        // Allow address reuse
        acceptor_.set_option(boost::asio::socket_base::reuse_address(true), ec);
        if(ec) {
            SPDLOG_ERROR("set_option:[{}]", ec.message());
            return;
        }

        // Bind to the server address
        acceptor_.bind(endpoint, ec);
        if(ec) {
            SPDLOG_ERROR("bind:[{}]", ec.message());
            return;
        }

        // Start listening for connections
        acceptor_.listen(
            boost::asio::socket_base::max_listen_connections, ec);
        if(ec) {
            SPDLOG_ERROR("listen:[{}]", ec.message());
            return;
        }
    }

    // Start accepting incoming connections
    void
    run()
    {
        do_accept();
    }

private:
    void
    do_accept()
    {
        // The new connection gets its own strand
        acceptor_.async_accept(
            boost::asio::make_strand(ioc_),
            boost::beast::bind_front_handler(
                &${service_class_name}::on_accept,
                this->shared_from_this()));
    }

    void
    on_accept(boost::beast::error_code ec, boost::asio::ip::tcp::socket socket)
    {
        if(ec) {
            SPDLOG_ERROR("accept:[{}]", ec.message());
        }
        else {
            // Create the WebsocketConnection and run it
            std::make_shared<WebsocketConnection<Adapt>>(std::move(socket), adapt_ptr_)->run();
        }

        // Accept another connection
        do_accept();
    }
};
