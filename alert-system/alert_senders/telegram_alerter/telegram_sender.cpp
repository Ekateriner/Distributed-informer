#include "telegram_sender.h"

pplx::task<http_response> makeRequest(
    std::shared_ptr<TelegramPreparedAlert> telegram_alert,
    const std::string &token,
    const std::string &chat_id) {
  web::json::value request_details;
  request_details[U("chat_id")] =
      web::json::value::string(U(chat_id));
  request_details[U("text")] =
      web::json::value::string(U(telegram_alert->getText()));

  auto request_string = uri_builder(U("/bot" + token))
      .append_path("sendMessage")
      .to_string();
  return http_client(U("https://api.telegram.org/"))
      .request(
          methods::POST,
          request_string,
          request_details);

}

pplx::task<web::json::value> getResponse(http_response response) {
  if (response.status_code() != 200) {
    throw std::runtime_error(
        "Returned " + std::to_string(response.status_code()) +
            "\nResponse is" + response.extract_string().get());
  }
  // Convert the response body to JSON object.
  return response.extract_json();
}

void TelegramSender::send(std::shared_ptr<PreparedAlert> prepared_alert) {
  auto telegram_alert = std::static_pointer_cast<TelegramPreparedAlert>(prepared_alert);
  auto send_request =
      pplx::create_task([=]() { return makeRequest(telegram_alert, token_, chat_id_); })
          .then([=](http_response response) { return getResponse(response); });

  try {
    auto status = send_request.wait();
  } catch (std::exception &e) {
    std::cout << e.what();
  }
}
