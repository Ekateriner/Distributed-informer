#include <cpprest/http_client.h>
#include <cpprest/uri.h>
#include <cpprest/json.h>

#include "configurator_service.h"


std::vector<Recipient> ConfiguratorService::getRecipientByNotificationId(const std::string & notification_id) {
  auto request_string = web::uri_builder(U("/api"))
          .append_path("notifications")
          .append_path("?level_id=")
          .to_string();

  request_string += notification_id;
  auto recipients_request = pplx::create_task([=](){ return makeRequest(request_string); })
          .then([=](web::http::http_response response){
            if (response.status_code() >= 400) {
              std::cerr << response.to_string() << std::endl;
              throw std::runtime_error(
                "Returned " + std::to_string(response.status_code()) +
                "\nResponse is" + response.extract_string().get());
            }
            std::vector<Recipient> recipients;
            auto json_body = response.extract_json();
            json_body.wait();
            for (int i = 0; i < json_body.get().as_array().size(); ++i) {
              auto recipient_object = json_body.get().as_array()[i];
              recipients.emplace_back(Recipient(recipient_object.at("user")));
            }
            return recipients;
          });

  try {
    auto status = recipients_request.wait();
    return recipients_request.get();
  } catch (const std::exception& e) {
    std::cerr << "AH, WE HAVE A LITTLE PROBLEM" << std::endl;
    std::cerr << e.what() ;
  }
}

pplx::task<web::http::http_response> ConfiguratorService::makeRequest(const std::string & request_string) {
  return web::http::client::http_client(U(CONFIGURATOR_HOST)).request(web::http::methods::GET, request_string);
}
