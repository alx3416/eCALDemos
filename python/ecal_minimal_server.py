import sys
import time
import ecal.core.core as ecal_core
import ecal.core.service as ecal_service


def main():
    ecal_core.initialize(sys.argv, "py_minimal_service_server")
    ecal_core.set_process_state(1, 1, "I feel good")

    # create a server for the "DemoService" service
    server = ecal_service.Server("DemoService")

    # define the server method "function1"
    def function1_req_callback(method_name, req_type, resp_type, request):
        print("'DemoService' method '{}' called with {}".format(method_name, request))
        return 0, bytes("thank you for calling this service :-)", "ascii")

    # define the server method "ping" function
    def ping_req_callback(method_name, req_type, resp_type, request):
        print("'DemoService' method '{}' called with {}".format(method_name, request))
        return 0, bytes("pong", "ascii")

    # define the server methods and connect them to the callbacks
    server.add_method_callback("function1", "string", "string", function1_req_callback)
    server.add_method_callback("ping", "ping_type", "pong_type", ping_req_callback)

    # idle
    while ecal_core.ok():
        time.sleep(6)

    server.destroy()
    ecal_core.finalize()


if __name__ == "__main__":
    main()
