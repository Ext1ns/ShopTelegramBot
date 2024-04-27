from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from database.models import Tovar

async def orm_add_product(session: AsyncSession, data: dict):
    add = Tovar(
        name=data['name'],
        description=['description'],
        price=float(data['price']),
        image=data['image']
    )
    session.add(add)
    await session.commit()

async def orm_get_products(session: AsyncSession):
    query = select(Tovar)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_product(session: AsyncSession, product_id: int):
    query = select(Tovar).where(Tovar.id == product_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_product(session: AsyncSession, product_id: int, data):
    query = update(Tovar).where(Tovar.id == product_id).values(
        name=data["name"],
        description=data["description"],
        price=float(data["price"]),
        image=data["image"],)
    await session.execute(query)
    await session.commit()


async def orm_delete_product(session: AsyncSession, product_id: int):
    query = delete(Tovar).where(Tovar.id == product_id)
    await session.execute(query)
    await session.commit()