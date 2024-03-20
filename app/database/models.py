from sqlalchemy import select

from app.database.conn import db
from app.database.schema import Product, Bookmark


async def get_bookmark_products(member_no: int, folder_no: int, paging_params: dict) -> list[dict]:
    sess = next(db.session())

    query = (
        select(Product)
        .join(Bookmark, Bookmark.product_no == Product.product_no)
        .where(
            Bookmark.member_no == member_no,
            Bookmark.folder_no == folder_no,
        )
        .limit(paging_params["limit"])
        .offset(paging_params["offset"])
    )

    result = sess.execute(query)

    return [
        {
            "product_no": product_obj.product_no,
            "product_name": product_obj.product_name,
            "thumbnail": product_obj.thumbnail,
            "price": product_obj.price,
        }
        for product_obj in result.scalars()
    ]
