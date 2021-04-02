import pulsar
from pulsar.schema import *

class EquityInfo(Record):
  total = Float()
  currency = String()
  timestamp = Long()
  def python_type(self):
    return self.__class__
class PositionInfo(Record):
  symbol = String()
  quantity = Float()
  markPrice = Float()
  liquidationPrice = Float()
  liquidationPercentage = Float()
  timestamp = Long()
  def python_type(self):
    return self.__class__
class SingleAccountSnap(Record):
  account = String()
  positions = Map(PositionInfo())
  equity = Map(EquityInfo())
  def python_type(self):
    return self.__class__
class AccountSnapShotSchema(Record):
  binance_portfolio = Map(SingleAccountSnap())
  def python_type(self):
    return self.__class__


client = pulsar.Client('pulsar://127.0.0.1:6650')
producer = client.create_producer(
  topic='persistent://public/default/complex-schema-in',
  schema=JsonSchema(AccountSnapShotSchema))
producer = client.create_producer(
  topic='persistent://public/default/complex-schema-out',
  schema=JsonSchema(AccountSnapShotSchema))
client.close()