#!/bin/bash

set -eu
cd -- "$(dirname -- "$0")/files"

rsync -rci ./ / "$@"
