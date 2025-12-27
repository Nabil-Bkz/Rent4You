#!/bin/bash

# Rent4You Frontend Setup Script

echo "Setting up Rent4You Frontend..."

# Install dependencies
echo "Installing dependencies..."
npm install

# Set up environment variables
if [ ! -f .env.local ]; then
    echo "Creating .env.local file..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api" > .env.local
    echo "Environment file created. Edit .env.local if needed."
fi

echo "Setup complete!"
echo "To start the development server, run: npm run dev"

