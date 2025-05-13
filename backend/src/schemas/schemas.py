from pydantic import BaseModel
from typing import List, Optional

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: Optional[str] = None

class NicknameRequest(BaseModel):
    nickname: str

class JoinGameRequest(BaseModel):
    user_id: str

class QuestionRequest(BaseModel):
    question: str
    options: List[str]
    time_limit: int

class AnswerRequest(BaseModel):
    player_id: str
    selected_option: str
