import json

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common import Types, Time
from pyflink.datastream.connectors import FlinkKafkaConsumer
from pyflink.datastream.window import TumblingProcessingTimeWindows
from pyflink.common.serialization import SimpleStringSchema

#make the execution environment for our dataflow pipeline
#execution environment is a container, sort of. 
#it holds the configuration
#it holds what we define below...registers them in the "DAG builder"(?) behind the scenes
#eventually, we'll call execute on it
env = StreamExecutionEnvironment.get_execution_environment()

# set parallelism for job to "1"...meaning the operators (map, window, etc.) execute sequentially
# ...for simplicity...because parallelism introduces potential complexity 
# ...(complexity that can be learned about later)
env.set_parallelism(1)
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

# the following would debug line to verify raw kafka input is deserializing, etc, right.
# ds.print()

# side note: for the lamdas below, output_type is required to ...
# ...map python type to java type (flink runs on java)...
# ...has to be explicity set/mapped

# note: the lamdas below are transformations...
# - they will be madepart of  DAG (directed acyclic graph) that...
# - ...Flink will execute when env.execute() is called.
# - the objects (captured to variables ) are "DataStream object"
#   - ...they are edge of the DAG

# convert raw JSON strings to Python dicts
# - i.e. for each item in this data stream, apply this function:
#   - (lambda raw: json.loads(raw))  
parsed = ds.map(lambda x: {k: str(v) for k, v in json.loads(x).items()},
                output_type=Types.MAP(Types.STRING(), Types.STRING()))

# make a tuple (like an ordered array) so flink can understand(?)...
# i.e., for each event/message, make a tuple, with the message level...
# (info, warning, error), and, a count of 1...
# that "1' will be used for counting later...like a tally
# "kv" i.e. key value...a common naming convention for this kind of 
# ...transformation?
kv = parsed.map(lambda x: (x['level'], 1),
                output_type=Types.TUPLE([Types.STRING(), Types.INT()]))

# side note: job/operators will use "processing time"...
# ... this is the default
# ..."processing time" i.e. the time on the flink node...
# ... when it processes a given message as part of the job (?)
# ... this is relevant for the windowing function
# ... other options would be
# ... - EventTime (timestamp from kafka)...
# ...   - we'd want this if:
# ...     - utilizing watermarks, for handling out of order stuff
# ...     - if extracting time stamps
# ... - IngestionTime (when flink receives the event/message(?)) 

# Windowed count: how many ERRORs, INFOs, etc every 10 seconds
# reduce() is an operation that takes two elements at a time and
# ... combines them into one — repeatedly — until one result is left per group.
windowed = kv.key_by(lambda x: x[0]) \
    .window(TumblingProcessingTimeWindows.of(Time.seconds(10))) \
    .reduce(lambda a, b: (a[0], a[1] + b[1]))


# Print the counts 
# this is a "sink"
# Print the counts
windowed.print()

# Run the job
# (serialize the job?)
# It will be called "FCount Logs by Level" in 
env.execute("Count Logs by Level")