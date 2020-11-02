file(GLOB RootProtoFiles "${CMAKE_CURRENT_SOURCE_DIR}/*.proto")
PROTOBUF_GENERATE_CPP(RootProtoSources RootProtoHeaders ${RootProtoFiles})
set(RootProtoSources ${RootProtoSources} PARENT_SCOPE)
set(RootProtoHeaders ${RootProtoHeaders} PARENT_SCOPE)

add_custom_target(root_proto_generating DEPENDS ${RootProtoSources})
