#pragma once

#include <string>
#include <vector>

#include <cpprest/http_client.h>

#include "recipient.h"


class ConfiguratorService {
public:
  std::vector<Recipient> getRecipientByNotificationId(const std::string & notification_id);
private:
  const std::string CONFIGURATOR_HOST = "http://127.0.0.1:8000";

  pplx::task<web::http::http_response> makeRequest(const std::string & request_string);
};
