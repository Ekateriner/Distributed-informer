#include <google/protobuf/timestamp.pb.h>

#include "matrix_factory.h"
#include "alert.pb.h"

int main() {
  MatrixFactory factory;
  auto preparer = factory.createPreparer();
  auto sender = factory.createSender("!peaLsZdtyOLKogIHZJ:matrix.org");
  alert::Alert alert;
  alert.set_allocated_time(new google::protobuf::Timestamp());
  alert.set_level(alert::WARN);
  auto prepared_alert = preparer->prepare(alert);
  sender->send(prepared_alert);
  return 0;
}
