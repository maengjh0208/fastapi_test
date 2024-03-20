## 실행 방법
1. Pycharm 으로 fastapi_test 프로젝트 파일 열기
2. 가상환경 세팅 (in 터미널)
   3. python3 -m venv <가상환경이름>
   4. source <가상환경이름>/bin/activate
   5. pip install -r requirements.txt
6. Pycharm 에서 main.py 실행 (위치: fastapi_test > app > main.py)

---
## 요구 사항
### 1. 회원가입
1. 이메일과 비밀번호로 회원가입

### 2. 로그인
1. 이메일과 비밀번호로 로그인

### 3. 내(회원) 정보 조회
1. 회원 정보 따로 명시된 것이 없어, 간단히 이메일과 닉네임 정보 조회하여 노출할 예정

### 4. 찜 서랍 추가
1. 찜 서랍은 이름으로 생성 가능
2. 회원이 등록한 찜 서랍 중, 이미 존재하는 이름으로는 생성 불가

### 5. 찜 서랍 삭제
1. 찜 서랍 삭제 시, 해당 서랍에 등록되어 있는 찜 상품이 있을 경우 함께 삭제처리할 예정

### 6. 찜 서랍 목록 조회
1. 페이지네이션 기능 필요
   2. API 호출시 limit, offset 으로 조정 가능

### 7. 상품 찜 추가
1. 특정 찜 서랍 내에 찜 상품을 등록
   2. 즉, 찜 서랍이 하나도 없을 경우 상품 찜 불가
2. 이미 다른 찜 서랍에 있는 상품인 경우 찜 불가

### 8. 상품 찜 삭제

### 9. (특정 찜 서랍에 등록된) 찜 상품 목록 조회
1. 페이지네이션 기능 필요

---
## API 명세서
### 1. 회원가입 (POST /users/signup)

request
```
[body]
- email : (필수), str(이메일) 
- password : (필수), str(비밀번호)
- nickname : (선택), str(닉네임)
```

response (status_code = 200)
```
{ "msg": "signup was successfully created" }
```
 
error case (status_code = 400)
```
1. 이메일 또는 패스워드가 양쪽 공백 제거 했을 때, 빈문자열인 경우
{ "msg": "email or password must be provided" }

2. 이메일 형식이 유효하지 않을 때
{ "msg": "email is not valid" }

3. 해당 이메일이 이미 존재할 때
{ "msg": "email already exists" }
```

### 2. 로그인 (POST /users/login)
request
```
[body]
- email : (필수), str(이메일) 
- password : (필수), str(비밀번호)
```
response (status_code = 200)
```
# 응답값으로 인증 토큰값 전달
# 로그인 이후 회원 기능을 사용할 시, Headers에 해당 토큰 전달 필요 

{
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZW1iZXJfbm8iOjE3LCJlbWFpbCI6Imp1aGVlLmJkYTE2QGdtYWlsLmNvbSIsImV4cCI6MTcxMjAwNzI4Nn0.ebPJVNF4eE_yExapjnS9OSv7Mt4i0fNBRIAUv9xCfug"
}
```
error case (status_code = 400)
```
1. 이메일 또는 패스워드가 양쪽 공백 제거 했을 때, 빈문자열인 경우
{ "msg": "email or password must be provided" }

2. 이메일 형식이 유효하지 않을 때
{ "msg": "email is not valid" }

3. 해당 이메일이 존재하지 않을 때
{ "msg": "email does not exist" }

4. 비밀번호가 일치하지 않을 때
{ "msg": "password does not correct" }
```

### 3. 내(회원) 정보 조회 (GET /users/info)
request
```
[headers]
- Authorization : (필수), str(로그인 응답값으로 받은 토큰정보)

ex)
Authorization : Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZW1iZXJfbm8iOjE3LCJlbWFpbCI6Imp1aGVlLmJkYTE2QGdtYWlsLmNvbSIsImV4cCI6MTcxMjAwNzI4Nn0.ebPJVNF4eE_yExapjnS9OSv7Mt4i0fNBRIAUv9xCfug
```
response (status_code = 200)
```
{
    "email": "juhee.bda16@gmail.com",
    "nickname": "주희10"
}
```

### 4. 찜 서랍 추가 (POST /bookmark/folder)
request
```
[body]
- folder_name : (필수), str(찜 서랍명), 10자 이하로 요청할 것

[headers]
- Authorization : (필수), str(토큰)
```
response (status_code = 200)
```
{ "msg": "The bookmark folder was successfully created" }
```
error case (status_code = 400)
```
1. 동일한 이름의 폴더 이름이 존재 할 때
{ "msg": "User already has same folder_name" }
```

### 5. 찜 서랍 삭제 (DELETE /bookmark/folder/{folder_no})
request
```
[path]
- folder_no : (필수), int(찜 서랍 번호), '찜 서랍 목록 조회 API'에서 조회 가능

[headers]
- Authorization : (필수), str(토큰)
```
response (status_code = 200)
```
# 추가 설명 : 해당 찜 서랍에 등록된 찜 상품이 존재할 경우, 해당 찜 상품도 삭제 처리
{
    "msg": "The bookmark folder & bookmark product were successfully deleted"
}
```
error case (status_code = 400)
```
1. 해당 찜 서랍이 존재하지 않는 경우
{ "msg": "The folder does not exist" }
```

### 6. 찜 서랍 목록 조회 (GET /bookmark/folder)
request
```
[query]
- limit : (선택), int(제한 개수), 기본값 100
- offset : (선택), int(시작 개수), 기본값 0

[headers]
- Authorization : (필수), str(토큰)

# 추가 설명 (페이지네이션)
- offset을 limit만큼 추가로 더해주면서 호출
- 응답값으로 내려온 찜 서랍 개수가 limit 보다 적을 시 더이상 호출하지 않는다.
```
response (status_code = 200)
```
[
    {
        "folder_name": "tes2",  # 찜 서랍 이름
        "folder_no": 13         # 찜 서랍 번호
    },
    {
        "folder_name": "test",
        "folder_no": 10
    }
]
```

### 7. 상품 찜 추가 (POST /bookmark/product)
request
```
[body]
- product_no : (필수), int(상품 번호), (참고: 상품번호는 2 ~ 501 까지 존재합니다.)
- folder_no : (필수), int(찜 서랍 번호)

[headers]
- Authorization : (필수), str(토큰)
```
response (status_code = 200)
```
{ "msg": "The bookmark was successfully created" }
```
error case (status_code = 400)
```
1. 해당 상품이 존재하지 않을 때
{ "msg": "The product does not exist" }

2. 해당 찜 서랍이 존재하지 않을 때
{ "msg": "The folder does not exist" }

3. 이미 찜 등록된 상품인 경우 (다른 찜 서랍에 등록되어 있어도 마찬가지)
{ "msg": "The product is already bookmarkded | folder_no: %(해당 상품이 등록되어 있는 찜 서랍 번호)%" }
```

### 8. 상품 찜 삭제 (DELETE /bookmark/product/{product_no})
request
```
[path]
- product_no : (필수), int(상품 번호) (참고: '찜 상품 목록 조회 API' 에서 상품번호 조회 가능)

[headers]
- Authorization : (필수), str(토큰)
```
response (status_code = 200)
```
{ "msg": "The bookmark was successfully deleted" }
```
error case (status_code = 400)
```
1. 해당 상품이 찜한 상품이 아닌 경우
{ "msg": "The product is not bookmarked" }
```

### 9. (특정 찜 서랍에 등록된) 찜 상품 목록 조회 (GET /bookmark/folder/{folder_no})
request
```
[path]
- folder_no : (필수), int(찜 서랍 번호)

[query]
- limit : (선택), int(제한 개수), 기본값 100
- offset : (선택), int(시작 개수), 기본값 0

[headers]
- Authorization : (필수), str(토큰)
```
response (status_code = 200)
```
# product_no: 상품 번호
# product_name: 상품 명
# thumbnail: 썸네일
# price: 가격

[
    {
        "product_no": 2,
        "product_name": "product_0",
        "thumbnail": "https://image.com/products/thumbnail/product_0.jpeg",
        "price": 140500
    },
    {
        "product_no": 3,
        "product_name": "product_1",
        "thumbnail": "https://image.com/products/thumbnail/product_1.jpeg",
        "price": 18000
    }
]
```
error case (status_code = 400)
```
1. 해당 찜 서랍이 존재하지 않는 경우
{ "msg": "The folder does not exist" }
```