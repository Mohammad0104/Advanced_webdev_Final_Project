from flask import Blueprint, request, jsonify, abort
from datetime import datetime
from services.product_service import create_product
from models.product import Product

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/create_product', methods=['POST'])
def create_new_product():
    data = request.get_json()

    seller_id = data.get('seller_id')
    description = data.get('description')
    price = data.get('price')
    gender = data.get('gender')
    size = data.get('size')
    youth_size = data.get('youth_size')
    featured = data.get('featured')
    brand = data.get('brand')
    sport = data.get('sport')
    quantity = data.get('quantity')
    condition = data.get('condition')
    image_url = data.get('image_url')
    year_product_made = data.get('year_product_made')
    avg_rating = data.get('avg_rating')

    # Update the product via the service
    product = create_product(
        seller_id=seller_id,
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
        image_url=image_url,
        date_listed=datetime.now(),
        year_product_made=year_product_made,
        avg_rating=avg_rating
    )
    
    if Product:
        return jsonify({
            'message': 'Product created successfully',
            'product': product.to_dict()
        })
    
    return jsonify({
        'error': 'Error creating product'
    })