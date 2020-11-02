add_executable(matrix_tester main.cpp)

add_proto_dependency(matrix_tester)

target_sources(matrix_tester
        PRIVATE
        ${MATRIXALERTCPPS}
        PUBLIC
        ${MATRIXALERTHS}
        )

target_include_directories(matrix_tester PUBLIC "${CMAKE_CURRENT_LIST_DIR}")
target_include_directories(matrix_tester PUBLIC "${CMAKE_CURRENT_LIST_DIR}/../")

my_target_link_cpprest(matrix_tester)