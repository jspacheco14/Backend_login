# Waste Inference API

## Description
A FastAPI application to store waste inference logs received from an external AI system. The application uses JWT for authentication and PostgreSQL as the database.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/username/fastapi-waste-inference.git
   cd fastapi-waste-inference
   ```

2. Install the dependencies using UV:
   ```bash
   uv sync
   ```

   Or if you don't have UV installed, use pip:
   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg2-binary passlib python-jose pydantic
   ```

3. Create a `.env` file with the following content:
   ```bash
   DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/waste_db
   JWT_SECRET_KEY=supersecretkey
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. Run the database initialization script:
   ```bash
   python init_db.py
   ```

5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints
- **Login**: `/auth/login` - Authenticate and get a JWT token.
- **Create Waste Log**: `/waste` (POST) - Store a new waste inference.
- **Get Waste Logs**: `/waste` (GET) - Retrieve all waste inferences.
- **Create Waste Category**: `/category` (POST) - Add a new waste category.
- **Get Waste Categories**: `/category` (GET) - List all waste categories.

## Testing
Use a tool like Postman or curl to test the endpoints.

## License
MIT License