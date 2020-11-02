#include <cpprest/http_client.h>
#include <cpprest/uri.h>
#include <cpprest/json.h>
#include <pplx/pplxtasks.h>
#include "matrix_sender.h"
#include "matrix_prepared_alert.h"

using web::uri_builder;
using web::http::methods;
using web::http::http_response;
using web::http::client::http_client;

void MatrixSender::setToken(const std::string &token) {
  token_ = token;
}

const std::string &MatrixSender::getToken() const {
  return token_;
}

void MatrixSender::reserveToken() {
  token_ =
      "MDAxOGxvY2F0aW9uIG1hdHJpeC5vcmcKMDAxM2lkZW50aWZpZXIga2V5CjAwMTBjaWQgZ2VuID0gMQowMDI3Y2lkIHVzZXJfaWQgPSBAbmFyZWtpdG86bWF0cml4Lm9yZwowMDE2Y2lkIHR5cGUgPSBhY2Nlc3MKMDAyMWNpZCBub25jZSA9IDJDWEZJZksjcHhyZThDMkwKMDAyZnNpZ25hdHVyZSD6J5BVtG6MZfTsBzENuDZ1vtRkljZWSYwJjqkwhlVFwwo";
}

void MatrixSender::send(std::shared_ptr<PreparedAlert> prepared_alert) {
  auto matrix_alert = std::static_pointer_cast<MatrixPreparedAlert>(prepared_alert);
  reserveToken();
  std::string room_id = chat_id_;
  std::string text = matrix_alert->getText();
  auto my_token = "m.room.message?access_token=" + token_;
  auto postJson = pplx::create_task([=]() {
    web::json::value jsonObject;
    jsonObject[U("msgtype")] = web::json::value::string(U("m.text"));
    jsonObject[U("body")] = web::json::value::string(U(text));

    std::cout << "JSON Ready to be sent" << std::endl;

    return http_client(U("https://matrix-client.matrix.org/"))
        .request(methods::POST,
                 uri_builder(U("_matrix")).append_path(U("client")).append_path(U("r0"))
                     .append_path(U("rooms")).append_path(room_id)
                     .append_path("send").append_path(my_token).to_string(),
                 jsonObject);
  })

      // Get the response.
      .then([](http_response response) {
        std::cout << "CLient connected" << std::endl;
        std::cout << "https://matrix-client.matrix.org/" << std::endl;
        std::cout << response.status_code() << std::endl;
        std::cout << response.extract_json().get() << std::endl;
        // Check the status code.
        if (response.status_code() != 200) {
          throw std::runtime_error("Returned " + std::to_string(response.status_code()));
        } else {
          std::cout << "OK returned, i guess" << std::endl;
        }

        // Convert the response body to JSON object.
        return response.extract_json();
      });
  try {
    postJson.wait();
    std::cout << "Matrix with no exceptions" << std::endl;
  } catch (const std::exception &e) {
    std::cout << "Matrix with exceptions :c" << std::endl;
    printf("Error exception:%s\n", e.what());
  }
}

void MatrixSender::acquireToken() {
  auto postJson = pplx::create_task([]() {
    web::json::value jsonObject;
    jsonObject[U("type")] = web::json::value::string(U("m.login.password"));
    jsonObject[U("user")] = web::json::value::string(U("narekito"));
    jsonObject[U("password")] = web::json::value::string(U("Alchemist1Edward"));

    return http_client(U("https://matrix-client.matrix.org/"))
        .request(methods::POST,
                 uri_builder(U("_matrix")).append_path(U("client")).append_path(U("r0")).append_path(U("login")).to_string(),
                 jsonObject);
  })

      // Get the response.
      .then([](http_response response) {
        // Check the status code.
        if (response.status_code() != 200) {
          throw std::runtime_error("Returned " + std::to_string(response.status_code()));
        }

        // Convert the response body to JSON object.
        return response.extract_json();
      })

          // Parse the user details.
      .then([=](web::json::value jsonObject) {
        token_ = jsonObject[U("access_token")].as_string();
      });
  try {
    postJson.wait();
  } catch (const std::exception &e) {
    printf("Error exception:%s\n", e.what());
  }
}
