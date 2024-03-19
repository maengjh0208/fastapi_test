import re
from typing import Optional
from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.database.schema import Member
from app.models import UserRegister, Token
from app.database.conn import db
from app.common.consts import JWT_SECRET, JWT_ALGORITHM, JWT_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix='/users')


@router.post("/signup", status_code = 200, response_model=Token)
async def signup(regist_info: UserRegister, session: Session = Depends(db.session)):
    # 회원가입시 전달받는 변수
    email = regist_info.email.strip()
    password = regist_info.password
    nickname = regist_info.nickname.strip()

    # 유효성 검사
    if not email or not password:
        return JSONResponse(status_code=400, content=dict(msg="email or password must be provided"))
    if not is_email_valid(email):
        return JSONResponse(status_code=400, content=dict(msg="email is not valid"))
    if await is_email_exist(email):
        return JSONResponse(status_code=400, content=dict(msg="email already exists"))

    # 비밀번호 암호화
    hash_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # 유저 생성
    Member.create(session, auto_commit=True, email=email, password=hash_password, nickname=nickname)

    # 토큰 전달
    token = create_access_token(data={"email": email}, expires_delta=JWT_TOKEN_EXPIRE_MINUTES)
    return Token(Authorization=f"Bearer {token}")


def is_email_valid(email: str) -> bool:
    regex_email = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9._]+[@][a-zA-Z][A-Za-z.]+[.]\w{2,}')
    return True if re.fullmatch(regex_email, email) else False


async def is_email_exist(email: str):
    get_email = Member.get(email=email)
    return True if get_email else False


def create_access_token(*, data: Optional[dict] = None, expires_delta: int = None):
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp": datetime.utcnow() + timedelta(hours=expires_delta)})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt