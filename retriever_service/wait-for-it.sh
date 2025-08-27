#!/usr/bin/env bash
# wait-for-it.sh: wait until a host:port is available
# Usage: ./wait-for-it.sh host:port -- command args

hostport=$1
shift
cmd="$@"

host=$(echo $hostport | cut -d':' -f1)
port=$(echo $hostport | cut -d':' -f2)

echo "Waiting for $host:$port..."

while ! nc -z $host $port; do
  sleep 1
done

echo "$host:$port is available, starting command..."
exec $cmd
