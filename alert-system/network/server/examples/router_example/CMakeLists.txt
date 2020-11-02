add_executable(router_example main.cpp runtime_utils.h)

target_link_libraries(router_example network)

my_target_link_cpprest(router_example)