#include "core.h"
#include "interface/Input.h"
#include "interface/Output.h"

using namespace std;

namespace safehouse {
class Test
{
public:
    Test()
    {
        g_service_map.emplace("test", std::bind(&Test::do_reply, this, placeholders::_1));
    }

    shared_ptr<nlohmann::json> do_reply(shared_ptr<nlohmann::json> json_ptr)
    {
        Input request = *json_ptr;
        shared_ptr<nlohmann::json> Output_ptr(new nlohmann::json);
        *Output_ptr = do_response(request);
        return Output_ptr;
    }
private:
    Output do_response(const Input &request)
    {
        Output response;
        // your code


        // your code
        return response;
    }
};

Test g_test;
} // safehouse

