#!/bin/bash
source ./venv/bin/activate

# Change into backend folder first
cd backend

echo "🚀 Starting FastAPI backend..."
uvicorn app.main:app --reload &
cd ..

sleep 2

echo "🌐 Starting Streamlit frontend..."
streamlit run delivery_frontend/app.py


#./run_app.sh

streamlit run backend/delivery_frontend/app.py

#streamlit run dorm-delivery-app/delivery_frontend/app.py

