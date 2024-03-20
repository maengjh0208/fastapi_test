import re
from typing import Optional
from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from starlette.requests import Request

from app.database.schema import Member
from app.models import UserRegister, Token, UserLogin, UserInfo
from app.database.conn import db
from app.common.consts import JWT_SECRET, JWT_ALGORITHM, JWT_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix='/users')


@router.post("/signup", status_code=200)
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

    # 이메일 존재 여부 확인
    matching_email = await is_email_exist(email)
    if matching_email["is_exist"]:
        return JSONResponse(status_code=400, content=dict(msg="email already exists"))

    # 비밀번호 암호화
    hash_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # 유저 생성
    Member.create(session, auto_commit=True, email=email, password=hash_password, nickname=nickname)
    return JSONResponse(status_code=200, content=dict(msg="signup was successfully created"))


@router.post("/login", status_code=200, response_model=Token)
async def login(login_info: UserLogin):
    # 로그인 시 전달받는 정보
    email = login_info.email.strip()
    password = login_info.password

    # 유효성 검사
    if not email or not password:
        return JSONResponse(status_code=400, content=dict(msg="email or password must be provided"))
    if not is_email_valid(email):
        return JSONResponse(status_code=400, content=dict(msg="email is not valid"))

    # 이메일 존재 여부 확인
    matching_email = await is_email_exist(email)
    if not matching_email["is_exist"]:
        return JSONResponse(status_code=400, content=dict(msg="email does not exist"))

    # 비밀번호 일치 확인
    is_password_verified = bcrypt.checkpw(password.encode("utf-8"), matching_email["password"])
    if not is_password_verified:
        return JSONResponse(status_code=400, content=dict(msg="password does not correct"))

    # 토큰 전달
    token = create_access_token(data={"member_no": matching_email["member_no"], "email": email})
    return Token(Authorization=f"Bearer {token}")


@router.get("/info", status_code=200, response_model=UserInfo)
async def get_user_info(request: Request):
    member_no = request.state.user.member_no
    user_info = Member.get(member_no=member_no)
    return UserInfo(email=user_info.email, nickname=user_info.nickname)


def is_email_valid(email: str) -> bool:
    regex_email = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9._]+[@][a-zA-Z][A-Za-z.]+[.]\w{2,}')
    return True if re.fullmatch(regex_email, email) else False


async def is_email_exist(email: str) -> dict:
    email_info = {"is_exist": False, "member_no": None, "email": None, "password": None}

    get_email = Member.get(email=email)

    if get_email is not None:
        email_info["is_exist"] = True
        email_info["member_no"] = get_email.member_no
        email_info["email"] = get_email.email
        email_info["password"] = get_email.password

    return email_info


def create_access_token(*, data: Optional[dict] = None, expires_delta: int = JWT_TOKEN_EXPIRE_MINUTES) -> str:
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp": datetime.utcnow() + timedelta(hours=expires_delta)})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt
