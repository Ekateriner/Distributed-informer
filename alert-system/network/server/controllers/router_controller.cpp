#include "router_controller.h"

namespace network {

using web::http::methods;
using web::http::status_codes;

RouterController::RouterController(const std::string &uri_string
                                 , std::initializer_list<std::pair<const std::string, Handler*>> handlers)
                                 : BasicController(uri_string), handlers_(handlers) { }

RouterController::~RouterController() {
  for (const auto& handler : handlers_) {
    delete handler.second;
  }
}

void RouterController::initRestOpHandlers() {
  listener_.support(methods::GET, std::bind(&RouterController::handleGet, this, std::placeholders::_1));
  listener_.support(methods::POST, std::bind(&RouterController::handlePost, this, std::placeholders::_1));
  listener_.support(methods::PUT, std::bind(&RouterController::handlePut, this, std::placeholders::_1));
  listener_.support(methods::HEAD, std::bind(&RouterController::handleHead, this, std::placeholders::_1));
  listener_.support(methods::DEL, std::bind(&RouterController::handleDelete, this, std::placeholders::_1));
  listener_.support(methods::CONNECT, std::bind(&RouterController::handleConnect, this, std::placeholders::_1));
  listener_.support(methods::OPTIONS, std::bind(&RouterController::handleOptions, this, std::placeholders::_1));
  listener_.support(methods::TRCE, std::bind(&RouterController::handleTrace, this, std::placeholders::_1));
  listener_.support(methods::PATCH, std::bind(&RouterController::handlePatch, this, std::placeholders::_1));
  listener_.support(methods::MERGE, std::bind(&RouterController::handleMerge, this, std::placeholders::_1));
}

void RouterController::handleGet(http_request message) {
  std::string api_path = requestPath(message);
  try {
    getHandlerByPath(api_path)->handleGet(message);
  } catch (const std::runtime_error& e) {
    message.reply(status_codes::NotFound);
    std::cerr << e.what() << std::endl;
  }
}

void RouterController::handlePost(http_request message) {
  std::string api_path = requestPath(message);
  try {
    getHandlerByPath(api_path)->handlePost(message);
  } catch (const std::runtime_error& e) {
    message.reply(status_codes::NotFound);
    std::cerr << e.what() << std::endl;
  }
}

void RouterController::handlePut(http_request message) {
  std::string api_path = requestPath(message);
  try {
    getHandlerByPath(api_path)->handlePut(message);
  } catch (const std::runtime_error& e) {
    message.reply(status_codes::NotFound);
    std::cerr << e.what() << std::endl;
  }
}

void RouterController::handleHead(http_request message) {
  std::string api_path = requestPath(message);
  try {
    getHandlerByPath(api_path)->handleHead(message);
  } catch (const std::runtime_error& e) {
    message.reply(status_codes::NotFound);
    std::cerr << e.what() << std::endl;
  }
}

void RouterController::handleDelete(http_request message) {
  std::string api_path = requestPath(message);
  try {
    getHandlerByPath(api_path)->handleDelete(message);
  } catch (const std::runtime_error& e) {
    message.reply(status_codes::NotFound);
    std::cerr << e.what() << std::endl;
  }
}

void RouterController::handleConnect(http_request message) {
  std::string api_path = requestPath(message);
  try {
    getHandlerByPath(api_path)->handleConnect(message);
  } catch (const std::runtime_error& e) {
    message.reply(status_codes::NotFound);
    std::cerr << e.what() << std::endl;
  }
}

void RouterController::handleOptions(http_request message) {
  std::string api_path = requestPath(message);
  try {
    getHandlerByPath(api_path)->handleOptions(message);
  } catch (const std::runtime_error& e) {
    message.reply(status_codes::NotFound);
    std::cerr << e.what() << std::endl;
  }
}

void RouterController::handleTrace(http_request message) {
  std::string api_path = requestPath(message);
  try {
    getHandlerByPath(api_path)->handleTrace(message);
  } catch (const std::runtime_error& e) {
    message.reply(status_codes::NotFound);
    std::cerr << e.what() << std::endl;
  }
}

void RouterController::handlePatch(http_request message) {
  std::string api_path = requestPath(message);
  try {
    getHandlerByPath(api_path)->handlePatch(message);
  } catch (const std::runtime_error& e) {
    message.reply(status_codes::NotFound);
    std::cerr << e.what() << std::endl;
  }
}

void RouterController::handleMerge(http_request message) {
  std::string api_path = requestPath(message);
  try {
    getHandlerByPath(api_path)->handleMerge(message);
  } catch (const std::runtime_error& e) {
    message.reply(status_codes::NotFound);
    std::cerr << e.what() << std::endl;
  }
}

Handler* RouterController::getHandlerByPath(const std::string & api_path) {
  for (const auto& handler : handlers_) {
    if (handler.first == api_path) {
      return handler.second;
    }
  }

  throw std::runtime_error("No such path defined");
}

} // namespace network
