import pika
import json
import uuid

# Stablish the connection to RabbitMQ
print("*********************************************")
def on_open(connection):
    """Callback when we have connected to the AMQP broker."""
    print('Connected')


amqp_url="amqp://rabbitmq?connection_attempts=5&retry_delay=5"
credentials = pika.PlainCredentials('guest', 'guest')

parameters = pika.ConnectionParameters('rabbitmq',
                                       5672,
                                       '/',
                                       credentials,
                                       heartbeat=60
                                       )
connection = pika.SelectConnection(parameters, on_open_callback=on_open)


# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='amqp://://rabbitmq:5672'))
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='0.0.0.0:5762'))
channel = connection.channel()

# declare the exchange
channel.exchange_declare(
    exchange='plate', # name of the exchange
    exchange_type='direct' # the exchange type
)

# # the message that we want to send
# order = {
#     'id': str(uuid.uuid4()),
#     'user_email': 'barzansaeedpour@gmail.com',
#     'product': 'RabbitMQ',
#     'quantity': 1
# }



def publish(plate:str):
    # publish the messages
    channel.basic_publish(
        exchange='plate',  # the exchange that we want to use
        routing_key='plate.detection', # the routing key
        body=json.dumps({'plate': plate}) # body of the message
    )

print('[x] Sent plate message')


# close the message
connection.close() 