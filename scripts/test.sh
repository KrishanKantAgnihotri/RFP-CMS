#!/bin/bash

# Test script for RFP Contract Management System
# This script runs tests for both the backend and frontend

# Configuration
TEST_BACKEND=true
TEST_FRONTEND=true

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --backend-only)
      TEST_FRONTEND=false
      shift
      ;;
    --frontend-only)
      TEST_BACKEND=false
      shift
      ;;
    *)
      echo "Unknown option: $key"
      echo "Available options: --backend-only, --frontend-only"
      exit 1
      ;;
  esac
done

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Run backend tests
run_backend_tests() {
  echo "Running backend tests..."
  
  # Check for Python
  if ! command_exists python; then
    echo "Error: Python is not installed"
    return 1
  fi
  
  # Navigate to backend directory
  cd ../backend
  
  # Create virtual environment if it doesn't exist
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
    return 1
  fi
  
  # Install backend dependencies
  echo "Installing backend dependencies..."
  pip install -r requirements.txt
  
  # Run tests
  echo "Running pytest..."
  pytest
  
  # Return to scripts directory
  cd ../scripts
}

# Run frontend tests
run_frontend_tests() {
  echo "Running frontend tests..."
  
  # Check for Node.js
  if ! command_exists node; then
    echo "Error: Node.js is not installed"
    return 1
  fi
  
  # Check for npm
  if ! command_exists npm; then
    echo "Error: npm is not installed"
    return 1
  fi
  
  # Navigate to frontend directory
  cd ../frontend
  
  # Install frontend dependencies
  echo "Installing frontend dependencies..."
  npm install
  
  # Run tests
  echo "Running tests..."
  npm test -- --watchAll=false
  
  # Return to scripts directory
  cd ../scripts
}

# Run linting
run_linting() {
  echo "Running linting..."
  
  # Backend linting
  if [ "$TEST_BACKEND" = true ]; then
    echo "Running backend linting..."
    cd ../backend
    
    # Activate virtual environment
    if [ -f "venv/bin/activate" ]; then
      source venv/bin/activate
    elif [ -f "venv/Scripts/activate" ]; then
      source venv/Scripts/activate
    fi
    
    # Run flake8
    if command_exists flake8; then
      echo "Running flake8..."
      flake8 app
    else
      echo "Warning: flake8 not found, skipping backend linting"
    fi
    
    cd ../scripts
  fi
  
  # Frontend linting
  if [ "$TEST_FRONTEND" = true ]; then
    echo "Running frontend linting..."
    cd ../frontend
    
    # Run ESLint
    echo "Running ESLint..."
    npm run lint
    
    cd ../scripts
  fi
}

# Main execution
echo "Starting tests..."

# Run backend tests if enabled
if [ "$TEST_BACKEND" = true ]; then
  run_backend_tests
  BACKEND_EXIT_CODE=$?
else
  BACKEND_EXIT_CODE=0
  echo "Skipping backend tests"
fi

# Run frontend tests if enabled
if [ "$TEST_FRONTEND" = true ]; then
  run_frontend_tests
  FRONTEND_EXIT_CODE=$?
else
  FRONTEND_EXIT_CODE=0
  echo "Skipping frontend tests"
fi

# Run linting
run_linting

# Check exit codes
if [ $BACKEND_EXIT_CODE -ne 0 ] || [ $FRONTEND_EXIT_CODE -ne 0 ]; then
  echo "Tests failed!"
  exit 1
else
  echo "All tests passed!"
  exit 0
fi
