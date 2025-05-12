from app.database import engine, Base, SessionLocal
from app.models import User, UserRole, WasteCategory, WasteInferenceLog
from app.utils.hashing import hash_password

print("Creating database tables...")
Base.metadata.create_all(bind=engine)

# Predefined roles
roles = ["admin", "user"]

# Predefined users
users = [
    {"username": "admin1", "password": hash_password("adminpass1"), "role": "admin"},
    {"username": "admin2", "password": hash_password("adminpass2"), "role": "admin"},
    {"username": "user1", "password": hash_password("userpass1"), "role": "user"},
    {"username": "user2", "password": hash_password("userpass2"), "role": "user"}
]

# Predefined waste categories
categories = [
    {"name": "Plastic", "description": "Plastic waste materials."},
    {"name": "Glass", "description": "Glass waste materials."},
    {"name": "Metal", "description": "Metal waste materials."},
    {"name": "Paper", "description": "Paper and cardboard materials."},
    {"name": "Organic", "description": "Organic waste like food scraps."}
]

with SessionLocal() as session:
    # Add roles
    for role in roles:
        db_role = UserRole(name=role)
        session.add(db_role)
    session.commit()

    # Add users
    for user in users:
        role_id = session.query(UserRole).filter_by(name=user["role"]).first().id
        db_user = User(username=user["username"], password=user["password"], role_id=role_id)
        session.add(db_user)
    session.commit()

    # Add waste categories
    for category in categories:
        db_category = WasteCategory(name=category["name"], description=category["description"])
        session.add(db_category)
    session.commit()

print("Database tables and initial data created successfully.")