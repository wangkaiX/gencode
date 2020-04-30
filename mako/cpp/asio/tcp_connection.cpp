#include "network/tcp_connection.h"

TcpConnection::TcpConnection(boost::asio::io_context& io_context, const boost::asio::ip::tcp::endpoint &ep)
    : io_context_(io_context)
    , socket_(io_context)
{
    connect(ep);
}

TcpConnection::TcpConnection(boost::asio::io_context& io_context, boost::asio::ip::tcp::socket &&socket)
    : io_context_(io_context)
    , socket_(std::move(socket))
{
}

TcpConnection::~TcpConnection()
{
    this->close();
}

const boost::asio::ip::tcp::endpoint TcpConnection::remote_endpoint() const
{
    return socket_.remote_endpoint();
}

const boost::asio::ip::tcp::endpoint TcpConnection::local_endpoint() const
{
    return socket_.local_endpoint();
}

void TcpConnection::async_wait_read(WaitCallback cb)
{
    using namespace boost::asio;
    socket_.async_wait(ip::tcp::socket::wait_read, cb);
}

void TcpConnection::async_wait_write(WaitCallback cb)
{
    using namespace boost::asio;
    socket_.async_wait(ip::tcp::socket::wait_write, cb);
}

TcpConnection::ErrorCode TcpConnection::write(const char *data, size_t length)
{
    using namespace boost::asio;
    TcpConnection::ErrorCode ec;
    boost::asio::write(socket_, buffer(data, length), ec);
    return ec;
}

void TcpConnection::async_write(const char *data, size_t length, WriteCallback cb)
{
    assert(cb && "callback can not be null");
    using namespace boost::asio;
    boost::asio::async_write(socket_, buffer(data, length), cb);
}

TcpConnection::ErrorCode TcpConnection::read(char *data, size_t length)
{
    using namespace boost::asio;
    TcpConnection::ErrorCode ec;
    boost::asio::read(socket_, buffer(data, length), ec);
    return ec;
}

void TcpConnection::async_read(char *data, size_t length, ReadCallback cb)
{
    assert(cb && "callback can not be null");
    using namespace boost::asio;
    boost::asio::async_read(socket_, buffer(data, length), cb);
}

void TcpConnection::async_read_some(char *data, size_t length, ReadCallback cb)
{
    assert(cb && "callback can not be null");
    using namespace boost::asio;
    socket_.async_read_some(buffer(data, length), cb);
}

void TcpConnection::close()
{
    boost::asio::post(io_context_, [this]() { socket_.close(); });
}

TcpConnection::ErrorCode TcpConnection::connect(const boost::asio::ip::tcp::endpoint &ep)
{
    TcpConnection::ErrorCode ec;
    socket_.connect(ep, ec);
    return ec;
}

std::ostream &operator<<(std::ostream &os, const boost::asio::ip::tcp::endpoint &ep)
{
    return os << ep.address().to_string() << ":" << ep.port();
}
