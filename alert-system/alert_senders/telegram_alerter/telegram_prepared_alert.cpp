#include <telegram_prepared_alert.h>

std::string TelegramPreparedAlert::getText() const {
  return text_;
}

TelegramPreparedAlert::TelegramPreparedAlert(const std::string &text) :
    text_(text) {

}
