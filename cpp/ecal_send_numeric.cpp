#include <ecal/ecal.h>
#include <ecal/msg/protobuf/publisher.h>
#include <iostream>
#include "mi_mensaje.pb.h"

int main(int argc, char **argv)
{
    // initialize eCAL API
    eCAL::Initialize(argc, argv, "cpp publisher");

    // set process state
    eCAL::Process::SetState(proc_sev_healthy, proc_sev_level1, "I feel good !");

    // create a publisher (topic name "person")
    eCAL::protobuf::CPublisher<pb::HelloWorld> pub("person");

    // generate a class instance of Person
    pb::HelloWorld proto_message;

    // enter main loop
    auto cnt = 0;
    while(eCAL::Ok())
    {
        // set message object content
        proto_message.set_id(++cnt);
        proto_message.set_name("Fulano Menganillo");
        proto_message.set_msg(12.3456);
        proto_message.set_state(true);

        // send the message object
        pub.Send(proto_message);
        std::cout << "sensing id   : " << proto_message.id()     << std::endl;
        eCAL::Process::SleepMS(500);
    }
    eCAL::Finalize();

    return(0);
}
