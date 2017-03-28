#!/bin/bash

set -eu
cd -- "$(dirname -- "$0")/files"

LANG=C diff -r -u ./ / | grep -v ^Only | colordiff
