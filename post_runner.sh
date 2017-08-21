#!/bin/bash

[[ -f /tmp/post.lock ]] && exit 0

touch /tmp/post.lock

trap 'rm -f /tmp/post.lock' EXIT

# Figure out what directory this script resides in
thisDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
intervalSeconds=4799

# Wait a random time within the select interval
/bin/sleep $(( $RANDOM % $intervalSeconds ))

# Tweet
/usr/bin/env python "$thisDir/post.py" &>> "$thisDir/post.log" || exit 1

exit 0
