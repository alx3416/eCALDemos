import sys
import time
import ecal.core.core as ecal_core
import ecal.core.service as ecal_service
import proto.mi_mensaje_pb2 as mi_mensaje_pb2


def main():
    ecal_core.initialize(sys.argv, "py_minimal_service_client")
    ecal_core.set_process_state(1, 1, "I feel good")

    # create a client for the "DemoService" service
    client = ecal_service.Client("DemoService")
    protobuf_message = mi_mensaje_pb2.HelloWorld()

    # define the client response callback to catch server responses
    def client_resp_callback(service_info, response):
        if service_info["call_state"] == "call_state_executed":
            protobuf_message.ParseFromString(response)
            print("DemoService responded: " + protobuf_message.name)
        else:
            print(
                "server {} response failed, error : '{}'".format(service_info["host_name"], service_info["error_msg"]))
            print()

    # and add it to the client
    client.add_response_callback(client_resp_callback)

    # idle and call service methods
    i = 0
    while ecal_core.ok():
        i = i + 1
        # call function1
        request = bytes("hello function1 {}".format(i), "ascii")
        print("'DemoService' method 'function1' requested with : {}".format(request))
        client.call_method("function1", request)
        time.sleep(3)

    client.destroy()
    ecal_core.finalize()


if __name__ == "__main__":
    main()
