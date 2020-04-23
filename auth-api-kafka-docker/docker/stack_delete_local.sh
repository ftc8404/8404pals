#!/bin/sh

# Destroys the auth-api Docker stack

# usage: sh ./stack_delete_local.sh

set -e

docker stack rm auth-api

echo "Destroying the stack...pausing for 30 seconds..."
sleep 30

docker ps

echo "Script completed..."
