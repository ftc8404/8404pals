#!/usr/bin/env bash

./gradlew clean build
docker build -f Docker/Dockerfile --no-cache -t J3T4R0/storefront-cases:latest .
docker push ftc8404/pals:latest

# docker run --name pals -d ftc8404/pals:latest