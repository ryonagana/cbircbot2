#!/usr/bin/env bash

export CB_NICKNAME="ryonagana"
export CB_IDENTD="hello"
export CB_HOST="chat.freenode.net"
export CB_CHANNEL="#lamechannel"
export CB_USER_PASSWD="cb3252518"
export OPEN_WEATHER_API="1c7173614738bfe6fa36212491f1f053"
export CB_NICKSERV_AUTH=1
export ZEO_ADDRESS="localhost"
export ZEO_PORT=9100

while true
do
python3 run.py
sleep 10
done
