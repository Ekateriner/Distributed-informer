#pragma once

#include <memory>
#include <string>

#include "alert.pb.h"

class FilterPredicate {
 public:
  virtual ~FilterPredicate() = 0;

  virtual bool isTrue(const alert::Alert& alert) const = 0;
};


class NegationFilterPredicate : public FilterPredicate {
 public:
  explicit NegationFilterPredicate(std::shared_ptr<FilterPredicate> predicate);

  ~NegationFilterPredicate() override;

  bool isTrue(const alert::Alert& alert) const override;

 private:
  const std::shared_ptr<FilterPredicate> operand_predicate_;
};


class AndFilterPredicate : public FilterPredicate {
 public:
  AndFilterPredicate(std::shared_ptr<FilterPredicate> first_predicate,
                     std::shared_ptr<FilterPredicate> second_predicate);

  ~AndFilterPredicate() override;

  bool isTrue(const alert::Alert& alert) const override;

 private:
  const std::shared_ptr<FilterPredicate> first_operand_predicate_;
  const std::shared_ptr<FilterPredicate> second_operand_predicate_;
};


class OrFilterPredicate : public FilterPredicate {
 public:
  OrFilterPredicate(std::shared_ptr<FilterPredicate> first_predicate,
  std::shared_ptr<FilterPredicate> second_predicate);

  ~OrFilterPredicate() override;

  bool isTrue(const alert::Alert& alert) const override;

 private:
  const std::shared_ptr<FilterPredicate> first_operand_predicate_;
  const std::shared_ptr<FilterPredicate> second_operand_predicate_;
};


class EqualsTagPredicate : public FilterPredicate {
 public:
  EqualsTagPredicate(const std::string& tag, const std::string& value);

  ~EqualsTagPredicate() override;

  bool isTrue(const alert::Alert& alert) const override;

 private:
  const std::string tag_;
  const std::string value_;
};


class NotEqualsTagPredicate : public FilterPredicate {
 public:
  NotEqualsTagPredicate(const std::string& tag, const std::string& value);

  ~NotEqualsTagPredicate() override;

  bool isTrue(const alert::Alert& alert) const override;

 private:
  const std::string tag_;
  const std::string value_;
};


class HasTagPredicate : public FilterPredicate {
 public:
  explicit HasTagPredicate(const std::string& tag);

  ~HasTagPredicate() override;

  bool isTrue(const alert::Alert& alert) const override;

 private:
  const std::string tag_;
};


class EqualsMetricPredicate : public FilterPredicate {
 public:
  EqualsMetricPredicate(const std::string& metric_name, double value);

  ~EqualsMetricPredicate() override;

  bool isTrue(const alert::Alert& alert) const override;

 private:
  const std::string metric_name_;
  const double value_;
};


class NotEqualsMetricPredicate : public FilterPredicate {
 public:
  NotEqualsMetricPredicate(const std::string& metric_name, double value);

  ~NotEqualsMetricPredicate() override;

  bool isTrue(const alert::Alert& alert) const override;

 private:
  const std::string metric_name_;
  const double value_;
};


class LessMetricPredicate : public FilterPredicate {
 public:
  LessMetricPredicate(const std::string& metric_name, double value);

  ~LessMetricPredicate() override;

  bool isTrue(const alert::Alert& alert) const override;

 private:
  const std::string metric_name_;
  const double threshold_value_;
};


class GreaterMetricPredicate : public FilterPredicate {
 public:
  GreaterMetricPredicate(const std::string& metric_name, double value);

  ~GreaterMetricPredicate() override;

  bool isTrue(const alert::Alert& alert) const override;

 private:
  const std::string metric_name_;
  const double threshold_value_;
};


class LessOrEqualsMetricPredicate : public FilterPredicate {
 public:
  LessOrEqualsMetricPredicate(const std::string& metric_name, double value);

  ~LessOrEqualsMetricPredicate() override;

  bool isTrue(const alert::Alert& alert) const override;

 private:
  const std::string metric_name_;
  const double threshold_value_;
};


class GreaterOrEqualsMetricPredicate : public FilterPredicate {
 public:
  GreaterOrEqualsMetricPredicate(const std::string& metric_name, double value);

  ~GreaterOrEqualsMetricPredicate() override;

  bool isTrue(const alert::Alert& alert) const override;

 private:
  const std::string metric_name_;
  const double threshold_value_;
};


class HasMetricPredicate : public FilterPredicate {
 public:
  explicit HasMetricPredicate(const std::string& metric_name);

  ~HasMetricPredicate() override;

  bool isTrue(const alert::Alert& alert) const override;

 private:
  const std::string metric_name_;
};


class EqualsLevelPredicate : public FilterPredicate {
 public:
  explicit EqualsLevelPredicate(alert::Level level);

  ~EqualsLevelPredicate() override;

  bool isTrue(const alert::Alert& alert) const override;

 private:
  const alert::Level level_;
};


class EqualsSubscriptionIdPredicate : public FilterPredicate {
 public:
  explicit EqualsSubscriptionIdPredicate(const std::string& value);

  ~EqualsSubscriptionIdPredicate() override;

  bool isTrue(const alert::Alert& alert) const override;

 private:
  const std::string value_;
};


class NotEqualsSubscriptionIdPredicate : public FilterPredicate {
 public:
  explicit NotEqualsSubscriptionIdPredicate(const std::string& value);

  ~NotEqualsSubscriptionIdPredicate() override;

  bool isTrue(const alert::Alert& alert) const override;

 private:
  const std::string value_;
};
