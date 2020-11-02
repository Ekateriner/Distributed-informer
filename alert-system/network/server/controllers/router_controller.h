#pragma once

#include <initializer_list>
#include <string>
#include <unordered_map>

#include "basic_controller.h"
#include "handler.h"

namespace network {

class RouterController : public BasicController, public Handler {
 public:
  explicit RouterController(const std::string& uri_string
                          , std::initializer_list<std::pair<const std::string, Handler*>> handlers);

  ~RouterController() override;

  void initRestOpHandlers() override;

  void handleGet(http_request message) override;
  void handlePost(http_request message) override;
  void handlePut(http_request message) override;
  void handleHead(http_request message) override;
  void handleDelete(http_request message) override;
  void handleConnect(http_request message) override;
  void handleOptions(http_request message) override;
  void handleTrace(http_request message) override;
  void handlePatch(http_request message) override;
  void handleMerge(http_request message) override;

 private:
  Handler* getHandlerByPath(const std::string& api_path);

 private:
  std::unordered_map<std::string, Handler*> handlers_;
};

} // namespace network


