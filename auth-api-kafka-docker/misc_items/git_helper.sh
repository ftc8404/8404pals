#!/bin/bash

# usage: sh ./git_helper.sh "Refactoring auth-api code"

args=("$@")

root="https://github.com/ftc8404/pals"
repos=(
  auth-api-demo-users
  storefront-eureka-server
  storefront-zuul-proxy
  auth-api-kafka-docker
)
if [ -n "${args[0]}" ]; then
    comment=${args[0]}
else
    comment="Automated commit of changes to project"
fi

for repo in "${repos[@]}"
do
  cd ${root}/${repo} && \
  git add -A && \
  git commit -m "${comment}" && \
  git push && \
  git status
  echo ${repo}
done

cd ../
