#pragma once

#include <ctime>
#include <memory>
#include <vector>
#include <unordered_set>

#include "alert.pb.h"
#include "delivery_rule.h"
#include "filter_predicates.h"

using alert::FilterStatus;

class BaseDeliveryRuleDecorator : public virtual DeliveryRule {
 public:
  explicit BaseDeliveryRuleDecorator(std::shared_ptr<DeliveryRule> rule);

  ~BaseDeliveryRuleDecorator() override = 0;

  void filterAlerts(std::vector<alert::Alert>& alerts) const override;

 protected:
  std::shared_ptr<DeliveryRule> wrappee_rule_;
};


class SlowModeDecorator : public BaseDeliveryRuleDecorator {
 public:
  SlowModeDecorator(std::shared_ptr<DeliveryRule> rule, size_t silent_interval);

  ~SlowModeDecorator() override;

  void filterAlerts(std::vector<alert::Alert>& alerts) const override;

 private:
  bool isSilent() const;

 private:
  const size_t silent_interval_;
  mutable std::time_t last_delivery_time_{0};

  static const std::unordered_set<FilterStatus> DELAYABLE;
};


class FilterModeDecorator : public BaseDeliveryRuleDecorator {
 public:
  FilterModeDecorator(std::shared_ptr<DeliveryRule> rule, std::vector<std::shared_ptr<FilterPredicate>> predicates);
  FilterModeDecorator(std::shared_ptr<DeliveryRule> rule, std::shared_ptr<FilterPredicate> predicate);

  ~FilterModeDecorator() override;

  void filterAlerts(std::vector<alert::Alert>& alerts) const override;

 private:
  const std::vector<std::shared_ptr<FilterPredicate>> predicates_;

  static const std::unordered_set<FilterStatus> IGNORABLE;
};


class ExceptModeDecorator : public BaseDeliveryRuleDecorator {
 public:
  ExceptModeDecorator(std::shared_ptr<DeliveryRule> rule, std::vector<std::shared_ptr<FilterPredicate>> predicates);
  ExceptModeDecorator(std::shared_ptr<DeliveryRule> rule, std::shared_ptr<FilterPredicate> predicate);

  ~ExceptModeDecorator() override;

  void filterAlerts(std::vector<alert::Alert>& alerts) const override;

 private:
  const std::vector<std::shared_ptr<FilterPredicate>> predicates_;

  static const std::unordered_set<FilterStatus> EXCEPTABLE;
};
