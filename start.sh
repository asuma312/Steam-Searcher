#!/bin/bash
source .venv/bin/activate

echo "Updating database..."
python kaggle_collector.py
echo "Finished database update..."
echo "Starting the backend-server..."
python run.py &
echo "Finished backend-server..."
echo "Starting the frontend-server..."

cd app/frontend
npm run dev

read -p "Press enter to stop the server"