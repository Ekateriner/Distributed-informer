#include "default_delivery_rule.h"

DefaultDeliveryRule::~DefaultDeliveryRule() {

}

void DefaultDeliveryRule::filterAlerts(std::vector<alert::Alert> &alerts) const {
  for (auto& alert : alerts) {
    if (alert.filter_status() == alert::FilterStatus::UNKNOWN) {
      alert.set_filter_status(alert::FilterStatus::TO_BE_SENT);
    }
  }
}
