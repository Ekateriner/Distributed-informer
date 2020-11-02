#include "basic_controller.h"
#include "network_utils.h"

namespace network {

using web::uri;
using web::uri_builder;

BasicController::BasicController(const std::string &uri_string) {
  uri endpointURI(uri_string);
  uri_builder endpointBuilder;

  endpointBuilder.set_scheme(endpointURI.scheme());
  if (endpointURI.host() == "host_auto_ip4") {
    endpointBuilder.set_host(NetworkUtils::hostIP4());
  } else if (endpointURI.host() == "host_auto_ip6") {
    endpointBuilder.set_host(NetworkUtils::hostIP6());
  } else if (endpointURI.host() == "0.0.0.0") {
    endpointBuilder.set_host("0.0.0.0");
  }
  endpointBuilder.set_port(endpointURI.port());
  endpointBuilder.set_path(endpointURI.path());

  listener_ = http_listener(endpointBuilder.to_uri());
}

std::string BasicController::endpoint() const{
  return listener_.uri().to_string();
}

pplx::task<void> BasicController::accept() {
  initRestOpHandlers();
  return listener_.open();
}

pplx::task<void> BasicController::shutdown() {
  return listener_.close();
}

std::string BasicController::requestPath(const web::http::http_request &message) const {
  return uri::decode(message.relative_uri().path());
}

} // namespace network