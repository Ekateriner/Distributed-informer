#pragma once

#include <memory>

#include "alert.pb.h"
#include "abstract_sender.h"
#include <telegram_prepared_alert.h>

class TelegramPreparer : public Preparer {
 public:
  TelegramPreparer() {};

  std::shared_ptr<PreparedAlert> prepare(const alert::Alert& alert) const override;
};
