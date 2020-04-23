//
// chat_server.cpp
// ~~~~~~~~~~~~~~~
//
// Copyright (c) 2003-2019 Christopher M. Kohlhoff (chris at kohlhoff dot com)
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//

#include <cstdlib>
#include <deque>
#include <iostream>
#include <list>
#include <memory>
#include <set>
#include <utility>
#include <boost/asio.hpp>

#include "tcp_connection.h"

//----------------------------------------------------------------------
// template <typename Adapt>
class TcpServer
{
public:
    TcpServer(boost::asio::io_context& io_context,
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
                }

                do_accept();
            });
    }

    // TcpConnection::ReadCallback _read_callback;
    // TcpConnection::ReadCallback _write_callback;
    boost::asio::io_context &_io_context;
    boost::asio::ip::tcp::acceptor acceptor_;
};
