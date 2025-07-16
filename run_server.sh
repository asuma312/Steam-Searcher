#!/bin/bash
source .venv/bin/activate

python run.py &

sleep 3

cd app/frontend
npm run dev

read -p "Press enter to stop the server"