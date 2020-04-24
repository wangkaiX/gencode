#pragma once

#include <cstdlib>
#include <deque>
#include <iostream>
#include <list>
#include <memory>
#include <set>
#include <utility>
#include <boost/asio.hpp>

#include "network/tcp_connection.h"
#include "${framework.service_name}/${framework.adapt_name}.h"

//----------------------------------------------------------------------
class ${framework.service_class_name}TcpServer
{
public:
    ${framework.service_class_name}TcpServer(boost::asio::io_context& io_context,
        const boost::asio::ip::tcp::endpoint& endpoint)
      : _io_context(io_context)
      , acceptor_(io_context, endpoint)
    {
        do_accept();
    }

    // void setReadCallback(TcpConnection::ReadCallback &cb)
    // {
    //     _read_callback = cb;
    // }

    // void setWriteCallback(TcpConnection::ReadCallback &cb)
    // {
    //     _write_callback = cb;
    // }

private:
    void do_accept()
    {
        acceptor_.async_accept(
            [this](boost::system::error_code ec, boost::asio::ip::tcp::socket socket)
            {
                if (!ec) {
                  auto connection_ptr = std::make_shared<TcpConnection>(_io_context, std::move(socket));
                  auto adapt_ptr = std::make_shared<${framework.adapt_class_name}<TcpConnection>>(_io_context, connection_ptr);
                  // adapt_ptr->run();
                }

                do_accept();
            });
    }

    // TcpConnection::ReadCallback _read_callback;
    // TcpConnection::ReadCallback _write_callback;
    boost::asio::io_context &_io_context;
    boost::asio::ip::tcp::acceptor acceptor_;
};
