
find_package(eCAL REQUIRED)
find_package(Protobuf REQUIRED)

set(TARGET_NAME ecal_send_numeric)
set(ecal_snd_src
        ecal_send_numeric.cpp
)

add_executable(${TARGET_NAME} ${ecal_snd_src})

target_link_libraries(${TARGET_NAME}
        PRIVATE
        ecal_proto
        PUBLIC
        eCAL::core
        protobuf::libprotobuf
)
