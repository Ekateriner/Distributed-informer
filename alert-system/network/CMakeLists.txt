add_library(network)

target_sources(network
    PRIVATE
        ${CMAKE_CURRENT_LIST_DIR}/network_utils.cpp
        ${CMAKE_CURRENT_LIST_DIR}/server/controllers/basic_controller.h
        ${CMAKE_CURRENT_LIST_DIR}/server/controllers/basic_controller.cpp
        ${CMAKE_CURRENT_LIST_DIR}/server/controllers/router_controller.cpp
    PUBLIC
        ${CMAKE_CURRENT_LIST_DIR}/network_utils.h
        ${CMAKE_CURRENT_LIST_DIR}/server/controllers/handler.h
        ${CMAKE_CURRENT_LIST_DIR}/server/controllers/router_controller.h
)

target_include_directories(network PUBLIC "${CMAKE_CURRENT_LIST_DIR}" "${CMAKE_CURRENT_LIST_DIR}/server/controllers")

my_target_link_cpprest(network)

add_subdirectory("${CMAKE_CURRENT_LIST_DIR}/server/examples/router_example")
add_subdirectory("${CMAKE_CURRENT_LIST_DIR}/client/examples/get_request_example")