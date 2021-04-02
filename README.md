# python-function

This is an example of how to use the python function.

## Project Structure

```
python_function
├── __init__.py
├── custom_object_function.py
└── pyserde
    ├── __init__.py
    └── serde.py
```

In python, if a folder contains `__init__` file, we call it a package, python_function and pyserde are both packages. Compressing `python_function` directory will generate `python_function.zip`.

## How to use

### Start pulsar standalone

```
docker run -d -it \
    -p 6650:6650 \
    -p 8080:8080 \
    --name pulsar-standalone \
    apachepulsar/pulsar-all:2.7.1 \
    bin/pulsar standalone
```

### Start python function by use zip package
```
./bin/pulsar-admin functions create \
    --tenant public   --namespace default   --name my_function \
    --py /YOUR-PATH/python_function.zip \
    --classname python_function.custom_object_function.CustomObjectFunction \
    --custom-serde-inputs '{"input-topic-1":"python_function.pyserde.serde.CustomSerDe","input-topic-2":"python_function.pyserde.serde.CustomSerDe"}' \
    --output-serde-classname python_function.pyserde.serde.CustomSerDe \
    --output output-topic-3
```
Replace `YOUR-PATH` with your file path.

### Run produce and consume

```
python test-producer-consumer.py
```

## Use schema

Setting schema is not currently supported in python function, this is a temporary solution. [This](https://github.com/apache/pulsar/issues/10114) is a track of the python function schema.

### Start pulsar standalone

```
docker run -d -it \
    -p 6650:6650 \
    -p 8080:8080 \
    --name pulsar-standalone \
    apachepulsar/pulsar-all:2.7.1 \
    bin/pulsar standalone
```

### Start python function by use zip package

```
./bin/pulsar-admin functions localrun \
  --name test-function \
  --tenant public \
  --namespace default \
  --py /YOUR-PATH/python_function_schema.zip \
  --classname python_function_schema.python_function_schema.CustomObjectFunction \
  --inputs persistent://public/default/data-in \
  --output persistent://public/default/data-out
```
Replace `YOUR-PATH` with your file path.


### Run produce and consume

```
python test-function-schema-producer-consumer.py
```

## Use complex schema

### Start pulsar standalone

```
./bin/pulsar-admin functions localrun \
    --name test-function \
    --tenant public \
    --namespace default \
    --py /YOUR-PATH/python_function_complex_schema.zip \
    --classname python_function_complex_schema.python_function_complex_schema.CustomObjectFunction \
    --inputs persistent://public/default/complex-schema-in   --output persistent://public/default/complex-schema-out
```
Replace `YOUR-PATH` with your file path.

### Run produce and consume

Create schema for input and output topic

```
python create-comple-schema.py
```

Run consumer:
```
python complex-schema-consumer.py
```

Open another window for run produce:

```
python complex-schema-producer.py
```

Data produced by the producer:
```
e1 = EquityInfo()
e2 = EquityInfo()
p1 = PositionInfo()
p2 = PositionInfo()
b = SingleAccountSnap()
b.account = 'hello'
b.positions = {'positions': {'DUMP': p1, 'QDUMP': p2}}
b.equity = {'equity': {'NOOP': e1, 'NOOP2': e2}}
data = AccountSnapShotSchema(binance_portfolio={'tfboot': b})
```

Data received by the function:
```
{
	'binance_portfolio': {
		'tfboot': {
			'account': 'hello',
			'positions': {
				'DUMP': {
					'symbol': '',
					'quantity': 0.0,
					'markPrice': 0.0,
					'liquidationPrice': 0.0,
					'liquidationPercentage': 0.0,
					'timestamp': 0
				},
				'QDUMP': {
					'symbol': '',
					'quantity': 0.0,
					'markPrice': 0.0,
					'liquidationPrice': 0.0,
					'liquidationPercentage': 0.0,
					'timestamp': 0
				}
			},
			'equity': {
				'NOOP': {
					'total': 0.0,
					'currency': '',
					'timestamp': 0
				},
				'NOOP2': {
					'total': 0.0,
					'currency': '',
					'timestamp': 0
				}
			}
		}
	}
}
```
The function processes the data, updating field account from `hello` to `world`.

Data received by the consumer:
```
{
	'binance_portfolio': {
		'tfboot': {
			'account': 'world',
			'positions': {
				'DUMP': {
					'symbol': '',
					'quantity': 0.0,
					'markPrice': 0.0,
					'liquidationPrice': 0.0,
					'liquidationPercentage': 0.0,
					'timestamp': 0
				},
				'QDUMP': {
					'symbol': '',
					'quantity': 0.0,
					'markPrice': 0.0,
					'liquidationPrice': 0.0,
					'liquidationPercentage': 0.0,
					'timestamp': 0
				}
			},
			'equity': {
				'NOOP': {
					'total': 0.0,
					'currency': '',
					'timestamp': 0
				},
				'NOOP2': {
					'total': 0.0,
					'currency': '',
					'timestamp': 0
				}
			}
		}
	}
}
```