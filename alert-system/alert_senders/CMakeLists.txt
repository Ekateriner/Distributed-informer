add_library(alert_senders)

add_proto_dependency(alert_senders)

SET(MATRIXALERTCPPS
        "${CMAKE_CURRENT_LIST_DIR}/matrix_alerter/matrix_factory.cpp"
        "${CMAKE_CURRENT_LIST_DIR}/matrix_alerter/matrix_prepared_alert.cpp"
        "${CMAKE_CURRENT_LIST_DIR}/matrix_alerter/matrix_preparer.cpp"
        "${CMAKE_CURRENT_LIST_DIR}/matrix_alerter/matrix_sender.cpp"
        "${RootProtoSources}"
        )

SET(MATRIXALERTHS
        "${CMAKE_CURRENT_LIST_DIR}/abstract_sender.h"
        "${CMAKE_CURRENT_LIST_DIR}/matrix_alerter/matrix_factory.h"
        "${CMAKE_CURRENT_LIST_DIR}/matrix_alerter/matrix_prepared_alert.h"
        "${CMAKE_CURRENT_LIST_DIR}/matrix_alerter/matrix_preparer.h"
        "${CMAKE_CURRENT_LIST_DIR}/matrix_alerter/matrix_sender.h"
        "${RootProtoHeaders}"
        )
SET(TELEGRAMALERTCPPS
        "${CMAKE_CURRENT_LIST_DIR}/telegram_alerter/telegram_factory.cpp"
        "${CMAKE_CURRENT_LIST_DIR}/telegram_alerter/telegram_prepared_alert.cpp"
        "${CMAKE_CURRENT_LIST_DIR}/telegram_alerter/telegram_preparer.cpp"
        "${CMAKE_CURRENT_LIST_DIR}/telegram_alerter/telegram_sender.cpp"
        "${RootProtoSources}"
        )

SET(TELEGRAMALERTHS
        "${CMAKE_CURRENT_LIST_DIR}/abstract_sender.h"
        "${CMAKE_CURRENT_LIST_DIR}/telegram_alerter/telegram_factory.h"
        "${CMAKE_CURRENT_LIST_DIR}/telegram_alerter/telegram_prepared_alert.h"
        "${CMAKE_CURRENT_LIST_DIR}/telegram_alerter/telegram_preparer.h"
        "${CMAKE_CURRENT_LIST_DIR}/telegram_alerter/telegram_sender.h"
        "${RootProtoHeaders}"
        )

set(DELIVERY_RULES_SRCS
        "${CMAKE_CURRENT_LIST_DIR}/delivery_rules/delivery_rule.cpp"
        "${CMAKE_CURRENT_LIST_DIR}/delivery_rules/default_delivery_rule.cpp"
        "${CMAKE_CURRENT_LIST_DIR}/delivery_rules/delivery_rule_decorators.cpp"
        "${CMAKE_CURRENT_LIST_DIR}/delivery_rules/filter_predicates.cpp"
)

target_sources(alert_senders
        PRIVATE
        ${MATRIXALERTCPPS}
        ${TELEGRAMALERTCPPS}
        ${DELIVERY_RULES_SRCS}
        PUBLIC
        ${TELEGRAMALERTHS}
        ${MATRIXALERTHS}
        )

target_include_directories(alert_senders
        PUBLIC
        "${CMAKE_CURRENT_LIST_DIR}"
        "${CMAKE_CURRENT_LIST_DIR}/telegram_alerter"
        "${CMAKE_CURRENT_LIST_DIR}/matrix_alerter"
        "${CMAKE_CURRENT_LIST_DIR}/delivery_rules"
)

my_target_link_cpprest(alert_senders)

add_subdirectory(matrix_alerter)
add_subdirectory(telegram_alerter)
