from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import chess
from pydantic import BaseModel
import secrets

# Configuration
SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class MoveRequest(BaseModel):
    move: str  # e2e4
    color: str  # "white" or "black"

class GameResponse(BaseModel):
    game_id: str
    token: str

class MoveResponse(BaseModel):
    valid: bool
    error: Optional[str] = None

class CheckmateResponse(BaseModel):
    winner: Optional[str] = None  # "white", "black", or None

games = {}  # Dictionary to store game states

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/create-game", response_model=GameResponse)
async def create_game():
    game_id = secrets.token_hex(8)
    games[game_id] = chess.Board()
    token = create_access_token({"sub": game_id})
    return {"game_id": game_id, "token": token}

@app.post("/move", response_model=MoveResponse)
async def make_move(move_request: MoveRequest, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        game_id = payload.get("sub")
        game = games.get(game_id)
        
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
            
        # Convert move to UCI format if needed
        move = chess.Move.from_uci(move_request.move)
        
        # Validate move
        if move not in game.legal_moves:
            return {"valid": False, "error": "Illegal move"}
            
        # Check if it's the correct player's turn
        if (game.turn == chess.WHITE and move_request.color != "white") or \
           (game.turn == chess.BLACK and move_request.color != "black"):
            return {"valid": False, "error": "Not your turn"}
            
        # Make the move
        game.push(move)
        return {"valid": True}
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

@app.get("/checkmate", response_model=CheckmateResponse)
async def check_checkmate(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        game_id = payload.get("sub")
        game = games.get(game_id)
        
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
            
        if game.is_checkmate():
            winner = "white" if game.turn == chess.BLACK else "black"
            return {"winner": winner}
        return {"winner": None}
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
