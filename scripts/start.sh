#!/bin/bash

# Start script for RFP Contract Management System
# This script starts both the backend and frontend servers

# Configuration
BACKEND_PORT=8000
FRONTEND_PORT=3000

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Check for required commands
if ! command_exists python; then
  echo "Error: Python is not installed"
  exit 1
fi

if ! command_exists node; then
  echo "Error: Node.js is not installed"
  exit 1
fi

if ! command_exists npm; then
  echo "Error: npm is not installed"
  exit 1
fi

# Check if MongoDB is running
echo "Checking MongoDB connection..."
if command_exists mongosh; then
  mongosh --eval "db.adminCommand('ping')" >/dev/null 2>&1
  if [ $? -ne 0 ]; then
    echo "Warning: MongoDB does not appear to be running"
    echo "Please start MongoDB before continuing"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
      exit 1
    fi
  else
    echo "MongoDB is running"
  fi
else
  echo "Warning: mongosh command not found, skipping MongoDB check"
fi

# Start backend server
echo "Starting backend server..."
cd ../backend
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python -m venv venv
fi

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
  source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
  source venv/Scripts/activate
else
  echo "Error: Could not find virtual environment activation script"
  exit 1
fi

# Install backend dependencies
echo "Installing backend dependencies..."
pip install -r requirements.txt

# Start backend server in background
echo "Starting backend server on port $BACKEND_PORT..."
uvicorn app.main:app --host 0.0.0.0 --port $BACKEND_PORT --reload &
BACKEND_PID=$!

# Start frontend server
echo "Starting frontend server..."
cd ../frontend

# Install frontend dependencies
echo "Installing frontend dependencies..."
npm install

# Start frontend server in background
echo "Starting frontend server on port $FRONTEND_PORT..."
npm start &
FRONTEND_PID=$!

# Function to handle script termination
cleanup() {
  echo "Stopping servers..."
  kill $BACKEND_PID $FRONTEND_PID
  exit 0
}

# Register the cleanup function for when the script is terminated
trap cleanup SIGINT SIGTERM

echo "Servers started successfully!"
echo "Backend server running on http://localhost:$BACKEND_PORT"
echo "Frontend server running on http://localhost:$FRONTEND_PORT"
echo "Press Ctrl+C to stop both servers"

# Keep the script running
wait
