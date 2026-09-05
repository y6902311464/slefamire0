#!/bin/sh

python bot.py &
BOT_PID=$!

python helper.py &
HELPER_PID=$!

trap 'kill $BOT_PID $HELPER_PID' TERM INT

wait $BOT_PID
wait $HELPER_PID
