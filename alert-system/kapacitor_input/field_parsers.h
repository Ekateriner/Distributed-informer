#pragma once

#include <string>

#include <cpprest/json.h>

#include "alert.pb.h"

size_t convertTime(const std::string& time_string);

class FieldParser {
 public:
  virtual ~FieldParser() = 0;

  virtual void parseField(const web::json::value& from, alert::Alert& to) const = 0;
};


class TimeFieldParser : public FieldParser {
  ~TimeFieldParser() override;

  void parseField(const web::json::value& from, alert::Alert& to) const override;
};


class DurationFieldParser : public FieldParser {
  ~DurationFieldParser() override;

  void parseField(const web::json::value& from, alert::Alert& to) const override;
};


class LevelFieldParser : public FieldParser {
  ~LevelFieldParser() override;

  void parseField(const web::json::value& from, alert::Alert& to) const override;
};


class PreviousLevelFieldParser : public FieldParser {
  ~PreviousLevelFieldParser() override;

  void parseField(const web::json::value& from, alert::Alert& to) const override;
};


class SeriesFieldParser : public FieldParser {
  ~SeriesFieldParser() override;

  void parseField(const web::json::value& from, alert::Alert& to) const override;

 private:
  void addSeries(const web::json::value &series_json, alert::Alert &to) const;
  std::vector<std::string> extractMetricNames(const web::json::value &series_json) const;
  void addMetricValues(alert::Series *series,
                       std::vector<std::string> metric_names,
                       const web::json::value &values_set) const;
};
