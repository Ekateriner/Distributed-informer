#pragma once

#include <map>
#include <string>
#include "alert_parser.h"
#include "handler.h"
#include "router_controller.h"
#include "abstract_sender.h"
#include <mutex>

class AlertHandler : public network::Handler {
 public:
  explicit AlertHandler();
  void handlePost(network::http_request message) override;

 private:

  void dump_alert();

  AlertParser parser_;
  const std::map <std::string, std::shared_ptr<Factory> > factories_;
  static int alerts_stored_;
  std::mutex file_mutex;
};
