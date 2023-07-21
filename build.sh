#!/usr/bin/env bash

docker build --tag rt_over_96 .
docker run rt_over_96
docker stop rt_over_96
docker rm rt_over_96

