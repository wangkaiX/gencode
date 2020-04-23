#pragma once
#include <chrono>
#include <boost/asio.hpp>

class TcpConnection
{
public:
    using ErrorCode = boost::system::error_code;
    using WriteCallback = std::function<void(size_t size, const ErrorCode&)>;
    using ReadCallback = std::function<void(size_t size, const ErrorCode&)>;
    using WaitCallback = std::function<void(const ErrorCode&)>;
    using TimerCallback = std::function<void(const ErrorCode&)>;
public:
    TcpConnection(boost::asio::io_context& io_context, const boost::asio::ip::tcp::endpoint &ep)
        : io_context_(io_context)
        , socket_(io_context)
    {
        connect(ep);
    }

    TcpConnection(boost::asio::io_context& io_context, boost::asio::ip::tcp::socket &&socket)
        : io_context_(io_context)
        , socket_(std::move(socket))
    {
    }

    ~TcpConnection()
    {
        this->close();
    }

    const boost::asio::ip::tcp::endpoint remote_endpoint() const
    {
        return socket_.remote_endpoint();
    }

    const boost::asio::ip::tcp::endpoint local_endpoint() const
    {
        return socket_.local_endpoint();
    }

    template <typename Rep, typename Period>
    void timer_task(std::chrono::duration<Rep, Period> &&timeout, TimerCallback cb)
    {
        auto timer_ptr = std::make_shared<boost::asio::steady_timer>(io_context_, timeout);
        timer_ptr->async_wait([timer_ptr, cb](ErrorCode &ec){ 
                cb(ec);
                }
            );
    }

    void async_wait_read(WaitCallback cb)
    {
        using namespace boost::asio;
        socket_.async_wait(ip::tcp::socket::wait_read, cb);
    }

    void async_wait_write(WaitCallback cb)
    {
        using namespace boost::asio;
        socket_.async_wait(ip::tcp::socket::wait_write, cb);
    }

    ErrorCode write(const char *data, size_t length)
    {
        using namespace boost::asio;
        ErrorCode ec;
        boost::asio::write(socket_, buffer(data, length), ec);
        return ec;
    }

    void async_write(const char *data, size_t length, WriteCallback cb)
    {
        assert(false && "callback can not be null");
        using namespace boost::asio;
        boost::asio::async_write(socket_, buffer(data, length), cb);
    }

    ErrorCode read(char *data, size_t length)
    {
        using namespace boost::asio;
        ErrorCode ec;
        boost::asio::read(socket_, buffer(data, length), ec);
        return ec;
    }

    void async_read(char *data, size_t length, WriteCallback cb)
    {
        using namespace boost::asio;
        boost::asio::async_read(socket_, buffer(data, length), cb);
    }

    void close()
    {
        boost::asio::post(io_context_, [this]() { socket_.close(); });
    }

private:
    boost::asio::io_context& io_context_;
    boost::asio::ip::tcp::socket socket_;
private:
    ErrorCode connect(const boost::asio::ip::tcp::endpoint &ep)
    {
        ErrorCode ec;
        boost::asio::connect(socket_, ep, ec);
        return ec;
    }
};

#include "spdlog/fmt/ostr.h"
inline std::ostream &operator<<(std::ostream &os, const boost::asio::ip::tcp::endpoint &ep)
{
    return os << ep.address().to_string() << ":" << ep.port();
}
