# Proof of Resolution Backend

This directory contains the FastAPI-driven backend for the Proof of Resolution application. It implements a custom blockchain for immutable storage of data.

## Features

- **Custom Blockchain:** Implements a SHA-256 based blockchain with proof-of-work.
- **Data Persistence:** Uses SQLite (SQLAlchemy-ready) to store the blockchain and user data.
- **RESTful API:** Developed with FastAPI for high performance and automatic documentation.
- **Secure Authentication:** JWT-based user authentication and route protection.
- **Validation:** Pydantic models for request/response validation.
## API Responses
I added some fun API response message formats. Not convention but fun.
## Directory Structure

- `BlockChain/`: Core blockchain business logic and mining implementation.
- `CaesarSQLDB/`: Database interaction layer (CRUD operations and table creation).
- `CaesarJWT/`: JWT generation and validation logic.
- `routers/`: API route definitions (auth, blockchain, resolutions).
- `models/`: Pydantic DTOs and request/response schemas.
- `services/`: Business logic layer.
- `tests/`: Automated end-to-end and unit tests.

## Local Development

### Environment Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) Create a `.env` file based on `.env.example`.

### Running the Application
```bash
python main.py
```
The server will start on `http://localhost:8080`.

## Docker Usage

Build and run locally:
```bash
./build_app.sh --local
```

## Testing
Execute tests using the build script:
```bash
./build_app.sh --test
```
Or manually via pytest:
```bash
pytest
```
