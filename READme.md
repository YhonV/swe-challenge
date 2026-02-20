# User Management API

RESTful API for user management built with FastAPI and PostgreSQL. Supports full CRUD operations for users with role-based assignments.

- You can interact with the endpoints through this url: https://user-management-api-240812885363.us-central1.run.app/docs#/

---
## Architecture

The project follows a **Layered Architecture** pattern, separating responsibilities across distinct layers:

```
app/
├── api/v1/          # Controllers 		— receives HTTP requests and delegates to services
├── services/        # Business Logic 	— handles CRUD operations and validations
├── db/              # Data Layer 		— SQLAlchemy models and database connection
├── schemas/         # DTOs 			— Pydantic models for request/response validation
└── core/            # Cross-cutting 	— configuration and logging
```

Each layer only communicates with the layer directly below it, making the codebase easy to test, maintain, and scale.

---

## Tech Stack

| Technology 		| Version 	| Purpose 		|
|-------------------|-----------|---------------|
| Python 			| 3.9 		| Runtime 		|
| FastAPI 			| 0.128.x 	| Web framework |
| SQLAlchemy		| 2.0.x 	| ORM (async) 	|
| PostgreSQL		| 18 		| database 		|
| Pydantic 			| 2.x 		| Data 			|
| asyncpg 			| 0.31.x 	| Async driver 	|
| pytest 			| 8.x 		| Testing 		|
| httpx 			| 0.28.x 	| Async tests 	|
| Docker 			| — 		| Containerization |
| Google Cloud Run | — 			| Deployment 	|
| Google Cloud Build | — 		| CI/CD pipeline|

---

## Requirements

- Python 3.9+
- PostgreSQL 14+ (or Postgres.app for local development)
- pip

---

## Local Setup

**1. Clone the repository**
```bash
git clone https://github.com/YhonV/swe-challenge.git
cd swe-challenge
```

**2. Create and activate virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

**5. Start the application**
```bash
fastapi dev app/main.py
```

**6. Access the API**
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## Environment Variables

Create a `.env` file in the root of the project:

```env
DATABASE_URL=postgresql+asyncpg://username@localhost:5432/users_db
```

---
## API Endpoints

Base URL: `/api/v1`

| Method 	| Endpoint 			| Description 		| Status Codes 	|
|---|-------|-------------------|-------------------|--------------	|
| `GET` 	| `/users/` 		| Get all users 	| 200 			|
| `GET` 	| `/users/{user_id}`| Get a user by ID 	| 200, 404 		|
| `POST` 	| `/users/` 		| Create a new user | 200, 409, 422 |
| `PUT` 	| `/users/{user_id}`| Update a user 	| 200, 404, 422 |
| `DELETE` 	| `/users/{user_id}`| Delete a user 	| 204, 404 		|

### User Roles
Accepted values for the `role` field: `admin`, `user`, `guest`

### Example: Create a User
```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "user",
    "active": true
  }'
```

## Running Tests

Tests use an isolated SQLite in-memory database, so no PostgreSQL connection is needed.

```bash
pytest tests/ -v
```

## Deployment

The API is deployed on **Google Cloud Run** and available at:

```
https://user-management-api-240812885363.us-central1.run.app/docs
```

### CI/CD Pipeline (Cloud Build)

The `cloudbuild.yaml` defines a 4-step pipeline that runs automatically on every push to `main`:

| Step 	| Description 									|
|-------|-----------------------------------------------|
| 1 	| Install dependencies and run pytest tests 	|
| 2 	| Build Docker image and tag with commit SHA 	|
| 3 	| Push Docker image to Google Artifact Registry |
| 4 	| Deploy to Cloud Run with latest image 		|

### Manual Deploy
```bash
gcloud builds submit --config cloudbuild.yaml
```
---

## Production Considerations

- SQLite is used only for testing. Production uses PostgreSQL via Supabase.