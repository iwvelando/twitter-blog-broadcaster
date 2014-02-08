#!/bin/bash

# Figure out what directory this script resides in
thisDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
intervalSeconds=1799

# Wait a random time within the select interval
/bin/sleep $(( $RANDOM % $intervalSeconds ))

# Tweet
/usr/bin/env python "$thisDir/post.py" &> "$thisDir/post.log"
