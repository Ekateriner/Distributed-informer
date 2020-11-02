#pragma once

#include <memory>
#include <string>

#include "abstract_sender.h"

class MatrixSender : public Sender {
 public:
  MatrixSender(const std::string &chat_id, const std::string &token) :
      chat_id_(chat_id), token_(token) {};

  explicit MatrixSender(const std::string &chat_id) : chat_id_(chat_id) {};

  void setToken(const std::string &token);

  const std::string &getToken() const;

  void send(std::shared_ptr<PreparedAlert> prepared_alert) override;

  void acquireToken();

 private:
  void reserveToken();

 private:
  std::string chat_id_;
  std::string token_ =
      "MDAxOGxvY2F0aW9uIG1hdHJpeC5vcmcKMDAxM2lkZW50aWZpZXIga2V5CjAwMTBjaWQgZ2VuID0gMQowMDI3Y2lkIHVzZXJfaWQgPSBAbmFyZWtpdG86bWF0cml4Lm9yZwowMDE2Y2lkIHR5cGUgPSBhY2Nlc3MKMDAyMWNpZCBub25jZSA9ICprVTp2cioyaUp1K1hTeDQKMDAyZnNpZ25hdHVyZSAltUACVTRGjM8oXfARpzoClL158YfFM4q6AfisXGOa9Qo";
};
