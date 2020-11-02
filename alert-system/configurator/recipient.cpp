#include "recipient.h"

Recipient::Recipient(const std::string & name, const std::string & telegram_chat_id, const std::string & matrix_id)
  : name_(name)
  , telegram_chat_id_(telegram_chat_id)
  , matrix_id_(matrix_id)
  {}

Recipient::Recipient(const web::json::value & recipient_json) {
  web::json::object recipient = recipient_json.as_object();

  name_ = recipient["name"].as_string();
  telegram_chat_id_ = std::to_string(recipient["id_for_bot"].as_integer());
  matrix_id_ = recipient["id_for_matrix"].as_string();
}

const std::string & Recipient::getName() const noexcept {
  return name_;
}

const std::string & Recipient::getTelegramChatId() const noexcept {
  return telegram_chat_id_;
}

const std::string & Recipient::getMatrixId() const noexcept {
  return matrix_id_;
}