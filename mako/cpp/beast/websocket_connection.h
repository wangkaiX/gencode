#pragma once
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
// % if log == "spdlog":
#include <spdlog/spdlog.h>
// % endif

class WebsocketConnection : public std::enable_shared_from_this<WebsocketConnection>
{
    boost::beast::flat_buffer buffer_;
    boost::asio::ip::tcp::endpoint _local_ep;
    boost::asio::ip::tcp::endpoint _remote_ep;
    boost::beast::websocket::stream<boost::beast::tcp_stream> _ws;

public:
    using ErrorCode = boost::beast::error_code;
    // Take ownership of the socket
    explicit
    WebsocketConnection(boost::asio::ip::tcp::socket&& socket)
        : _local_ep(socket.local_endpoint())
        , _remote_ep(socket.remote_endpoint())
        , _ws(std::move(socket))
    {
    }

    const boost::asio::ip::tcp::endpoint &remote_endpoint()
    {
        return _remote_ep;
    }

    const boost::asio::ip::tcp::endpoint &local_endpoint()
    {
        return _local_ep;
    }

    // Get on the correct executor
    void
    run()
    {
        // We need to be executing within a strand to perform async operations
        // on the I/O objects in this WebsocketConnection. Although not strictly necessary
        // for single-threaded contexts, this example code is written to be
        // thread-safe by default.
        boost::asio::dispatch(_ws.get_executor(),
            boost::beast::bind_front_handler(
                &WebsocketConnection::on_run,
                this->shared_from_this()));
    }

    // Start the asynchronous operation
    void
    on_run()
    {
        // Set suggested timeout settings for the boost::beast::websocket
        _ws.set_option(
            boost::beast::websocket::stream_base::timeout::suggested(
                boost::beast::role_type::server));

        // Set a decorator to change the Server of the handshake
        _ws.set_option(boost::beast::websocket::stream_base::decorator(
            [](boost::beast::websocket::response_type& res)
            {
                res.set(boost::beast::http::field::server,
                    std::string(BOOST_BEAST_VERSION_STRING) +
                        " boost::beast::websocket-server-async");
            }));
        // Accept the boost::beast::websocket handshake
        _ws.async_accept(
            boost::beast::bind_front_handler(
                &WebsocketConnection::on_accept,
                this->shared_from_this()));
    }

    void
    on_accept(boost::beast::error_code ec)
    {
        if(ec) {
            SPDLOG_ERROR("accept:[{}]", ec.message());
            return;
        }

        // Read a message
        do_read();
    }

    void
    do_read()
    {
        // Read a message into our buffer
        _ws.async_read(
            buffer_,
            boost::beast::bind_front_handler(
                &WebsocketConnection::on_read,
                this->shared_from_this()));
    }

    void
    on_read(
        boost::beast::error_code ec,
        std::size_t bytes_transferred)
    {
        boost::ignore_unused(bytes_transferred);

        // This indicates that the WebsocketConnection was closed
        if(ec == boost::beast::websocket::error::closed)
            return;

        if(ec) {
            SPDLOG_ERROR("read:[{}]", ec.message());
        }

        auto resp = adapt_ptr_->request(static_cast<const char*>(buffer_.data().data()), buffer_.data().size());
        _ws.text(_ws.got_text());
        _ws.async_write(
            boost::asio::buffer(resp),
            boost::beast::bind_front_handler(
                &WebsocketConnection::on_write,
                this->shared_from_this()));
    }

    void
    on_write(
        boost::beast::error_code ec,
        std::size_t bytes_transferred)
    {
        boost::ignore_unused(bytes_transferred);

        if(ec) {
            SPDLOG_ERROR("write:[{}]", ec.message());
            return;
        }

        // Clear the buffer
        buffer_.consume(buffer_.size());

        // Do another read
        do_read();
    }
};
