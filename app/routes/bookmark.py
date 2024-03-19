from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.database.conn import db
from app.database.schema import BookmarkFolder
from app.models import BookmarkFolderInfo, NormalResponse

router = APIRouter(prefix='/bookmark')


@router.post("/folder", status_code=200, response_model=NormalResponse)
async def bookmark_folder(request: Request, folder_info: BookmarkFolderInfo, session: Session = Depends(db.session)):
    member_no = request.state.user.member_no
    folder_name = folder_info.folder_name.strip()[:10]  # 편의상 찜 서랍 이름은 10 자리까지만 허용하기로

    # 이미 존재하는 이름으로 생성 불가
    folder = BookmarkFolder.get(member_no=member_no, folder_name=folder_name)
    if folder:
        return JSONResponse(status_code=400, content=dict(msg="user already has same folder_name"))

    # 찜 폴더 생성
    BookmarkFolder.create(session, auto_commit=True, member_no=member_no, folder_name=folder_name)

    return NormalResponse(success=True, message="The bookmark folder has been successfully created")


@router.get("/folders", status_code=200)
async def get_bookmark_folders(request: Request):
    member_no = request.state.user.member_no

