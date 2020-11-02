#include "filter_predicates.h"

FilterPredicate::~FilterPredicate() {

}

NegationFilterPredicate::NegationFilterPredicate(std::shared_ptr<FilterPredicate> predicate)
    : operand_predicate_(predicate) {

}

NegationFilterPredicate::~NegationFilterPredicate() {

}

bool NegationFilterPredicate::isTrue(const alert::Alert &alert) const {
  return !operand_predicate_->isTrue(alert);
}

AndFilterPredicate::AndFilterPredicate(std::shared_ptr<FilterPredicate> first_predicate,
                                       std::shared_ptr<FilterPredicate> second_predicate)
    : first_operand_predicate_(first_predicate)
    , second_operand_predicate_(second_predicate) {

}

AndFilterPredicate::~AndFilterPredicate() {

}

bool AndFilterPredicate::isTrue(const alert::Alert &alert) const {
  return first_operand_predicate_->isTrue(alert) && second_operand_predicate_->isTrue(alert);
}

OrFilterPredicate::OrFilterPredicate(std::shared_ptr<FilterPredicate> first_predicate,
                                     std::shared_ptr<FilterPredicate> second_predicate)
    : first_operand_predicate_(first_predicate)
    , second_operand_predicate_(second_predicate) {

}

OrFilterPredicate::~OrFilterPredicate() {

}

bool OrFilterPredicate::isTrue(const alert::Alert &alert) const {
  return first_operand_predicate_->isTrue(alert) || second_operand_predicate_->isTrue(alert);
}

EqualsTagPredicate::EqualsTagPredicate(const std::string &tag, const std::string &value)
    : tag_(tag), value_(value) {

}

EqualsTagPredicate::~EqualsTagPredicate() {

}

bool EqualsTagPredicate::isTrue(const alert::Alert &alert) const {
  for (const auto& series : alert.series()) {
    if (series.tags().contains(tag_) && series.tags().at(tag_) == value_) {
      return true;
    }
  }

  return false;
}

NotEqualsTagPredicate::NotEqualsTagPredicate(const std::string &tag, const std::string &value)
    : tag_(tag), value_(value) {

}

NotEqualsTagPredicate::~NotEqualsTagPredicate() {

}

bool NotEqualsTagPredicate::isTrue(const alert::Alert &alert) const {
  for (const auto& series : alert.series()) {
    if (series.tags().contains(tag_) && series.tags().at(tag_) != value_) {
      return true;
    }
  }

  return false;
}

HasTagPredicate::HasTagPredicate(const std::string &tag) : tag_(tag) {

}

HasTagPredicate::~HasTagPredicate() {

}

bool HasTagPredicate::isTrue(const alert::Alert &alert) const {
  for (const auto& series : alert.series()) {
    if (series.tags().contains(tag_)) {
      return true;
    }
  }

  return false;
}

EqualsMetricPredicate::EqualsMetricPredicate(const std::string &metric_name, double value)
    : metric_name_(metric_name), value_(value) {

}

EqualsMetricPredicate::~EqualsMetricPredicate() {

}

bool EqualsMetricPredicate::isTrue(const alert::Alert &alert) const {
  for (const auto& series : alert.series()) {
    for (const auto& metric : series.metrics()) {
      if (metric.values().contains(metric_name_) && metric.values().at(metric_name_) == value_) {
        return true;
      }
    }
  }

  return false;
}

LessMetricPredicate::LessMetricPredicate(const std::string &metric_name, double value)
    : metric_name_(metric_name), threshold_value_(value) {

}

LessMetricPredicate::~LessMetricPredicate() {

}

bool LessMetricPredicate::isTrue(const alert::Alert &alert) const {
  for (const auto& series : alert.series()) {
    for (const auto& metric : series.metrics()) {
      if (metric.values().contains(metric_name_) && metric.values().at(metric_name_) < threshold_value_) {
        return true;
      }
    }
  }

  return false;
}

GreaterMetricPredicate::GreaterMetricPredicate(const std::string &metric_name, double value)
    : metric_name_(metric_name), threshold_value_(value) {


}

GreaterMetricPredicate::~GreaterMetricPredicate() {

}

bool GreaterMetricPredicate::isTrue(const alert::Alert &alert) const {
  for (const auto& series : alert.series()) {
    for (const auto& metric : series.metrics()) {
      if (metric.values().contains(metric_name_) && metric.values().at(metric_name_) > threshold_value_) {
        return true;
      }
    }
  }

  return false;
}

NotEqualsMetricPredicate::NotEqualsMetricPredicate(const std::string &metric_name, double value)
    : metric_name_(metric_name), value_(value) {

}

NotEqualsMetricPredicate::~NotEqualsMetricPredicate() {

}

bool NotEqualsMetricPredicate::isTrue(const alert::Alert &alert) const {
  for (const auto& series : alert.series()) {
    for (const auto& metric : series.metrics()) {
      if (metric.values().contains(metric_name_) && metric.values().at(metric_name_) != value_) {
        return true;
      }
    }
  }

  return false;
}

LessOrEqualsMetricPredicate::LessOrEqualsMetricPredicate(const std::string &metric_name, double value)
    : metric_name_(metric_name), threshold_value_(value) {

}

LessOrEqualsMetricPredicate::~LessOrEqualsMetricPredicate() {

}

bool LessOrEqualsMetricPredicate::isTrue(const alert::Alert &alert) const {
  for (const auto& series : alert.series()) {
    for (const auto& metric : series.metrics()) {
      if (metric.values().contains(metric_name_) && metric.values().at(metric_name_) <= threshold_value_) {
        return true;
      }
    }
  }

  return false;
}

GreaterOrEqualsMetricPredicate::GreaterOrEqualsMetricPredicate(const std::string &metric_name, double value)
    : metric_name_(metric_name), threshold_value_(value) {


}

GreaterOrEqualsMetricPredicate::~GreaterOrEqualsMetricPredicate() {

}

bool GreaterOrEqualsMetricPredicate::isTrue(const alert::Alert &alert) const {
  for (const auto& series : alert.series()) {
    for (const auto& metric : series.metrics()) {
      if (metric.values().contains(metric_name_) && metric.values().at(metric_name_) >= threshold_value_) {
        return true;
      }
    }
  }

  return false;
}

HasMetricPredicate::HasMetricPredicate(const std::string &metric_name) : metric_name_(metric_name) {

}

HasMetricPredicate::~HasMetricPredicate() {

}

bool HasMetricPredicate::isTrue(const alert::Alert &alert) const {
  for (const auto& series : alert.series()) {
    for (const auto& metric : series.metrics()) {
      if (metric.values().contains(metric_name_)) {
        return true;
      }
    }
  }

  return false;
}

EqualsLevelPredicate::EqualsLevelPredicate(alert::Level level) : level_(level) {

}

EqualsLevelPredicate::~EqualsLevelPredicate() {

}

bool EqualsLevelPredicate::isTrue(const alert::Alert &alert) const {
  return alert.has_level() && alert.level() == level_;
}

EqualsSubscriptionIdPredicate::EqualsSubscriptionIdPredicate(const std::string &value) : value_(value) {

}

EqualsSubscriptionIdPredicate::~EqualsSubscriptionIdPredicate() {

}

bool EqualsSubscriptionIdPredicate::isTrue(const alert::Alert &alert) const {
  for (const auto& series : alert.series()) {
    if (series.has_subscription_id() && series.subscription_id() == value_) {
      return true;
    }
  }

  return false;
}


NotEqualsSubscriptionIdPredicate::NotEqualsSubscriptionIdPredicate(const std::string &value) : value_(value) {

}

NotEqualsSubscriptionIdPredicate::~NotEqualsSubscriptionIdPredicate() {

}

bool NotEqualsSubscriptionIdPredicate::isTrue(const alert::Alert &alert) const {
  for (const auto& series : alert.series()) {
    if (series.has_subscription_id() && series.subscription_id() != value_) {
      return true;
    }
  }

  return false;
}
