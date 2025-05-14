#!/usr/bin/env bash

DOCKER_BUILDKIT=1 docker build \
  --secret id=env,src=.env \
  -f Dockerfile.consumers \
  -t stellar-harvest-ie-consumers:latest .
