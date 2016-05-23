#!/bin/bash

babel app -d dist
webpack dist/main.js dist/tetra.bundle.js
