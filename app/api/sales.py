import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.product import Product
from app.models.sale import Sale, SaleItem
from app.schemas.sale import SaleCreate, SaleResponse

router = APIRouter(prefix="/sales", tags=["sales"])

TENANT_ID = "demo"


@router.post("/", response_model=SaleResponse, status_code=201)
async def create_sale(
    payload: SaleCreate,
    db: AsyncSession = Depends(get_db),
) -> Sale:
    product_ids = [item.product_id for item in payload.items]
    result = await db.execute(
        select(Product).where(Product.id.in_(product_ids), Product.tenant_id == TENANT_ID)
    )
    products = {p.id: p for p in result.scalars().all()}

    # Validate all products exist and have enough stock
    sale_items: list[SaleItem] = []
    total = 0

    for item in payload.items:
        product = products.get(item.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Not enough stock for {product.name}: "
                    f"{product.stock} available, {item.quantity} requested"
                ),
            )

        subtotal = product.price * item.quantity
        total += subtotal

        sale_items.append(
            SaleItem(
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=product.price,
                subtotal=subtotal,
            )
        )

        # Decrease stock
        product.stock -= item.quantity

    sale = Sale(
        tenant_id=TENANT_ID,
        total=total,
        notes=payload.notes,
        items=sale_items,
    )
    db.add(sale)
    await db.flush()

    # Reload with items
    result = await db.execute(
        select(Sale).where(Sale.id == sale.id).options(selectinload(Sale.items))
    )
    return result.scalar_one()


@router.get("/{sale_id}", response_model=SaleResponse)
async def get_sale(
    sale_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> Sale:
    result = await db.execute(
        select(Sale)
        .where(Sale.id == sale_id, Sale.tenant_id == TENANT_ID)
        .options(selectinload(Sale.items))
    )
    sale = result.scalar_one_or_none()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale
