from models.product import Product, db
from flask import jsonify
from typing import Optional
from datetime import datetime


def get_product_by_id(id: int) -> Optional[Product]:
    """
    Get a product by its ID.

    Args:
        id (int): The ID of the product.

    Returns:
        Optional[Product]: The product if it exists, otherwise None.
    """
    return Product.query.filter_by(id=id).first()


def get_all_products() -> list[Product]:
    """
    Retrieve all products from the database.

    Returns:
        list[Product]: A list of all Product objects.
    """
    return Product.query.all()


def create_product(seller_id: int, 
    name: str,
    description: str, 
    price: float, 
    gender: str, 
    size: str, 
    youth_size: bool, 
    featured: bool, 
    brand: str, 
    sport: str, 
    quantity: int, 
    condition: str, 
    image: bytes, 
    date_listed: datetime,
    year_product_made: Optional[str], 
    avg_rating: float
) -> Optional[Product]:
    """
    Create a new product in the database.

    Args:
        seller_id (int): The ID of the seller listing the product.
        name (str): Name of the product.
        description (str): Description of the product.
        price (float): Price of the product.
        gender (str): Target gender for the product.
        size (str): Size of the product.
        youth_size (bool): Whether the product is a youth size.
        featured (bool): Whether the product is featured.
        brand (str): Brand of the product.
        sport (str): Associated sport for the product.
        quantity (int): Quantity of the product available.
        condition (str): Condition of the product.
        image (bytes): Image of the product.
        date_listed (datetime): Date the product was listed.
        year_product_made (Optional[str]): Year the product was made.
        avg_rating (float): Average rating of the product.

    Returns:
        Optional[Product]: The newly created product.
    """
    new_product = Product(
        seller_id=seller_id,
        name=name,
        description=description,
        price=price,
        gender=gender,
        size=size,
        youth_size=youth_size,
        featured=featured,
        brand=brand,
        sport=sport,
        quantity=quantity,
        condition=condition,
        image=image,
        date_listed=date_listed,
        year_product_made=year_product_made,
        avg_rating=avg_rating
    )
    db.session.add(new_product)
    db.session.commit()
    return new_product


def update_product(
    product_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    price: Optional[float] = None,
    gender: Optional[str] = None,
    size: Optional[str] = None,
    youth_size: Optional[bool] = None,
    featured: Optional[bool] = None,
    brand: Optional[str] = None,
    sport: Optional[str] = None,
    quantity: Optional[int] = None,
    condition: Optional[str] = None,
    image: Optional[bytes] = None,
    year_product_made: Optional[str] = None,
    avg_rating: Optional[float] = None
) -> Optional[Product]:
    """
    Update an existing product in the database.

    Args:
        product_id (int): ID of the product to update.
        (Other fields are optional updates)

    Returns:
        Optional[Product]: The updated product, or None if not found.
    """
    product = Product.query.get(product_id)
    if not product:
        return None

    updates = {
        'name': name,
        'description': description,
        'price': price,
        'gender': gender,
        'size': size,
        'youth_size': youth_size,
        'featured': featured,
        'brand': brand,
        'sport': sport,
        'quantity': quantity,
        'condition': condition,
        'image': image,
        'year_product_made': year_product_made,
        'avg_rating': avg_rating
    }

    for field, value in updates.items():
        if value is not None:
            setattr(product, field, value)

    db.session.commit()
    return product


def delete_product(product_id: int) -> str:
    """
    Delete a product from the database.

    Args:
        product_id (int): ID of the product to delete.

    Returns:
        str: Message indicating the result of the operation.
    """
    product = Product.query.get(product_id)
    if not product:
        return "Product with this ID not found"

    db.session.delete(product)
    db.session.commit()
    return "Product deleted successfully"
