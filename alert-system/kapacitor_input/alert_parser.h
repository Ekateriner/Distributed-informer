#pragma once

#include <string>
#include <unordered_map>
#include <unordered_set>

#include <cpprest/json.h>

#include "alert.pb.h"
#include "field_parsers.h"

class AlertParser {
 public:
  AlertParser();
  ~AlertParser();

  alert::Alert parseJson(const web::json::value& json) const;

 private:
  void parseField(const std::string &field_name, const web::json::value &from, alert::Alert &to) const;
  void parseRequiredField(const std::string &field_name, const web::json::value &from, alert::Alert &to) const;

 private:
  const std::unordered_map<std::string, FieldParser*> field_parsers_;

  static const std::unordered_set<std::string> REQUIRED_FIELDS;
  static const std::unordered_set<std::string> OPTIONAL_FIELDS;
};
