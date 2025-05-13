from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from ..schemas import RegisterRequest, NicknameRequest, JoinGameRequest, QuestionRequest, AnswerRequest, RegisterResponse, AnswerResponse
from ..db.session import get_db
from ..db.models import User, Game, GamePlayer, Question
from ..cache.question_cache import get_question_cache, set_question_cache
import uuid

router = APIRouter()

@router.post("/users/register", response_model=RegisterResponse)
async def register_user(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    # 檢查是否有重複的 username
    existing_user = await db.execute(
        select(User).where(User.username == request.username)
    )
    if existing_user.scalar():
        raise HTTPException(status_code=400, detail="Username already exists")

    # 建立新用戶
    new_user = User(username=request.username, password=request.password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    token = f"token-{new_user.id}"  # 模擬 token
    return RegisterResponse(user_id=new_user.id, token=token)

@router.put("/users/{user_id}/nickname")
async def set_nickname(user_id: int, request: NicknameRequest, db: AsyncSession = Depends(get_db)):
    # 查找用戶
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # 更新暱稱
    user.nickname = request.nickname
    await db.commit()
    await db.refresh(user)
    return {"user_id": user_id, "nickname": user.nickname}

@router.post("/games/{game_id}/join")
async def join_game(game_id: int, request: JoinGameRequest, db: AsyncSession = Depends(get_db)):
    # 確認用戶是否存在
    user = await db.get(User, request.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # 查找或建立遊戲
    game = await db.get(Game, game_id)
    if not game:
        game = Game(id=game_id, name=f"Game-{game_id}")
        db.add(game)
        await db.commit()
        await db.refresh(game)

    # 確認玩家是否已加入遊戲
    existing_player = await db.execute(
        select(GamePlayer).where(GamePlayer.game_id == game_id, GamePlayer.user_id == request.user_id)
    )
    if existing_player.scalar():
        raise HTTPException(status_code=400, detail="User already in game")

    # 加入遊戲
    new_player = GamePlayer(game_id=game_id, user_id=request.user_id, score=0)
    db.add(new_player)
    await db.commit()

    session_id = str(uuid.uuid4())  # 模擬 session ID
    return {"game_id": game_id, "session_id": session_id}

@router.post("/games/{game_id}/questions")
async def publish_question(game_id: int, request: QuestionRequest, db: AsyncSession = Depends(get_db)):
    # 查找遊戲
    game = await db.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")

    # 新增問題
    question_id = str(uuid.uuid4())
    new_question = Question(
        id=question_id,
        game_id=game_id,
        question=request.question,
        options=request.options,
        time_limit=request.time_limit
    )
    db.add(new_question)
    await db.commit()
    await db.refresh(new_question)

    # 將問題存入 Redis 快取
    question_data = {
        "id": question_id,
        "question": new_question.question,
        "options": new_question.options,
        "time_limit": new_question.time_limit
    }
    await set_question_cache(game_id, question_id, question_data)

    return {
        "game_id": game_id,
        "question_id": question_id,
        "question": new_question.question,
        "options": new_question.options,
        "time_limit": new_question.time_limit
    }

@router.get("/games/{game_id}/questions/{question_id}")
async def get_question(game_id: int, question_id: str, db: AsyncSession = Depends(get_db)):
    # 嘗試從 Redis 快取中獲取題目
    cached_question = await get_question_cache(game_id, question_id)
    if cached_question:
        return cached_question

    # 如果快取中沒有，從資料庫查詢
    question = await db.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")

    # 將查詢結果存入 Redis 快取
    question_data = {
        "id": question.id,
        "question": question.question,
        "options": question.options,
        "time_limit": question.time_limit
    }
    await set_question_cache(game_id, question_id, question_data)

    return question_data

@router.delete("/games/{game_id}/players/{player_id}/leave")
async def leave_game(game_id: int, player_id: int, db: AsyncSession = Depends(get_db)):
    # 查找遊戲
    game = await db.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")

    # 查找玩家
    player = await db.execute(
        select(GamePlayer).where(GamePlayer.game_id == game_id, GamePlayer.user_id == player_id)
    )
    player = player.scalar()
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not in game")

    # 移除玩家
    await db.delete(player)
    await db.commit()

    return {"game_id": game_id, "player_id": player_id, "status": "left"}

@router.post("/games/{game_id}/questions/{question_id}/answer", response_model=AnswerResponse)
async def submit_answer(game_id: int, question_id: str, request: AnswerRequest, db: AsyncSession = Depends(get_db)):
    # 查找遊戲
    game = await db.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")

    # 查找玩家
    player = await db.execute(
        select(GamePlayer).where(GamePlayer.game_id == game_id, GamePlayer.user_id == request.player_id)
    )
    player = player.scalar()
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not in game")

    # 嘗試從 Redis 快取中獲取問題
    cached_question = await get_question_cache(game_id, question_id)
    if cached_question:
        question = cached_question
    else:
        # 如果快取中沒有，從資料庫查詢
        question = await db.get(Question, question_id)
        if not question:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")

        # 將查詢結果存入 Redis 快取
        question_data = {
            "id": question.id,
            "question": question.question,
            "options": question.options,
            "time_limit": question.time_limit
        }
        await set_question_cache(game_id, question_id, question_data)

    # 判斷答案是否正確
    correct_option = question["options"][0] if isinstance(question, dict) else question.options[0]  # 假設正確答案為 options[0]
    is_correct = (request.selected_option == correct_option)

    # 更新分數
    if is_correct:
        player.score += 10
        await db.commit()
        await db.refresh(player)

    return AnswerResponse(correct=is_correct, current_score=player.score)