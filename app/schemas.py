from pydantic import BaseModel
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    username: str
    password: str

class WasteLogCreate(BaseModel):
    category_id: str
    probability: float
    value: str
    timestamp: datetime

class WasteCategoryCreate(BaseModel):
    name: str
    description: str