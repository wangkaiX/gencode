#pragma once

#include <cstdlib>
#include <deque>
#include <iostream>
#include <list>
#include <memory>
#include <set>
#include <utility>
#include <boost/asio.hpp>

#include "net/tcp_connection.h"
// #include "${module.name}/api.h"

//----------------------------------------------------------------------
class ${module.network_server_class_name}
{
public:
    ${module.network_server_class_name}(net::io_context& io_context,
        const tcp::endpoint& endpoint);

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
    net::io_context &_io_context;
    tcp::acceptor acceptor_;
};
