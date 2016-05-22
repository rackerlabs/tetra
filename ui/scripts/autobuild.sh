#!/bin/bash

babel -w app -d dist &
webpack -w dist/main.js dist/tetra.bundle.js &

wait
