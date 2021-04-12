#!/usr/bin/env bash

DB="d"
HOSTNAME="localhost"
PORT=9100


if ! [ -f "$DB" ]; then
  echo -e "Database file: $DB does not exists\n"
  echo -e "Please go to the folder cli/  and run \"python3 db_utils.py\" and create a fresh file\n"
  exit
fi

while true; do
  runzeo -f "$DB" -a "$HOSTNAME":"$PORT"
  sleep 3
done