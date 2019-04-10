#include "service/http_server.h"
#include "interface/${request}.h"
#include "interface/${response}.h"

using namespace std;

namespace safehouse {
class ${class_name}
{
public:
    ${class_name}()
    {
        g_service_map.emplace("${interface_name}", std::bind(&${class_name}::do_reply, this, placeholders::_1));
    }

    shared_ptr<nlohmann::json> do_reply(shared_ptr<nlohmann::json> json_ptr)
    {
        ${struct_request} request = *json_ptr;
        shared_ptr<nlohmann::json> ${response}_ptr(new nlohmann::json);
        *${response}_ptr = do_response(request);
        return ${response}_ptr;
    }
private:
    ${struct_response} do_response(const ${struct_request} &request)
    {
        ${struct_response} response;
        // your code


        // your code
        return response;
    }
};

${class_name} g_${interface_name};
} // safehouse

