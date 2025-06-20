import json
#this requires not just pyflink but apache-flink
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.typeinfo import Types
from pyflink.datastream.connectors import FlinkKafkaConsumer

env = StreamExecutionEnvironment.get_execution_environment()

# Define Kafka consumer
kafka_props = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'log-flink-group',
    'auto.offset.reset': 'earliest'
}

consumer = FlinkKafkaConsumer(
    topics='logs',
    deserialization_schema=Types.STRING(),
    properties=kafka_props
)

ds = env.add_source(consumer)

# Convert raw JSON strings to Python dicts
parsed = ds.map(lambda x: json.loads(x), output_type=Types.MAP(Types.STRING(), Types.STRING()))

# Print the output (to stdout for now)
parsed.print()

# Run the job
env.execute("Flink Kafka Log Consumer")