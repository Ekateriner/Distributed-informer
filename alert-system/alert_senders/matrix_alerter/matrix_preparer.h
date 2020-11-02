#pragma once

#include <memory>

#include "abstract_sender.h"
#include "alert.pb.h"

class MatrixPreparer : public Preparer {
 public:
  MatrixPreparer();
  std::shared_ptr<PreparedAlert> prepare(const alert::Alert& alert) const override;
};
