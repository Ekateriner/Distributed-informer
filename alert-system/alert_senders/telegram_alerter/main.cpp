#include <google/protobuf/timestamp.pb.h>

#include "alert.pb.h"
#include "telegram_factory.h"

int main() {
  TelegramFactory factory;
  auto preparer = factory.createPreparer();
  auto sender = factory.createSender("495925142");
  alert::Alert alert;
  alert.set_allocated_time(new google::protobuf::Timestamp());
  alert.set_level(alert::WARN);
  auto prepared_alert = preparer->prepare(alert);
  sender->send(prepared_alert);
  return 0;
}
