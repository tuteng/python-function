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
    return self.__class__


client = pulsar.Client('pulsar://127.0.0.1:6650')
producer = client.create_producer(
  topic='persistent://public/default/complex-schema-in',
  schema=JsonSchema(AccountSnapShotSchema))
e1 = EquityInfo()
e2 = EquityInfo()
p1 = PositionInfo()
p2 = PositionInfo()
b = SingleAccountSnap()
b.account = 'hello'
b.positions = {'positions': {'DUMP': p1, 'QDUMP': p2}}
b.equity = {'equity': {'NOOP': e1, 'NOOP2': e2}}
data = AccountSnapShotSchema(binance_portfolio={'tfboot': b})
producer.send(data)
client.close()