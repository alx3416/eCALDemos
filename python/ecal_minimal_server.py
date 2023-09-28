import sys
import time
import ecal.core.core as ecal_core
import ecal.core.service as ecal_service
import proto.mi_mensaje_pb2 as mi_mensaje_pb2


def main():
    ecal_core.initialize(sys.argv, "py_minimal_service_server")
    ecal_core.set_process_state(1, 1, "I feel good")

    # create a server for the "DemoService" service
    server = ecal_service.Server("DemoService")

    # define the server method "function1"
    def function1_req_callback(method_name, req_type, resp_type, request):
        print("'DemoService' method '{}' called with {}".format(method_name, request))
        protobuf_message = mi_mensaje_pb2.HelloWorld()
        protobuf_message.name = "fulano menganillo"
        protobuf_message.id = protobuf_message.id + 1
        protobuf_message.msg = -123.456
        protobuf_message.state = True
        return 0, protobuf_message

    # define the server methods and connect them to the callbacks
    server.add_method_callback("function1", "string", "bytes", function1_req_callback)

    while ecal_core.ok():
        time.sleep(6)

    server.destroy()
    ecal_core.finalize()


if __name__ == "__main__":
    main()
