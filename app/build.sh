#!/usr/bin/env bash

# Builds docker image and tags it with current git branch
# commit hash.

COMMIT_HASH=$(git rev-parse HEAD)
docker build --tag garret-interview:$COMMIT_HASH .
