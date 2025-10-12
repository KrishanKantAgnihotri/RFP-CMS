#!/bin/bash

# Deploy script for RFP Contract Management System
# This script deploys the application to various platforms

# Configuration
BUILD_DIR="../build"
DEPLOYMENT_TARGET=${1:-"vercel"}  # Default to vercel if no argument provided

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Check if build directory exists
if [ ! -d "$BUILD_DIR" ]; then
  echo "Error: Build directory not found"
  echo "Please run build.sh first"
  exit 1
fi

# Deploy to Vercel
deploy_to_vercel() {
  echo "Deploying to Vercel..."
  
  # Check for Vercel CLI
  if ! command_exists vercel; then
    echo "Error: Vercel CLI not found"
    echo "Please install it with: npm install -g vercel"
    exit 1
  fi
  
  # Deploy backend
  echo "Deploying backend..."
  cd $BUILD_DIR/backend
  vercel --prod
  
  # Deploy frontend
  echo "Deploying frontend..."
  cd $BUILD_DIR/frontend
  vercel --prod
  
  echo "Vercel deployment completed!"
}

# Deploy to Netlify
deploy_to_netlify() {
  echo "Deploying to Netlify..."
  
  # Check for Netlify CLI
  if ! command_exists netlify; then
    echo "Error: Netlify CLI not found"
    echo "Please install it with: npm install -g netlify-cli"
    exit 1
  fi
  
  # Deploy frontend
  echo "Deploying frontend..."
  cd $BUILD_DIR/frontend
  netlify deploy --prod
  
  echo "Netlify deployment completed!"
  echo "Note: Backend must be deployed separately to a service like Heroku or Railway"
}

# Deploy to Railway
deploy_to_railway() {
  echo "Deploying to Railway..."
  
  # Check for Railway CLI
  if ! command_exists railway; then
    echo "Error: Railway CLI not found"
    echo "Please install it with: npm install -g @railway/cli"
    exit 1
  fi
  
  # Deploy backend
  echo "Deploying backend..."
  cd $BUILD_DIR/backend
  railway up
  
  # Deploy frontend
  echo "Deploying frontend..."
  cd $BUILD_DIR/frontend
  railway up
  
  echo "Railway deployment completed!"
}

# Deploy to Docker
deploy_to_docker() {
  echo "Deploying to Docker..."
  
  # Check for Docker
  if ! command_exists docker; then
    echo "Error: Docker not found"
    echo "Please install Docker first"
    exit 1
  fi
  
  # Check for Docker Compose
  if ! command_exists docker-compose; then
    echo "Error: Docker Compose not found"
    echo "Please install Docker Compose first"
    exit 1
  fi
  
  # Create Docker Compose file if it doesn't exist
  if [ ! -f "$BUILD_DIR/docker-compose.yml" ]; then
    echo "Creating Docker Compose file..."
    cat > $BUILD_DIR/docker-compose.yml << EOL
version: '3'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://mongo:27017
      - MONGODB_DB_NAME=rfp_cms
      - SECRET_KEY=\${SECRET_KEY}
    depends_on:
      - mongo

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  mongo:
    image: mongo:4.4
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db

volumes:
  mongo-data:
EOL
  fi
  
  # Create backend Dockerfile if it doesn't exist
  if [ ! -f "$BUILD_DIR/backend/Dockerfile" ]; then
    echo "Creating backend Dockerfile..."
    cat > $BUILD_DIR/backend/Dockerfile << EOL
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOL
  fi
  
  # Create frontend Dockerfile if it doesn't exist
  if [ ! -f "$BUILD_DIR/frontend/Dockerfile" ]; then
    echo "Creating frontend Dockerfile..."
    cat > $BUILD_DIR/frontend/Dockerfile << EOL
FROM nginx:alpine

COPY . /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
EOL
  fi
  
  # Build and run Docker containers
  cd $BUILD_DIR
  docker-compose up -d
  
  echo "Docker deployment completed!"
  echo "Application is running at http://localhost"
}

# Deploy based on target
case $DEPLOYMENT_TARGET in
  "vercel")
    deploy_to_vercel
    ;;
  "netlify")
    deploy_to_netlify
    ;;
  "railway")
    deploy_to_railway
    ;;
  "docker")
    deploy_to_docker
    ;;
  *)
    echo "Error: Unknown deployment target: $DEPLOYMENT_TARGET"
    echo "Available targets: vercel, netlify, railway, docker"
    exit 1
    ;;
esac
