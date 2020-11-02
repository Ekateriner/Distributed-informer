#pragma once

#include <vector>

#include "alert.pb.h"
#include "delivery_rule.h"

class DefaultDeliveryRule : public DeliveryRule {
 public:
  ~DefaultDeliveryRule() override;

  void filterAlerts(std::vector<alert::Alert>& alerts) const override;
};
