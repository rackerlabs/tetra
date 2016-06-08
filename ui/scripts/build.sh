#!/bin/bash
#
# build once,
#
#     ./build.sh
#
# watch files and auto rebuild (any argument works),
#
#     ./build.sh watch
#

function run_babel() {
    babel $1 app -d dist
}

function run_webpack() {
    webpack $1

}

if [ "$1" ]; then
    run_webpack -w &
    run_babel -w
    wait
else
    run_babel
    run_webpack
fi
