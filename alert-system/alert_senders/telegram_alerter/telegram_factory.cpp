#include <memory>
#include <string>

#include <telegram_factory.h>

TelegramFactory::TelegramFactory() {}

std::shared_ptr<Sender> TelegramFactory::createSender(const std::string &chat_id) const {
  return std::make_shared<TelegramSender>(chat_id);
}

std::shared_ptr<Preparer> TelegramFactory::createPreparer() const {
  return std::make_shared<TelegramPreparer>();
}
