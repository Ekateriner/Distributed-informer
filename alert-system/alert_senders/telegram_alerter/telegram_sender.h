#pragma once

#include <cstdlib>
#include <memory>

#include <cpprest/http_client.h>
#include <cpprest/filestream.h>
#include <cpprest/uri.h>
#include <cpprest/json.h>
#include <pplx/pplxtasks.h>

#include "abstract_sender.h"
#include "telegram_sender.h"
#include "telegram_prepared_alert.h"

using web::uri_builder;
using web::http::methods;
using web::http::http_response;
using web::http::client::http_client;

class TelegramSender : public Sender {
 public:
  TelegramSender(const std::string &chat_id, const std::string &token) :
      chat_id_(chat_id), token_(token) {};

  explicit TelegramSender(const std::string &chat_id) : chat_id_(chat_id) {};

  void send(std::shared_ptr<PreparedAlert> prepared_alert) override;

 private:
  std::string chat_id_;
  std::string token_{std::getenv("TELEGRAM_BOT_TOKEN")};
};
