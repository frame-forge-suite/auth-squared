#!/bin/sh

# This hook is invoked by git commit, and can be bypassed with --no-verify option.
# It takes a single parameter, the name of the file that holds the proposed commit log message.
set -e
cog verify --file $1
cog check
