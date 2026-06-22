#!/bin/bash
cd $(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
set -x

docker buildx build --no-cache \
	-t dfine:latest \
	--build-arg BASE_IMAGE_VERSION=8.1.1 \
	--build-arg USER=$(cat ${HOME}/.gitlab_user) \
	--secret id=gitlab_token,src=${HOME}/.gitlab_token \
	.
