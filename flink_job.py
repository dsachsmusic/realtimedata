import json

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.typeinfo import Types
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer

#make the execution environment for our dataflow pipeline
#execution environment is a container, sort of. 
#it holds the configuration
#it holds what we define below...registers them in the "DAG builder"(?) behind the scenes
#eventually, we'll call execute on it
env = StreamExecutionEnvironment.get_execution_environment()

# Define Kafka consumer
kafka_props = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'log-flink-group',
    'auto.offset.reset': 'earliest'
}

consumer = FlinkKafkaConsumer(
    topics='logs',
    deserialization_schema=SimpleStringSchema(),
    properties=kafka_props
)

#ds stands for data steam.  we are defining the data stream and we'll execute later
# start by adding the source (kafka consumer)
ds = env.add_source(consumer)

# debug line to verify raw kafka input is deserializing, etc, right.
ds.print()
# 
# for each item in this data stream, apply this function:
# - (lambda raw: json.loads(raw))
#   - i.e. convert raw JSON strings to Python dicts
# this is a transformation...and it is now part of the DAG (directed acyclic graph) that...
# ...Flink will execute when env.execute() is called.
# "parsed" is a "DataStream object"...its an edge of the DAG
parsed = ds.map(lambda x: {k: str(v) for k, v in json.loads(x).items()},
                output_type=Types.MAP(Types.STRING(), Types.STRING()))

# Print the output (to stdout for now)
# this is a "sink"
parsed.print()

# Run the job
# (serialize the job?)
# It will be called "Flink Kafka Log Consumer" in 
env.execute("Flink Kafka Log Consumer")