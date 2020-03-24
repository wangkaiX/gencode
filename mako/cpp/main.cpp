% for framework in frameworks:
#include "${framework.include_file}"
% endfor

int main()
{
    boost::asio::io_context;
% for framework in frameworks:
    ${framework.network.class_name} ${gen_lower_camel(framework.network.class_name)}(io_context, boost::asio::ip::tcp::endpoint(ip, port));

% endfor
    io_context.run();
}
