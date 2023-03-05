from sqlalchemy.orm import Session, selectinload
from fastapi import HTTPException, status

from services.order_service.order_model import CreateBaseOrder
from database.models import OrderDetails, OrderItems, Client, PaymentDetails
from services.product_service.product import check_if_product_exists, check_products_amount_and_return_data, update_product_amount


def create(request: CreateBaseOrder, db: Session):
    check_if_product_exists(request.products, db)
    product_for_withdraw = check_products_amount_and_return_data(request.products, db)
    new_order = OrderDetails(
        client_id=request.client_id,
        total=request.total,
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for product in product_for_withdraw:
        update_product_amount(product.id, product.amount_to_withdraw, db)
        new_order_items = OrderItems(
            order_id=new_order.id,
            product_id=product.id,
            amount=product.amount_to_withdraw,
            product_price=product.price
        )
        db.add(new_order_items)

    db.commit()
    db.close()

    return request


def get_list(offset: int, limit: int, db: Session):
    orders = db.query(OrderDetails, Client.name, Client.phone, PaymentDetails.status, PaymentDetails.payment_method)\
        .options(selectinload(OrderDetails.order_items))\
        .join(Client, OrderDetails.client_id == Client.id)\
        .outerjoin(PaymentDetails, OrderDetails.id == PaymentDetails.order_id)\
        .order_by(OrderDetails.id).offset(offset).limit(limit).all()
    order_list = [
        {
            "id": order.id,
            "client_name": client_name,
            "client_phone": client_phone,
            "products": order.order_items,
            "total": order.total,
            "status": status,
            "payment_method": payment_method,
            "created_at": order.created_at,
            "updated_at": order.updated_at,
        }
        for order, client_name, client_phone, status, payment_method in orders
    ]
    return order_list


def get_by_id(id: int, db: Session):
    order = db.query(OrderDetails).filter(OrderDetails.id == id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Order with id {id} not found")
    return order


def delete(id: int, db: Session):
    order_details = db.query(OrderDetails).filter(OrderDetails.id == id)
    if not order_details.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Order with id {id} not found")

    order_items = db.query(OrderItems).filter(OrderItems.order_id == id)

    for order in order_items:
        print(f"product id: {order.product_id} with amount {-order.amount}")
        update_product_amount(order.product_id, -order.amount, db)

    order_items.delete(synchronize_session=False)
    order_details.delete(synchronize_session=False)
    db.commit()

    return status.HTTP_204_NO_CONTENT
