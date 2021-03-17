#!/bin/bash

set -e

convert mascotte.png -resize 32x32 favicon.ico

cp favicon.ico ../frontend/public/