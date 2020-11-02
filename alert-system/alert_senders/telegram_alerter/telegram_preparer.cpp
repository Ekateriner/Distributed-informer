#include <ctime>
#include <memory>

#include "alert.pb.h"
#include "telegram_preparer.h"

std::shared_ptr<PreparedAlert> TelegramPreparer::prepare(const alert::Alert& alert) const {
  char buffer[sizeof "YYYY-MM-DD HH:MM:SS"];
  std::time_t ts(alert.time().seconds());
  std::strftime(buffer, sizeof(buffer), "%F %T", std::localtime(&ts));
  return std::make_shared<TelegramPreparedAlert>("Alert! At " + std::string(buffer) + '\n' + alert.DebugString());
}
