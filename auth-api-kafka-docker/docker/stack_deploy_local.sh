#!/bin/sh

# Deploys the auth-api Docker stack

# usage: sh ./stack_deploy_local.sh

set -e

# docker swarm init

docker stack deploy -c docker-compose-middleware.yml auth-api
echo "Starting the stack: middleware...pausing for 30 seconds..."
sleep 30

docker stack deploy -c docker-compose-services.yml auth-api
echo "Starting the stack: services...pausing for 10 seconds..."
sleep 10

docker stack ls
docker stack services auth-api
docker container ls

echo "Script completed..."
echo "Services may take up to several minutes to start, fully..."
