# Docker
Get into a docker container 
- docker exec -it containername bash
  - example: docker exec -it kafka bash

Spin up a container that is defined in docker-compose.yml
- docker-compose up -d containername
  - example: docker-compose up -d zookeeper
  - note: -d flag sets detached mode...without it, never get back to cmd prompt
  
Handle stuck docker container
- docker-compose restart containername