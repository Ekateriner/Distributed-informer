#include "delivery_rule_decorators.h"

BaseDeliveryRuleDecorator::BaseDeliveryRuleDecorator(std::shared_ptr<DeliveryRule> rule)
    : wrappee_rule_(rule) {

}

BaseDeliveryRuleDecorator::~BaseDeliveryRuleDecorator() {

}

void BaseDeliveryRuleDecorator::filterAlerts(std::vector<alert::Alert> &alerts) const {
  wrappee_rule_->filterAlerts(alerts);
}

const std::unordered_set<FilterStatus> SlowModeDecorator::DELAYABLE({
                                                                        FilterStatus::UNKNOWN, FilterStatus::TO_BE_SENT
                                                                    });

SlowModeDecorator::SlowModeDecorator(std::shared_ptr<DeliveryRule> rule, size_t silent_interval)
    : BaseDeliveryRuleDecorator(rule)
    , silent_interval_(silent_interval) {

}

SlowModeDecorator::~SlowModeDecorator() {

}

void SlowModeDecorator::filterAlerts(std::vector<alert::Alert> &alerts) const {
  if (isSilent()) {
    for (auto& alert : alerts) {
      if (DELAYABLE.find(alert.filter_status()) != DELAYABLE.end()) {
        alert.set_filter_status(FilterStatus::DELAYED);
      }
    }
  }

  BaseDeliveryRuleDecorator::filterAlerts(alerts);

  for (const auto& alert : alerts) {
    if (alert.filter_status() == FilterStatus::TO_BE_SENT) {
      last_delivery_time_ = std::time(nullptr);
      break;
    }
  }
}

bool SlowModeDecorator::isSilent() const {
  return std::time(nullptr) - last_delivery_time_ < silent_interval_;
}

const std::unordered_set<FilterStatus> FilterModeDecorator::IGNORABLE({
                                                                          FilterStatus::UNKNOWN,
                                                                          FilterStatus::TO_BE_SENT
                                                                      });

FilterModeDecorator::FilterModeDecorator(std::shared_ptr<DeliveryRule> rule,
                                         std::vector<std::shared_ptr<FilterPredicate>> predicates)
    : BaseDeliveryRuleDecorator(rule), predicates_(std::move(predicates)) {

}

FilterModeDecorator::FilterModeDecorator(std::shared_ptr<DeliveryRule> rule,
                                         std::shared_ptr<FilterPredicate> predicate)
    : BaseDeliveryRuleDecorator(rule), predicates_(1, predicate) {

}

FilterModeDecorator::~FilterModeDecorator() {

}

void FilterModeDecorator::filterAlerts(std::vector<alert::Alert> &alerts) const {
  for (auto& alert : alerts) {
    if (IGNORABLE.find(alert.filter_status()) != IGNORABLE.end()) {
      for (const auto& predicate : predicates_) {
        if (predicate->isTrue(alert)) {
          alert.set_filter_status(FilterStatus::IGNORED);
          break;
        }
      }
    }
  }

  BaseDeliveryRuleDecorator::filterAlerts(alerts);
}


const std::unordered_set<FilterStatus> ExceptModeDecorator::EXCEPTABLE({
                                                                          FilterStatus::UNKNOWN,
                                                                          FilterStatus::IGNORED,
                                                                          FilterStatus::DELAYED
                                                                      });

ExceptModeDecorator::ExceptModeDecorator(std::shared_ptr<DeliveryRule> rule,
                                         std::vector<std::shared_ptr<FilterPredicate>> predicates)
    : BaseDeliveryRuleDecorator(rule), predicates_(std::move(predicates)) {

}

ExceptModeDecorator::ExceptModeDecorator(std::shared_ptr<DeliveryRule> rule,
                                         std::shared_ptr<FilterPredicate> predicate)
    : BaseDeliveryRuleDecorator(rule), predicates_(1, predicate) {

}

ExceptModeDecorator::~ExceptModeDecorator() {

}

void ExceptModeDecorator::filterAlerts(std::vector<alert::Alert> &alerts) const {
  BaseDeliveryRuleDecorator::filterAlerts(alerts);

  for (auto& alert : alerts) {
    if (EXCEPTABLE.find(alert.filter_status()) != EXCEPTABLE.end()) {
      for (const auto& predicate : predicates_) {
        if (predicate->isTrue(alert)) {
          alert.set_filter_status(FilterStatus::TO_BE_SENT);
          break;
        }
      }
    }
  }
}
