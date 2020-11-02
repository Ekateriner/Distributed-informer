#pragma once

#include <memory>
#include <string>

#include "abstract_sender.h"

class MatrixFactory : public Factory {
 public:
  MatrixFactory();
  std::shared_ptr<Sender> createSender(const std::string &chat_id) const override;
  std::shared_ptr<Preparer> createPreparer() const override;
};

