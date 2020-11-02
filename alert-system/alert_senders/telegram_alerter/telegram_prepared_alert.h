#pragma once

#include <string>

#include <abstract_sender.h>

class TelegramPreparedAlert: public PreparedAlert {
public:
    explicit TelegramPreparedAlert(const std::string& text);

    std::string getText() const;

private:
    std::string text_;
};