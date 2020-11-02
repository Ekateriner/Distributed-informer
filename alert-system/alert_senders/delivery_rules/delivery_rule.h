#pragma once

#include <vector>

#include "alert.pb.h"

class DeliveryRule {
 public:
  virtual ~DeliveryRule() = 0;

  virtual void filterAlerts(std::vector<alert::Alert>& alerts) const = 0;
};
