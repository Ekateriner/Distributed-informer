#pragma once

#include <cpprest/http_msg.h>

namespace network {

using web::http::status_codes;

class Handler {
 public:
  virtual ~Handler() = 0;

  virtual void handleGet(web::http::http_request request) { request.reply(status_codes::NotFound); }
  virtual void handlePost(web::http::http_request request) { request.reply(status_codes::NotFound); }
  virtual void handlePut(web::http::http_request request) { request.reply(status_codes::NotFound); }
  virtual void handleHead(web::http::http_request request) { request.reply(status_codes::NotFound); }
  virtual void handleDelete(web::http::http_request request) { request.reply(status_codes::NotFound); }
  virtual void handleConnect(web::http::http_request request) { request.reply(status_codes::NotFound); }
  virtual void handleOptions(web::http::http_request request) { request.reply(status_codes::NotFound); }
  virtual void handleTrace(web::http::http_request request) { request.reply(status_codes::NotFound); }
  virtual void handlePatch(web::http::http_request request) { request.reply(status_codes::NotFound); }
  virtual void handleMerge(web::http::http_request request) { request.reply(status_codes::NotFound); }
};

inline Handler::~Handler() { }

} // namespace network
