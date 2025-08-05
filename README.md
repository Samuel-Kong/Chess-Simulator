# Chess Simulator API

A RESTful API for playing chess games with JWT authentication.

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python3 -m uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## API Endpoints

### 1. Create Game
`POST /create-game`

Creates a new chess game and returns a JWT token for authentication.

Response:
```json
{
    "game_id": "string",
    "token": "jwt_token"
}
```

### 2. Make Move
`POST /move`

Submit a chess move for validation and execution.

Request Body:
```json
{
    "move": "e2e4",
    "color": "white"
}
```

Response:
```json
{
    "valid": true,
    "error": "string"
}
```

### 3. Check Checkmate
`GET /checkmate`

Checks if the game is in checkmate.

Response:
```json
{
    "winner": "white"
}
```

## Authentication

All endpoints except `/create-game` require a valid JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Example Usage

1. Create a new game:
```bash
curl -X POST http://127.0.0.1:8000/create-game
```

2. Make a move:
```bash
curl -X POST \
  http://127.0.0.1:8000/move \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"move": "e2e4", "color": "white"}'
```

3. Check for checkmate:
```bash
curl -X GET \
  http://127.0.0.1:8000/checkmate \
  -H "Authorization: Bearer <your_token>"
```

## Development

The API is built using:
- FastAPI for the web framework
- python-chess for chess game logic
- python-jose for JWT authentication
- uvicorn as the ASGI server

## API Documentation

Interactive API documentation is available at:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
