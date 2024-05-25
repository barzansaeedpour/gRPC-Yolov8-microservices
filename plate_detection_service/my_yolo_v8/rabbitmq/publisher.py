
import pika
import os
import time
from dotenv import find_dotenv, load_dotenv
import json

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
AMQP_URL = os.getenv("AMQP_URL")

# read rabbitmq connection url from environment variable
def publish(detected_plates, path):
    
    # Stablish the connection to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # declare the exchange
    channel.exchange_declare(
        exchange='order', # name of the exchange
        exchange_type='direct' # the exchange type
    )

    channel.basic_publish(
        exchange='order', # the exchange that we want to use
        routing_key='order.report',
        body=json.dumps({"detected_plates": detected_plates,}) # body of the message
    )

    print('[x] Sent report message')


    # close the message
    connection.close() 
    
# # read rabbitmq connection url from environment variable
# def publish(plate:str):
#     print('******** plate:',plate,'********')
#     # pass
#     # read rabbitmq connection url from environment variable
#     # amqp_url = os.environ['AMQP_URL']
#     amqp_url = AMQP_URL
#     url_params = pika.URLParameters(amqp_url)

#     # connect to rabbitmq
#     connection = pika.BlockingConnection(url_params)
#     chan = connection.channel()

#     # declare a new queue
#     # durable flag is set so that messages are retained
#     # in the rabbitmq volume even between restarts
#     chan.queue_declare(queue='hello', durable=True)

#     # publish a 100 messages to the queue
#     # for i in range(5):
#     chan.basic_publish(exchange='', routing_key='hello',
#                     body=plate, properties=pika.BasicProperties(delivery_mode=2))
#     print(f"Produced the message: {plate}")

#     # close the channel and connection
#     # to avoid program from entering with any lingering
#     # message in the queue cache
#     chan.close()
#     connection.close()


#################################################################
# import pika
# import json
# import uuid
# import os
# # Stablish the connection to RabbitMQ
# # print("*********************************************")
# # def on_open(connection):
# #     """Callback when we have connected to the AMQP broker."""
# #     print('Connected')


# # amqp_url="amqp://rabbitmq?connection_attempts=5&retry_delay=5"
# # credentials = pika.PlainCredentials('guest', 'guest')

# # parameters = pika.ConnectionParameters('rabbitmq',
# #                                        5672,
# #                                        '/',
# #                                        credentials,
# #                                        heartbeat=60
# #                                        )
# # connection = pika.SelectConnection(parameters, on_open_callback=on_open)

# # read rabbitmq connection url from environment variable
# amqp_url = os.environ['AMQP_URL']
# url_params = pika.URLParameters(amqp_url)

# # connect to rabbitmq
# connection = pika.BlockingConnection(url_params)

# # connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
# # connection = pika.BlockingConnection(pika.ConnectionParameters(host='amqp://://rabbitmq:5672'))
# # connection = pika.BlockingConnection(pika.ConnectionParameters(host='0.0.0.0:5762'))
# channel = connection.channel()

# # declare the exchange
# channel.exchange_declare(
#     exchange='plate', # name of the exchange
#     exchange_type='direct' # the exchange type
# )

# channel.queue_declare(queue='plate_detection', durable=True)

# # # the message that we want to send
# # order = {
# #     'id': str(uuid.uuid4()),
# #     'user_email': 'barzansaeedpour@gmail.com',
# #     'product': 'RabbitMQ',
# #     'quantity': 1
# # }



# def publish(plate:str):
#     # publish the messages
#     channel.basic_publish(
#         exchange='plate',  # the exchange that we want to use
#         routing_key='plate.detection', # the routing key
#         body=json.dumps({'plate': plate}) # body of the message
#     )

# print('[x] Sent plate message')


# # close the message
# connection.close() 



