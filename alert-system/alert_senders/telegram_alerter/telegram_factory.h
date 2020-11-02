#pragma once

#include <memory>

#include "abstract_sender.h"
#include <telegram_sender.h>
#include <telegram_preparer.h>

class TelegramFactory : public Factory {
 public:
  TelegramFactory();

  std::shared_ptr<Sender> createSender(const std::string &chat_id) const override;
  std::shared_ptr<Preparer> createPreparer() const override;
};
