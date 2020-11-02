#include <iostream>
#include <vector>

#include "alert_parser.h"

const std::unordered_set<std::string> AlertParser::REQUIRED_FIELDS({"time"});
const std::unordered_set<std::string> AlertParser::OPTIONAL_FIELDS({
  "duration", "level", "previousLevel", "data"
});


AlertParser::AlertParser()
    : field_parsers_({
                         {"time", new TimeFieldParser()},
                         {"duration", new DurationFieldParser()},
                         {"level", new LevelFieldParser()},
                         {"previousLevel", new PreviousLevelFieldParser()},
                         {"data", new SeriesFieldParser()}
    }) {

}

AlertParser::~AlertParser() {
  for (auto parser : field_parsers_) {
    delete parser.second;
  }
}

alert::Alert AlertParser::parseJson(const web::json::value &json) const {
  alert::Alert alert;
  try {
    for (const auto& required_field : REQUIRED_FIELDS) {
      parseRequiredField(required_field, json, alert);
    }

    for (const auto& optional_field : OPTIONAL_FIELDS) {
      parseField(optional_field, json, alert);
    }
  } catch (const std::exception& e) {
    std::cerr << e.what() << std::endl;
  }

  return alert;
}

void AlertParser::parseField(const std::string &field_name, const web::json::value &from, alert::Alert &to) const {
  if (field_parsers_.find(field_name) == field_parsers_.end()) {
    throw std::runtime_error("Field " + field_name + " is not supported");
  } else if (from.has_field(field_name)) {
    field_parsers_.at(field_name)->parseField(from, to);
  }
}

void AlertParser::parseRequiredField(const std::string &field_name,
                                     const web::json::value &from,
                                     alert::Alert &to) const {
  if (!from.has_field(field_name)) {
    throw std::runtime_error("Missed required field: " + field_name);
  } else {
    parseField(field_name, from, to);
  }
}
