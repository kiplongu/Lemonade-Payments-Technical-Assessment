#!/bin/bash
CPU_THRESHOLD=80
SERVICE_NAME="laravel-backend"

while true; do
  CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}')
  CPU_USAGE=${CPU_USAGE%.*}
  if [ "$CPU_USAGE" -gt "$CPU_THRESHOLD" ]; then
    echo "CPU usage is $CPU_USAGE%, restarting $SERVICE_NAME..."
    systemctl restart $SERVICE_NAME
  fi
  sleep 10
done
