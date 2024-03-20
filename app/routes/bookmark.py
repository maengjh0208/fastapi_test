from typing import List

from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.database.conn import db
from app.database.schema import BookmarkFolder, Bookmark, Product
from app.models import BookmarkFolderInfo, NormalResponse, BookmarkFolders, BookmarkProduct

router = APIRouter(prefix='/bookmark')


@router.post("/folder", status_code=200, response_model=NormalResponse)
async def bookmark_folder(request: Request, folder_info: BookmarkFolderInfo, session: Session = Depends(db.session)):
    member_no = request.state.user.member_no
    folder_name = folder_info.folder_name.strip()[:10]  # 편의상 찜 서랍 이름은 10 자리까지만 허용하기로

    # 이미 존재하는 이름으로 생성 불가
    folder = BookmarkFolder.get(member_no=member_no, folder_name=folder_name)
    if folder:
        return JSONResponse(status_code=400, content=dict(msg="User already has same folder_name"))

    # 찜 폴더 생성
    BookmarkFolder.create(session, auto_commit=True, member_no=member_no, folder_name=folder_name)

    return NormalResponse(success=True, message="The bookmark folder was successfully created")


@router.get("/folder", status_code=200, response_model=List[BookmarkFolders])
async def get_bookmark_folders(
    request: Request,
    limit: int = Query(default=100, title="제한 개수"),
    offset: int = Query(default=0, title="시작 개수"),
):
    member_no = request.state.user.member_no
    paging_params = {"limit": limit, "offset": offset}

    folders = BookmarkFolder.filter(None, paging_params, member_no=member_no).all()

    response = []
    for folder in folders:
        response.append(BookmarkFolders(folder_no=folder.folder_no, folder_name=folder.folder_name))

    return response


@router.post("/product", status_code=200, response_model=NormalResponse)
async def bookmark_product(
    request: Request, bookmark_info: BookmarkProduct, session: Session = Depends(db.session)
):
    member_no = request.state.user.member_no
    product_no = bookmark_info.product_no
    folder_no = bookmark_info.folder_no

    # 상품 존재 여부 확인
    if Product.get(product_no=product_no) is None:
        return JSONResponse(status_code=400, content=dict(msg=f"The product does not exist"))

    # 이미 찜한 상품 인지 확인
    bookmark = Bookmark.get(member_no=member_no, product_no=product_no)
    if bookmark is not None:
        return JSONResponse(
            status_code=400,
            content=dict(msg=f"The product is already bookmarkded | folder_no: {bookmark.folder_no}")
        )

    # 해당 찜 서랍 존재 여부 확인 (잘못된 찜 서랍 가져왔는지 여부도 더블 체크됨)
    if BookmarkFolder.get(folder_no=folder_no, member_no=member_no) is None:
        return JSONResponse(status_code=400, content=dict(msg=f"The folder does not exist"))

    # 상품 찜 생성
    Bookmark.create(session, auto_commit=True, member_no=member_no, product_no=product_no, folder_no=folder_no)

    return NormalResponse(success=True, message="The bookmark was successfully created")


@router.delete("/product/{product_no}", status_code=200, response_model=NormalResponse)
async def delete_bookmark_product(
    request: Request, product_no: int = Path(title="상품 번호")
):
    member_no = request.state.user.member_no

    # 찜한 상품인지 확인
    bookmark = Bookmark.get(member_no=member_no, product_no=product_no)
    if bookmark is None:
        return JSONResponse(status_code=400, content=dict(msg=f"The product does not exist in the bookmark folder"))

    # 상품 찜 삭제
    Bookmark.filter(bookmark_no=bookmark.bookmark_no).delete(auto_commit=True)

    return NormalResponse(success=True, message="The bookmark was successfully deleted")

