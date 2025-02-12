from fastapi import FastAPI
from referral_system.routers import auth, referral, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(referral.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Referral System API"}