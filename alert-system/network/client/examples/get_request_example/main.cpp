#include <iostream>
#include <cpprest/http_client.h>
#include <cpprest/filestream.h>
#include <cpprest/uri.h>
#include <cpprest/json.h>

using namespace utility;
using namespace web;
using namespace web::http;
using namespace web::http::client;
using namespace concurrency::streams;

// GET request using cpprest library. Look more at: http://www.atakansarioglu.com/easy-quick-start-cplusplus-rest-client-example-cpprest-tutorial/
int main() {
  // Create a file stream to write the received file into it.
  auto fileStream = std::make_shared<ostream>();

  // Open stream to output file.
  pplx::task<void> requestTask = fstream::open_ostream(U("users.json"))

      // Make a GET request.
      .then([=](ostream outFile) {
        *fileStream = outFile;

        // Create http_client to send the request.
        http_client client(U("https://reqres.in"));

        // Build request URI and start the request.
        return client.request(methods::GET, uri_builder(U("api")).append_path(U("users")).to_string());
      })

          // Get the response.
      .then([=](http_response response) {
        // Check the status code.
        if (response.status_code() != 200) {
          throw std::runtime_error("Returned " + std::to_string(response.status_code()));
        }

        // Write the response body to file stream.
        response.body().read_to_end(fileStream->streambuf()).wait();

        // Close the file.
        return fileStream->close();
      });

  // Wait for the concurrent tasks to finish.
  try {
    while (!requestTask.is_done()) { std::cout << "."; }
  } catch (const std::exception &e) {
    printf("Error exception:%s\n", e.what());
  }

  return 0;
}
