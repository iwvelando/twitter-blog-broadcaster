#!/bin/bash

/bin/sleep $(( $RANDOM % 1799 ))

/usr/bin/env python $HOME/cron/post.py &> $HOME/cron/post.log
