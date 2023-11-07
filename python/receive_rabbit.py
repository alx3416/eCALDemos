import os
import pika
import sys
import proto.mi_mensaje_pb2 as mi_mensaje_pb2


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')
    protobuf_message = mi_mensaje_pb2.HelloWorld()

    def callback(ch, method, properties, body):
        protobuf_message.ParseFromString(body)
        print(protobuf_message.name)
        print(protobuf_message.id)
        print(protobuf_message.msg)
        print(protobuf_message.state)

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)