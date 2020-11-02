add_executable(telegram_tester main.cpp)

add_proto_dependency(telegram_tester)

target_sources(telegram_tester
        PRIVATE
        ${TELEGRAMALERTCPPS}
        PUBLIC
        ${TELEGRAMALERTHS}
        )


target_include_directories(telegram_tester PUBLIC "${CMAKE_CURRENT_LIST_DIR}")
target_include_directories(telegram_tester PUBLIC "${CMAKE_CURRENT_LIST_DIR}/../")

my_target_link_cpprest(telegram_tester)
