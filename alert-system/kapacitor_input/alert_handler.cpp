#include <exception>
#include <memory>
#include <sstream>
#include <iostream>
#include <typeinfo>
#include <cpprest/http_client.h>
#include <cpprest/json.h>

#include "alert_handler.h"
#include "alert.pb.h"
#include <matrix_alerter/matrix_factory.h>
#include <telegram_alerter/telegram_factory.h>
#include <configurator_service.h>
#include "abstract_sender.h"

int AlertHandler::alerts_stored_ = 0;

AlertHandler::AlertHandler(): factories_({{"matrix", std::make_shared<MatrixFactory>()},
                                          {"telegram", std::make_shared<TelegramFactory>()}}),
                                          file_mutex()
                                          {}

void AlertHandler::dump_alert() {
  const std::lock_guard<std::mutex> lock(file_mutex);

  std::ofstream myfile;
  myfile.open ("alert_log.txt");
  if(alerts_stored_ < 10)
    std::cout << "O";
  myfile.close();

}

void AlertHandler::handlePost(network::http_request message) {
  auto alert_body_task = message.extract_json();

  //std::cout << alert_body_task.get().as_string() << std::endl;

  std::cerr << "New Request!" << std::endl;
  alerts_stored_++;


  alert_body_task.wait();
  web::json::value alert_body = alert_body_task.get();



  try {
    alert::Alert alert = parser_.parseJson(alert_body);

    //TODO delete this in Future
    // ONLY FOR TESTING PURPOSES. TEST + KAPACITOR
    /*
    std::shared_ptr<Factory> factory = std::make_shared<MatrixFactory>();
    auto preparer = factory->createPreparer();
    auto prepared_alert = preparer->prepare(alert);
    auto sender = factory->createSender("!peaLsZdtyOLKogIHZJ:matrix.org");
    sender->send(prepared_alert);
    */

    std::string level_id = "1";

    //TODO uncomment this when task_id is ready
    level_id = alert_body.at("level_id").as_string();

    auto recipient_list = ConfiguratorService().getRecipientByNotificationId(level_id);


    for(auto const& recipient: recipient_list)
    {
      std::map <std::string, std::string> chat_id_mapping;
      if(recipient.getMatrixId() != "-")
      {
        chat_id_mapping["matrix"] = recipient.getMatrixId();
        std::cerr << recipient.getMatrixId() << std::endl;
      }

      if(recipient.getTelegramChatId() != "-1")
      {
        chat_id_mapping["telegram"] = recipient.getTelegramChatId();
        std::cerr << recipient.getTelegramChatId() << std::endl;
      }

      for(auto it = chat_id_mapping.begin(); it != chat_id_mapping.end(); ++it)
      {
        auto preparer = factories_.at(it->first)->createPreparer();
        auto prepared_alert = preparer->prepare(alert);
        auto sender = factories_.at(it->first)->createSender(it->second);
        sender->send(prepared_alert);
      }

    }

    std::cerr << "SENT!" << std::endl;
    message.reply(web::http::status_codes::OK);
  } catch (std::exception) {
    message.reply(web::http::status_codes::ServiceUnavailable);
  }
}