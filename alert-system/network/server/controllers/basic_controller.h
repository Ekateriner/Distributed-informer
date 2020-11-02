#pragma once

#include <string>
#include <vector>

#include <cpprest/http_listener.h>
#include <cpprest/uri.h>
#include <cpprest/uri_builder.h>
#include <cpprest/http_msg.h>

namespace network {

using web::http::http_request;

using web::http::experimental::listener::http_listener;

class BasicController {
 public:
  explicit BasicController(const std::string &uri_string);

  std::string endpoint() const;
  pplx::task<void> accept();
  pplx::task<void> shutdown();

  virtual void initRestOpHandlers() = 0;

  std::string requestPath(const http_request &message) const;

 protected:
  http_listener listener_;
};

} // namespace network
