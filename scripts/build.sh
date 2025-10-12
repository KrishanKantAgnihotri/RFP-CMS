#!/bin/bash

# Build script for RFP Contract Management System
# This script builds both the backend and frontend for production

# Configuration
BUILD_DIR="../build"

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

# Create build directory
echo "Creating build directory..."
mkdir -p $BUILD_DIR

# Build backend
echo "Building backend..."
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
  exit 1
fi

# Install backend dependencies
echo "Installing backend dependencies..."
pip install -r requirements.txt

# Copy backend files to build directory
echo "Copying backend files to build directory..."
mkdir -p $BUILD_DIR/backend
cp -r app $BUILD_DIR/backend/
cp -r requirements.txt $BUILD_DIR/backend/

# Build frontend
echo "Building frontend..."
cd ../frontend

# Install frontend dependencies
echo "Installing frontend dependencies..."
npm install

# Build frontend
echo "Building frontend for production..."
npm run build

# Copy frontend build to build directory
echo "Copying frontend build to build directory..."
mkdir -p $BUILD_DIR/frontend
cp -r build/* $BUILD_DIR/frontend/

# Copy scripts
echo "Copying scripts..."
mkdir -p $BUILD_DIR/scripts
cp ../scripts/*.sh $BUILD_DIR/scripts/

# Copy documentation
echo "Copying documentation..."
mkdir -p $BUILD_DIR/docs
cp ../docs/*.md $BUILD_DIR/docs/

# Create .env.example file
echo "Creating .env.example file..."
cp ../backend/.env.example $BUILD_DIR/backend/

# Create README
echo "Creating README..."
cp ../README.md $BUILD_DIR/

echo "Build completed successfully!"
echo "Build files are in $BUILD_DIR"
