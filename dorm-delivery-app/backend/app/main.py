from fastapi import FastAPI
from app.core.database import engine, Base
from app.api.routes import auth, users, deliveries, admin
from fastapi.middleware.cors import CORSMiddleware

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dorm Delivery App - Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(deliveries.router, prefix="/api/delivery", tags=["delivery"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])

@app.get("/")
def root():
    return {"msg": "Dorm Delivery Backend is alive"}
