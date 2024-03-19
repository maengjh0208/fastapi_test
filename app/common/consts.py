JWT_SECRET = "JUHEE12345"
JWT_ALGORITHM = "HS256"
JWT_TOKEN_EXPIRE_MINUTES = 300

EXCEPT_PATH_LIST = [
    "/healthcheck",
    "/openapi.json",
    "/users/signup",
    "/users/login"
]
EXCEPT_PATH_REGEX = "^(/docs|/redoc)"
