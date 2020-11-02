#include <ctime>
#include <iomanip>
#include <vector>
#include <unordered_map>

#include <google/protobuf/duration.pb.h>
#include <google/protobuf/timestamp.pb.h>

#include "field_parsers.h"

static const std::unordered_map<std::string, alert::Level> STRINGS_TO_LEVELS({
  {"INFO", alert::INFO},
  {"WARN", alert::WARN},
  {"CRIT", alert::CRIT}
});

size_t convertTime(const std::string &time_string) {
  std::tm ts = {};
  std::istringstream ss(time_string);
  ss >> std::get_time(&ts, "%Y-%m-%dT%TZ");
  if (ss.fail()) {
    throw std::runtime_error("Failed to parse time:" + time_string);
  } else {
    return std::mktime(&ts);
  }
}


FieldParser::~FieldParser() {

}


TimeFieldParser::~TimeFieldParser() {

}

void TimeFieldParser::parseField(const web::json::value &from, alert::Alert &to) const {
  auto ts = new google::protobuf::Timestamp();
  try {
    ts->set_seconds(convertTime(from.at("time").as_string()));
    to.set_allocated_time(ts);
  } catch (...) {
    delete ts;
    throw;
  }
}


DurationFieldParser::~DurationFieldParser() {

}

void DurationFieldParser::parseField(const web::json::value &from, alert::Alert &to) const {
  auto duration = new google::protobuf::Duration();
  try {
    duration->set_seconds(from.at("duration").as_integer());
    to.set_allocated_duration(duration);
  } catch (...) {
    delete duration;
    throw;
  }
}


LevelFieldParser::~LevelFieldParser() {

}

void LevelFieldParser::parseField(const web::json::value &from, alert::Alert &to) const {
  to.set_level(STRINGS_TO_LEVELS.at(from.at("level").as_string()));
}


PreviousLevelFieldParser::~PreviousLevelFieldParser() {

}

void PreviousLevelFieldParser::parseField(const web::json::value &from, alert::Alert &to) const {
  to.set_previous_level(STRINGS_TO_LEVELS.at(from.at("previousLevel").as_string()));
}


SeriesFieldParser::~SeriesFieldParser() {

}

void SeriesFieldParser::parseField(const web::json::value &from, alert::Alert &to) const {
  if (!from.at("data").has_field("series")) {
    throw std::runtime_error("Field \"data\" has not nested field \"series\"");
  }

  for (const auto& series_json : from.at("data").at("series").as_array()) {
    addSeries(series_json, to);
  }
}

void SeriesFieldParser::addSeries(const web::json::value &series_json, alert::Alert &to) const {
  auto series = to.add_series();
  if (series_json.has_field("name")) {
    series->set_name(series_json.at("name").as_string());
  }

  if (series_json.has_field("tags")) {
    const auto &tags_obj = series_json.at("tags").as_object();
    for (const auto &tag : tags_obj) {
      series->mutable_tags()->operator[](tag.first) = tag.second.as_string();
    }
  }

  if (series_json.has_field("columns") && series_json.has_field("values")) {
    std::vector<std::string> metric_names = extractMetricNames(series_json);
    for (const auto& values_set : series_json.at("values").as_array()) {
      addMetricValues(series, metric_names, values_set);
    }
  }
}

std::vector<std::string> SeriesFieldParser::extractMetricNames(const web::json::value &series_json) const {
  std::vector<std::string> metric_names;
  for (const auto& metric_name : series_json.at("columns").as_array()) {
    metric_names.push_back(metric_name.as_string());
  }
  return metric_names;
}

void SeriesFieldParser::addMetricValues(alert::Series *series,
                                        std::vector<std::string> metric_names,
                                        const web::json::value &values_set) const {
  auto new_metric = series->add_metrics();
  const auto& values_array = values_set.as_array();
  for (size_t i = 0; i < values_array.size(); ++i) {
    if (metric_names[i] == "time") {
      auto ts = new google::protobuf::Timestamp();
      try {
        ts->set_seconds(convertTime(values_array.at(i).as_string()));
        new_metric->set_allocated_time(ts);
      } catch (...) {
        delete ts;
        throw;
      }
    } else {
      new_metric->mutable_values()->operator[](metric_names[i]) = values_array.at(i).as_double();
    }
  }
}
