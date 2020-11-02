add_library(configurator configurator_service.h configurator_service.cpp recipient.h recipient.cpp)

add_proto_dependency(configurator)

target_include_directories(configurator PUBLIC "${CMAKE_CURRENT_LIST_DIR}")

target_link_libraries(configurator network)
target_link_libraries(configurator alert_senders)

my_target_link_cpprest(configurator)

add_executable(configurator_tester main.cpp)

add_proto_dependency(configurator_tester)

target_include_directories(configurator_tester PUBLIC "${CMAKE_CURRENT_LIST_DIR}")

target_link_libraries(configurator_tester configurator)

my_target_link_cpprest(configurator_tester)