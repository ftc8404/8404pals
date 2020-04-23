# Kafka Docker

## Goal

Spins up a Docker Swarm with a Docker Stack, including containers for Kafka, Zookeeper, Kafka Manager, MongoDB, Mongo Express, Zuul, Eureka Server, and the user/actions microservices. Note there is no persistent storage backing Kafka or MongoDB.

In the Docker Compose file, you can chose uncomment the Kafka and MongoDB ports to expose them for local development.

-   Zuul Endpoints: <http://localhost:8080/actuator/mappings>
-   Zuul Routes: <http://localhost:8080/actuator/routes>
-   Eureka UI: <http://localhost:8761>
-   Kafka Manager UI: <http://localhost:9000>
-   Mongo Express UI: <http://localhost:8081>

## Usage

Build Docker Swarm and deploy Docker Stack.

```bash
docker swarm init
sh ./stack_deploy_local.sh
```

Delete (3) MongoDB databases, (3) Kafka topics, create sample data by hitting Zuul API Gateway endpoints, and return MongoDB documents as verification.

```bash
python3 ./refresh.py
```

## Results

```text
$ docker stack ls
NAME                SERVICES
auth-api          10

$ docker stack services auth-api

ID                  NAME                       MODE                REPLICAS            IMAGE                                        PORTS
ID                  NAME                       MODE                REPLICAS            IMAGE                                        PORTS
2b8h3jhbnqfy        auth-api_mongo_express   replicated          1/1                 mongo-express:latest                                            *:27017->27017/tcp
ezkh59y3kncd        auth-api_kafka_manager   replicated          1/1                 hlebalbau/kafka-manager:latest               *:9000->9000/tcp
gzz4o5q1v7dr        auth-api_fulfillment     replicated          1/1                      pals8404/auth-api-zuul:latest          *:8080->8080/tcp
nx23d9aef15o        auth-api_zookeeper       replicated          1/1                 wurstmeister/zookeeper:latest                *:2181->2181/tcp
qggjcswrfv6m        auth-api_eureka          replicated          1/1                 pals8404/auth-api-eureka:latest        *:8761->8761/tcp
ty4u7r09org5        auth-api_kafka           replicated          1/1                 wurstmeister/kafka:latest                    *:9092->9092/tcp
vn1as2p93jrf        auth-api_users          replicated          1/1                 pals8404/auth-api-users:latest

$ docker container ls

CONTAINER ID        IMAGE                                        COMMAND                  CREATED              STATUS              PORTS                                  NAMES
749199f2c84a        mongo-express:latest                         "tini -- node app"       38 seconds ago       Up 36 seconds       8081/tcp                               auth-api_mongo_express.1.arjli02nc06p9901y47hpevfl
814b801940ea        wurstmeister/kafka:latest                    "start-kafka.sh"         About a minute ago   Up About a minute                                          auth-api_kafka.1.q8d4jw0bcbdmcjrhvjt35p4hv
aea969916f7e        pals8404/auth-api-eureka:latest        "java -jar -Djava.se…"   4 hours ago          Up 4 hours          8761/tcp                               auth-api_eureka.1.r0ag0rtf5dgxjkipcbgy4phdk
894d57522cf5        pals8404/auth-api-zuul:latest          "java -jar -Djava.se…"   4 hours ago          Up 4 hours          8761/tcp                               auth-api_zuul.1.vaw0ot7l7yktke2e4skf1dmg2
b650d357d787        hlebalbau/kafka-manager:latest               "/kafka-manager/bin/…"   4 hours ago          Up 4 hours                                                 auth-api_kafka_manager.1.heequi6l9ylxqwos5bx47imh2
a93b12beb396        pals8404/auth-api-users:latest   "java -jar -Djava.se…"   4 hours ago          Up 4 hours          8080/tcp                               auth-api_fulfillment.1.u1o4rahz0decqpmokmefx9n8a
af280e77f975        wurstmeister/zookeeper:latest                "/bin/sh -c '/usr/sb…"   4 hours ago          Up 4 hours          22/tcp, 2181/tcp, 2888/tcp, 3888/tcp   auth-api_zookeeper.1.xbg8xetfof68l89ex4w155gnw
f2c82d998ac8        pals8404/auth-api-users:latest      "java -jar -Djava.se…"   4 hours ago          Up 4 hours          8080/tcp                               auth-api_users.1.vceb6iz8kehkssvni7hplsd0q
                   auth-api_mongo.1.tg6oa5t75wv2vow2hpoh6q871
```
