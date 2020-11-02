#include <iostream>

#include <server/controllers/handler.h>
#include <server/controllers/router_controller.h>

#include "runtime_utils.h"

class HelloWorldHandler : public network::Handler {
 public:
  void handleGet(network::http_request message) override {
    std::cout << "Responded to world!" << std::endl;
    message.reply(web::http::status_codes::Accepted, "Hello, world!");
  }
};

int main(int argc, const char * argv[]) {
  InterruptHandler::hookSIGINT();

  network::RouterController server("http://host_auto_ip4:42000/api/"
                                  , {{"hello/world/", new HelloWorldHandler()}});

  try {
    // wait for server initialization...
    server.accept().wait();
    std::cout << "Modern C++ RouterController now listening for requests at: " << server.endpoint() << '\n';

    InterruptHandler::waitForUserInterrupt();

    server.shutdown().wait();
  }
  catch(std::exception & e) {
    std::cerr << e.what() << std::endl;
    std::cerr << "somehitng wrong happen! :(" << '\n';
  }

  return 0;
}