#pragma once

#include <string>

#include "abstract_sender.h"

class MatrixPreparedAlert : public PreparedAlert {
 public:
  explicit MatrixPreparedAlert(const std::string &text);
  std::string getText() const;

 private:
  std::string text_;
};

