import pulsar
from pulsar.schema import *

class EquityInfo(Record):
  total = Float()
  currency = String()
  timestamp = Long()
  def python_type(self):
    return dict
class PositionInfo(Record):
  symbol = String()
  quantity = Float()
  markPrice = Float()
  liquidationPrice = Float()
  liquidationPercentage = Float()
  timestamp = Long()
  def python_type(self):
    return dict
class SingleAccountSnap(Record):
  account = String()
  positions = Map(PositionInfo())
  equity = Map(EquityInfo())
  def python_type(self):
    return dict
class AccountSnapShotSchema(Record):
  binance_portfolio = Map(SingleAccountSnap())
  def python_type(self):
    return dict

client = pulsar.Client('pulsar://127.0.0.1:6650')
consumer = client.subscribe(topic='persistent://public/default/complex-schema-out',
    subscription_name='test-subscription',
    schema=JsonSchema(AccountSnapShotSchema))

while True:
    msg = consumer.receive()
    try:
        data = msg.value()
        print(type(data))
        print(dir(data))
        print(data)
        # Acknowledge successful processing of the message
        consumer.acknowledge(msg)
    except:
        # Message failed to be processed
        consumer.negative_acknowledge(msg)
client.close()