from sqlalchemy import Column, String, Integer, ForeignKey, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped
import uuid
from app.database import Base

class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)

    user = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role_id = Column(UUID(as_uuid=True), ForeignKey("user_roles.id"))

    role: Mapped["UserRole"]= relationship("UserRole", back_populates="user")

    def get_token_data(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "role": {
                "id": str(self.role.id),
                "name": self.role.name
            }
        }

class WasteCategory(Base):
    __tablename__ = "waste_categories"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    description = Column(String)

    waste_logs: Mapped["WasteInferenceLog"] = relationship("WasteInferenceLog", back_populates="category")

class WasteInferenceLog(Base):
    __tablename__ = "waste_inference_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id = Column(UUID(as_uuid=True), ForeignKey("waste_categories.id"))
    probability = Column(Float)
    value = Column(String)
    timestamp = Column(DateTime)

    category: Mapped["WasteCategory"] = relationship("WasteCategory", back_populates="waste_logs")

    def to_dict(self):
        return {
            "id": self.id,
            "probability": self.probability,
            "value": self.value,
            "timestamp": self.timestamp,
            "category": self.category.name,
            "category_description": self.category.description
        }