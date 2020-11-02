#include <ctime>
#include <memory>

#include "alert.pb.h"
#include "matrix_prepared_alert.h"
#include "matrix_preparer.h"

MatrixPreparer::MatrixPreparer() = default;

std::shared_ptr<PreparedAlert> MatrixPreparer::prepare(const alert::Alert& alert) const {
  char buffer[sizeof "YYYY-MM-DD HH:MM:SS"];
  std::time_t ts(alert.time().seconds());
  std::strftime(buffer, sizeof(buffer), "%F %T", std::localtime(&ts));
  return std::make_shared<MatrixPreparedAlert>("Alert! At " + std::string(buffer) + '\n' + alert.DebugString());
}