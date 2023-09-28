find_package(Protobuf REQUIRED)

set(protobuf_files
        ${CMAKE_CURRENT_SOURCE_DIR}/mi_mensaje.proto
        )

set(TARGET_NAME ecal_proto)
protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS ${protobuf_files})
add_library(${TARGET_NAME} ${PROTO_SRCS} ${PROTO_HDRS})
target_link_libraries(${TARGET_NAME}
        PUBLIC ${Protobuf_LIBRARIES})
target_include_directories(${TARGET_NAME}
    PUBLIC
        ${Protobuf_INCLUDE_DIRS}
        ${CMAKE_BINARY_DIR}
        ${CMAKE_CURRENT_BINARY_DIR}
        ${CMAKE_CURRENT_SOURCE_DIR})
