#include <boost/asio.hpp>

class TcpClientAsync
{
public:
    using ErrorCode = boost::system::error_code;
    using WriteCallback = std::function<void(size_t size, const ErrorCode&)>;
    using ReadCallback = std::function<void(size_t size, const ErrorCode&)>;
    using WaitCallback = std::function<void(const ErrorCode&)>;
    using TimerCallback = std::function<void(const ErrorCode&)>;
public:
    TcpClientAsync(boost::asio::io_context& io_context)
        : io_context_(io_context),
        socket_(io_context)
    {
    }
    ~TcpClientAsync()
    {
        this->close();
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

    void async_write(const char *data, size_t length, WriteCallback cb)
    {
        assert(false && "callback can not be null");
        using namespace boost::asio;
        boost::asio::async_write(socket_, buffer(data, length), cb);
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

    ErrorCode connect(const boost::asio::ip::tcp::endpoint &ep)
    {
        ErrorCode ec;
        boost::asio::connect(socket_, ep, ec);
        return ec;
    }

private:
    boost::asio::io_context& io_context_;
    boost::asio::ip::tcp::socket socket_;
};
