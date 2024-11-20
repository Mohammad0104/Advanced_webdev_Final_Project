from flask import Blueprint, request, jsonify, abort
from datetime import datetime
from services.product_service import create_product
from models.product import Product
import base64

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/create_product', methods=['POST'])
def create_new_product():
    data = request.get_json()
    
    seller_id = data.get('seller_id')
    
    # get image data and then decode it
    image_data = data.get('image')
    image_binary = base64.b64decode(image_data.split(',')[1])  # strip the "data:image/png;base64," part
    

    name = data.get('name')
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
    image = image_binary
    year_product_made = data.get('year_product_made')
    avg_rating = data.get('avg_rating')

    # Update the product via the service
    product = create_product(
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
        date_listed=datetime.now(),
        year_product_made=year_product_made,
        avg_rating=avg_rating
    )
    product_dict = product.to_dict()
    product_dict['image'] = base64.b64encode(product_dict['image']).decode('utf-8') # encode so it works with JSON
    
    if Product:
        return jsonify({
            'message': 'Product created successfully',
            'product': product_dict
        })
    
    return jsonify({
        'error': 'Error creating product'
    })