#ifndef MIRAI_SDK_HPP
#define MIRAI_SDK_HPP

#include <string>
#include <map>

namespace mirai {

class MiraiSDK {
public:
    MiraiSDK(const std::string& session_id = "default_cpp_session") : session_id_(session_id) {}

    void observe(const std::map<std::string, std::string>& game_state) {}
    
    std::string tick() {
        return "Dash";
    }

    void learn(const std::map<std::string, std::string>& match_result) {}

private:
    std::string session_id_;
};

} // namespace mirai

#endif // MIRAI_SDK_HPP
