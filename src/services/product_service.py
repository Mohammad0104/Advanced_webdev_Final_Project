from models.product import Product, db
from flask import jsonify
from typing import Optional
from datetime import datetime

def get_product_by_id(id: int) -> Optional[Product]:
    """Get a product by id

    Args:
        id (int): the id of the product to get

    Returns:
        Optional[Product]: The product if a product of the specified id exists
    """
    product = Product.query.filter_by(id=id).first()
    return product

def create_product(
    seller_id: int, 
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
    image: str, 
    date_listed: datetime,
    year_product_made: Optional[str], 
    avg_rating: float) -> Optional[Product]:
    """Create a new product in the db

    Args:
        seller_id (int): id of the user selling/listing the product
        name (str): name of the product 
        description (str): description of the product
        price (float): price of the product
        gender (str): gender the product was made for (M, F, Uni-sex)
        size (str): size of the product (XS, S, M, L, XL)
        youth_size (bool): if the product is a youth size (True) or adult size (False)
        featured (bool): if the product is featured
        brand (str): product brand
        sport (str): sport(s) of the product
        quantity (int): the amount of the product listed (default=1 initially)
        condition (str): the condition of the product (how used it is: practically new, lightly used, moderately used, heavily used)
        image (str): image url for the product
        date_listed (datetime): datetime the product was listed
        year_product_made (Optional[str]): year the product was originally made (can be null)
        avg_rating (float): average of the ratings given to the product by user reviews (out of 5.0)

    Returns:
        Optional[Product]: the new product created
    """
    product_data = {
        'seller_id': seller_id,
        'name': name,
        'description': description,
        'price': price,
        'gender': gender,
        'size': size,
        'youth_size': youth_size,
        'featured': featured,
        'brand': brand,
        'sport': sport,
        'condition': condition,
        'image': image,
        'date_listed': date_listed,
        'year_product_made': year_product_made,
        'avg_rating': avg_rating
    }
    
    # add quantity to product_data if quantity is not None or 1
    if quantity is not None and quantity is not 1:
        product_data['quantity'] = quantity
    
    # create Product object
    new_product = Product(**product_data)
    
    # add Product to db and commit
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
    youth_product: Optional[bool] = None,
    featured: Optional[bool] = None,
    brand: Optional[str] = None,
    sport: Optional[str] = None,
    quantity: Optional[int] = None,
    condition: Optional[str] = None,
    image: Optional[str] = None,
    date_listed: Optional[datetime] = None,
    year_product_made: Optional[str] = None,
    avg_rating: Optional[float] = None
) -> Product | str:
    
    product = Product.query.get(product_id)
    
    # if product with the given id is not found
    if product is None:
        return "Product with this id not found"
    
    # dictionary of fields to update
    updates = {
        'name': name,
        'description': description,
        'price': price,
        'gender': gender,
        'size': size,
        'youth_product': youth_product,
        'featured': featured,
        'brand': brand,
        'sport': sport,
        'quantity': quantity,
        'condition': condition,
        'image': image,
        'date_listed': date_listed,
        'year_product_made': year_product_made,
        'avg_rating': avg_rating
    }
    
    # loop over dictionary and update fields if not None
    for field, value in updates.items():
        if value is not None:
            setattr(product, field, value) # set the value for the field in product
    
    # commit changes
    db.session.commit()
    
    return product

def delete_product(product_id: int) -> str:
    """Delete product from the db

    Args:
        product_id (int): id of the product to delete

    Returns:
        str: message if product was deleted
    """
    product = Product.query.get(product_id)
    
    # if no product with the given id is found
    if not Product:
        return "Product with this id not found"

    # delete product from db
    db.session.delete(product)
    
    # commit changes
    db.session.commit()
    
    return "Product was deleted successfully"