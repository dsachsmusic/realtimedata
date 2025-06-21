# Docker
Get into a docker container 
- docker exec -it containername bash
  - example: docker exec -it kafka bash

Spin up a container that is defined in docker-compose.yml
- docker-compose up -d containername
  - example: docker-compose up -d zookeeper
  - note: -d flag sets detached mode...doesn't show logs/output
- if container 
  
Handle stuck docker container
- docker-compose restart containername
