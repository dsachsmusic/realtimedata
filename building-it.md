- Create a docker image for flink, that extends apache's image, adding pyflink and kafka connector jar
  - create dockerfile.flink
  - docker build -f dockerfile.flink -t dsachsmusic/flink1.19.2-with-pyflink:latest . 
  - docker login
  - docker push dsachsmusic/flink1.19.2-with-pyflink:latest
- Create the docker-compose file...with and zookeeper, kafka, flink
- Create producer.py
- docker-compose pull && up
- from a separate wls window: python3 producer.py
  - this will start generating fake logs, and sending them to kafka (via topic "logs")
  - from project folder, run source .venv/bin/activate
  - run python 3 producer.py
- (optional) confirm kafka is getting logs
  - from a separate window: docker exec -it kafka bash (gets into bash shell in the docker container "kafka")
  - run kafka-console-consumer --bootstrap-server localhost:29092 --topic logs --from-beginning
- run the consumer...confirm flink is getting the messages from topic "logs"
  - docker exec -it flink-jobmanager bash
    - python3 /opt/flink_job.py

