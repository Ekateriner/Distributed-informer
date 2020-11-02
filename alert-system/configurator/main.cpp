#include <iostream>
#include "configurator_service.h"
#include "recipient.h"
#include <string>

int main()
{
  auto x = ConfiguratorService();
  std::string s = "";
  auto z = ConfiguratorService().getRecipientByNotificationId(s);
  for(auto lol : z)
    std::cout << lol.getTelegramChatId() << ' ' << lol.getMatrixId() << std::endl;
  return 0;
}