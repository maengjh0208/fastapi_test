from dataclasses import asdict

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.database.conn import db
from app.common.config import conf
from app.middlewares.token_validator import access_control
from app.routes import healthcheck, users

API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)


def create_app():
    """
    앱 함수 실행
    :return:
    """
    c = conf()
    app = FastAPI()
    conf_dict = asdict(c)

    # DB init
    db.init_app(app, **conf_dict)

    # 미들웨어 정의
    app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=conf().ALLOW_SITE,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 라우터 정의
    app.include_router(healthcheck.router, tags=["HealthCheck"])
    app.include_router(users.router, tags=["Users"])
    # app.include_router(auth.router, tags=["Authentication"], prefix="/api")
    # app.include_router(users.router, tags=["Users"], prefix="/api", dependencies=[Depends(API_KEY_HEADER)])
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=conf().DEBUG)
