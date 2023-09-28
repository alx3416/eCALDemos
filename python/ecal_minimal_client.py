import sys
import time
import ecal.core.core as ecal_core
import ecal.core.service as ecal_service


def main():
    ecal_core.initialize(sys.argv, "py_minimal_service_client")
    ecal_core.set_process_state(1, 1, "I feel good")

    # create a client for the "DemoService" service
    client = ecal_service.Client("DemoService")

    # define the client response callback to catch server responses
    def client_resp_callback(service_info, response):
        if (service_info["call_state"] == "call_state_executed"):
            print("'DemoService' method '{}' responded : '{}'".format(service_info["method_name"], response))
            print()
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
        # call ping
        request = bytes("ping number {}".format(i), "ascii")
        print("'DemoService' method 'ping' requested with : {}".format(request))
        client.call_method("ping", request)
        time.sleep(3)

    client.destroy()
    ecal_core.finalize()


if __name__ == "__main__":
    main()
