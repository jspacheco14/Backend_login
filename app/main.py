from fastapi import FastAPI
from app.routers import auth, waste

app = FastAPI(title="Waste Inference API")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(waste.router, prefix="/waste", tags=["Waste"])

@app.get("/")
def root():
    return {"message": "Welcome to the Waste Inference API"}