#pragma once

#include <string>

#include <cpprest/json.h>


class Recipient {
public:
  explicit Recipient(const std::string & name, const std::string & telegram_chat_id, const std::string & matrix_id);
  explicit Recipient(const web::json::value & recipient_json);
  const std::string & getName() const noexcept;
  const std::string & getTelegramChatId() const noexcept;
  const std::string & getMatrixId() const noexcept;

private:
  std::string name_;
  std::string telegram_chat_id_;
  std::string matrix_id_;
};