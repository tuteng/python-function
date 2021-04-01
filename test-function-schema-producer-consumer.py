import pulsar
from pulsar.schema import *


class Person(Record):
    name = String()
    phone = String()


client = pulsar.Client('pulsar://127.0.0.1:6650')
producer = client.create_producer(topic='persistent://public/default/data-in', schema=JsonSchema(Person))
consumer = client.subscribe(topic='persistent://public/default/data-out', subscription_name='test-subscription', schema=JsonSchema(Person))

for i in range(100):
  dataObject = Person()
  dataObject.name = "name" + str(i)
  dataObject.phone = "phone" + str(i)
  producer.send(dataObject)
  print('send msg "%s", "%s"' % (dataObject.name, dataObject.phone))
for i in range(100):
  msg = consumer.receive()
  consumer.acknowledge(msg)
  ex = msg.value()
  print('receive and ack msg "%s", "%s"' % (ex.name, ex.phone))
client.close()