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
/*

class AdaptBase
{
public:
    std::string request(const boost::beast::flat_buffer &buffer)
    {
        return std::string((const char*)buffer.data().data(), buffer.size());
    }
};
*/

void
fail(boost::beast::error_code ec, char const* what)
{
    std::cerr << what << ": " << ec.message() << "\n";
}

template <typename Adapt>
class session : public std::enable_shared_from_this<session<Adapt>>
{
    boost::beast::websocket::stream<boost::beast::tcp_stream> ws_;
    boost::beast::flat_buffer buffer_;
    std::shared_ptr<Adapt> adapt_ptr_;

public:
    // Take ownership of the socket
    explicit
    session(boost::asio::ip::tcp::socket&& socket, std::shared_ptr<Adapt> adapt_ptr)
        : ws_(std::move(socket))
        , adapt_ptr_(adapt_ptr)
    {
    }

    // Get on the correct executor
    void
    run()
    {
        // We need to be executing within a strand to perform async operations
        // on the I/O objects in this session. Although not strictly necessary
        // for single-threaded contexts, this example code is written to be
        // thread-safe by default.
        boost::asio::dispatch(ws_.get_executor(),
            boost::beast::bind_front_handler(
                &session::on_run,
                this->shared_from_this()));
    }

    // Start the asynchronous operation
    void
    on_run()
    {
        // Set suggested timeout settings for the boost::beast::websocket
        ws_.set_option(
            boost::beast::websocket::stream_base::timeout::suggested(
                boost::beast::role_type::server));

        // Set a decorator to change the Server of the handshake
        ws_.set_option(boost::beast::websocket::stream_base::decorator(
            [](boost::beast::websocket::response_type& res)
            {
                res.set(boost::beast::http::field::server,
                    std::string(BOOST_BEAST_VERSION_STRING) +
                        " boost::beast::websocket-server-async");
            }));
        // Accept the boost::beast::websocket handshake
        ws_.async_accept(
            boost::beast::bind_front_handler(
                &session::on_accept,
                this->shared_from_this()));
    }

    void
    on_accept(boost::beast::error_code ec)
    {
        if(ec)
            return fail(ec, "accept");

        // Read a message
        do_read();
    }

    void
    do_read()
    {
        // Read a message into our buffer
        ws_.async_read(
            buffer_,
            boost::beast::bind_front_handler(
                &session::on_read,
                this->shared_from_this()));
    }

    void
    on_read(
        boost::beast::error_code ec,
        std::size_t bytes_transferred)
    {
        boost::ignore_unused(bytes_transferred);

        // This indicates that the session was closed
        if(ec == boost::beast::websocket::error::closed)
            return;

        if(ec)
            fail(ec, "read");

        // Echo the message
        auto resp = adapt_ptr_->request(buffer_);
        ws_.text(ws_.got_text());
        ws_.async_write(
            boost::asio::buffer(resp),
            boost::beast::bind_front_handler(
                &session::on_write,
                this->shared_from_this()));
    }

    void
    on_write(
        boost::beast::error_code ec,
        std::size_t bytes_transferred)
    {
        boost::ignore_unused(bytes_transferred);

        if(ec)
            return fail(ec, "write");

        // Clear the buffer
        buffer_.consume(buffer_.size());

        // Do another read
        do_read();
    }
};

//------------------------------------------------------------------------------

// Accepts incoming connections and launches the sessions
template <typename Adapt>
class WebSocketServer: public std::enable_shared_from_this<WebSocketServer<Adapt>>
{
    boost::asio::io_context& ioc_;
    boost::asio::ip::tcp::acceptor acceptor_;
    std::shared_ptr<Adapt> adapt_ptr_;

public:
    WebSocketServer(
        boost::asio::io_context& ioc,
        boost::asio::ip::tcp::endpoint endpoint,
        std::shared_ptr<Adapt> adapt_ptr)
        : ioc_(ioc)
        , acceptor_(ioc)
        , adapt_ptr_(adapt_ptr)
    {
        boost::beast::error_code ec;

        // Open the acceptor
        acceptor_.open(endpoint.protocol(), ec);
        if(ec)
        {
            fail(ec, "open");
            return;
        }

        // Allow address reuse
        acceptor_.set_option(boost::asio::socket_base::reuse_address(true), ec);
        if(ec)
        {
            fail(ec, "set_option");
            return;
        }

        // Bind to the server address
        acceptor_.bind(endpoint, ec);
        if(ec)
        {
            fail(ec, "bind");
            return;
        }

        // Start listening for connections
        acceptor_.listen(
            boost::asio::socket_base::max_listen_connections, ec);
        if(ec)
        {
            fail(ec, "listen");
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
                &WebSocketServer::on_accept,
                this->shared_from_this()));
    }

    void
    on_accept(boost::beast::error_code ec, boost::asio::ip::tcp::socket socket)
    {
        if(ec)
        {
            fail(ec, "accept");
        }
        else
        {
            // Create the session and run it
            std::make_shared<session<Adapt>>(std::move(socket), adapt_ptr_)->run();
        }

        // Accept another connection
        do_accept();
    }
};

//------------------------------------------------------------------------------
/*

int main(int argc, char* argv[])
{
    // Check command line arguments.
    if (argc != 4)
    {
        std::cerr <<
            "Usage: boost::beast::websocket-server-async <address> <port> <threads>\n" <<
            "Example:\n" <<
            "    boost::beast::websocket-server-async 0.0.0.0 8080 1\n";
        return EXIT_FAILURE;
    }
    auto const address = boost::asio::ip::make_address(argv[1]);
    auto const port = static_cast<unsigned short>(std::atoi(argv[2]));
    auto const threads = std::max<int>(1, std::atoi(argv[3]));

    // The io_context is required for all I/O
    boost::asio::io_context ioc{threads};

    // Create and launch a listening port
    auto adapt = std::make_shared<AdaptBase>();
    std::make_shared<WebSocketServer<AdaptBase>>(ioc, boost::asio::ip::tcp::endpoint{address, port}, adapt)->run();

    // Run the I/O service on the requested number of threads
    std::vector<std::thread> v;
    v.reserve(threads - 1);
    for(auto i = threads - 1; i > 0; --i)
        v.emplace_back(
        [&ioc]
        {
            ioc.run();
        });
    ioc.run();

    return EXIT_SUCCESS;
}
*/
