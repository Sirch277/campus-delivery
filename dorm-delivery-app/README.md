Dorm Delivery App

A university dorm delivery management system built with FastAPI (backend) and Next.js (frontend).
Designed for dorm students to request, track, and manage deliveries easily.


⚙️ Setup & Installation


1️⃣ Clone the repository:

    git clone https://github.com/protaatoo/dorm-delivery-app.git
    cd dorm-delivery-app

2️⃣ Backend setup

    cd backend
    pip install -r requirements.txt


Run the backend:
    uvicorn backend.app.main:app --reload

Backend will start at http://127.0.0.1:8000

3️⃣ Frontend setup:

    cd ../frontend
    npm install
    npm run dev

Frontend runs at http://localhost:3000


👥 User Roles:
🧍‍♂️ Customer:

- Register and log in

- Create delivery requests

- Track status (pending, in progress, completed)

🚴‍♂️ Delivery Driver:

- Register as a delivery person

- Accept or complete delivery tasks

- Manage active deliveries

🧑‍💼 Admin Access

Login credentials for admin panel:

    Email: admin@example.com
    Password: adminpassword

Admin can view:

- Total users

- Total and active deliveries

- Pending / In progress deliveries

- Held payments

🧠 Development Workflow

When you make changes:

    git add .
    git commit -m "Describe your update"
    git push

To sync new updates from the repo:

    git pull
