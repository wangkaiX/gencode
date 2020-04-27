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
#include "${framework.service_name}/api.h"

//----------------------------------------------------------------------
class ${framework.service_network_class_name}
{
public:
    ${framework.service_network_class_name}(boost::asio::io_context& io_context,
        const boost::asio::ip::tcp::endpoint& endpoint);

    // void setReadCallback(TcpConnection::ReadCallback &cb)
    // {
    //     _read_callback = cb;
    // }

    // void setWriteCallback(TcpConnection::ReadCallback &cb)
    // {
    //     _write_callback = cb;
    // }

private:
    void do_accept();

    // TcpConnection::ReadCallback _read_callback;
    // TcpConnection::ReadCallback _write_callback;
    boost::asio::io_context &_io_context;
    boost::asio::ip::tcp::acceptor acceptor_;
};
