#!/bin/bash

ENV_DIR="$1";
COMMAND="$2"
/usr/bin/env -i bash --norc scripts/init-env.sh "$ENV_DIR" "$COMMAND";