from pulsar import Function

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


class Schema:
    schema = None

    def __init__(self, *args):
        self.schema = args[0]

    def __call__(self, f):
        def wrapped(*args):
            args = list(args)
            args[1] = self.schema.decode(args[1].encode())
            return self.schema.encode(f(*tuple(args))).decode("utf-8")

        return wrapped

# Function that deals with custom objects
class CustomObjectFunction(Function):
  def __init__(self):
    pass

  @Schema(JsonSchema(AccountSnapShotSchema))
  def process(self, input, context):
    logger = context.get_logger()
    logger.info("Message: {0}".format(input))
    logger.info(input.binance_portfolio)
    # Some processing
    input.binance_portfolio['tfboot']['account'] = 'world'
    return input