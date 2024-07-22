#!/bin/bash

# Define variables
ACTION=$1
LISTEN_PORT=$2
CONTAINER_IP=$3
CONTAINER_PORT=22  # Fixed container port

# Check if the action, listen port, and container IP are provided
if [ -z "$LISTEN_PORT" ] || [ -z "$CONTAINER_IP" ]; then
  echo "Usage: $0 <open|close> <listen_port> <container_ip>"
  exit 1
fi

# Validate listen port and IP address
if ! [[ "$LISTEN_PORT" =~ ^[0-9]+$ ]] || ! [[ "$CONTAINER_IP" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]] || [ "$LISTEN_PORT" -lt 1 ] || [ "$LISTEN_PORT" -gt 65535 ]; then
  echo "Error: Port must be a number between 1 and 65535. Container IP must be in valid format (x.x.x.x)."
  exit 1
fi

# Function to open a port and forward it
open_port() {
  echo "Opening port $LISTEN_PORT and forwarding it to $CONTAINER_IP:$CONTAINER_PORT..."
  sudo iptables -A INPUT -p tcp --dport $LISTEN_PORT -j ACCEPT
  sudo iptables -t nat -A PREROUTING -p tcp --dport $LISTEN_PORT -j DNAT --to-destination $CONTAINER_IP:$CONTAINER_PORT
  sudo iptables -t nat -A POSTROUTING -p tcp -d $CONTAINER_IP --dport $CONTAINER_PORT -j MASQUERADE
  if [ $? -eq 0 ]; then
    echo "Port $LISTEN_PORT is now open and forwarded to $CONTAINER_IP:$CONTAINER_PORT."
  else
    echo "Failed to open and forward port $LISTEN_PORT."
  fi
}

# Function to close a port and unforward it
close_port() {
  echo "Removing port forwarding for port $LISTEN_PORT and closing port $LISTEN_PORT..."
  sudo iptables -t nat -D PREROUTING -p tcp --dport $LISTEN_PORT -j DNAT --to-destination $CONTAINER_IP:$CONTAINER_PORT
  sudo iptables -t nat -D POSTROUTING -p tcp -d $CONTAINER_IP --dport $CONTAINER_PORT -j MASQUERADE
  sudo iptables -D INPUT -p tcp --dport $LISTEN_PORT -j ACCEPT
  if [ $? -eq 0 ]; then
    echo "Port $LISTEN_PORT is now closed and port forwarding is removed."
  else
    echo "Failed to close port and remove forwarding."
  fi
}

# Main logic
case $ACTION in
  open)
    open_port
    ;;
  close)
    close_port
    ;;
  *)
    echo "Invalid action. Use 'open' or 'close'."
    exit 1
    ;;
esac
