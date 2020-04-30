#pragma once
#include <chrono>
#include <boost/asio.hpp>

class TcpConnection
{
public:
    using ErrorCode = boost::system::error_code;
    using WriteCallback = std::function<void(const ErrorCode&, size_t)>;
    using ReadCallback = std::function<void(const ErrorCode&, size_t)>;
    using WaitCallback = std::function<void(const ErrorCode&)>;
    using TimerCallback = std::function<void(const ErrorCode&)>;
public:
    TcpConnection(boost::asio::io_context& io_context, const boost::asio::ip::tcp::endpoint &ep);

    TcpConnection(boost::asio::io_context& io_context, boost::asio::ip::tcp::socket &&socket);

    ~TcpConnection();

    const boost::asio::ip::tcp::endpoint remote_endpoint() const;

    const boost::asio::ip::tcp::endpoint local_endpoint() const;

    template <typename Rep, typename Period>
    void timer_task(std::chrono::duration<Rep, Period> &&timeout, TimerCallback cb)
    {
        auto timer_ptr = std::make_shared<boost::asio::steady_timer>(io_context_, timeout);
        timer_ptr->async_wait([timer_ptr, cb](ErrorCode &ec){ 
                cb(ec);
                }
            );
    }

    void async_wait_read(WaitCallback cb);

    void async_wait_write(WaitCallback cb);

    ErrorCode write(const char *data, size_t length);

    void async_write(const char *data, size_t length, WriteCallback cb);

    ErrorCode read(char *data, size_t length);

    void async_read(char *data, size_t length, ReadCallback cb);

    void async_read_some(char *data, size_t length, ReadCallback cb);

    void close();

private:
    boost::asio::io_context& io_context_;
    boost::asio::ip::tcp::socket socket_;
private:
    ErrorCode connect(const boost::asio::ip::tcp::endpoint &ep);
};

#include "spdlog/fmt/ostr.h"
std::ostream &operator<<(std::ostream &os, const boost::asio::ip::tcp::endpoint &ep);
