#!/usr/bin/env bash

# Builds docker image and tags it with current git branch
# commit hash.

COMMIT_HASH=$(git rev-parse HEAD)
docker build --tag garrett-interview:$COMMIT_HASH .
docker tag garrett-interview:$COMMIT_HASH garrett-interview:latest
