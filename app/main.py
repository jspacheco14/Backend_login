from fastapi import FastAPI
from app.routers import auth, waste
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Waste Inference API")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(waste.router, prefix="/waste", tags=["Waste"])

@app.get("/")
def root():
    return {"message": "Welcome to the Waste Inference API"}