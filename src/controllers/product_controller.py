from flask import Blueprint, request, jsonify, abort
from datetime import datetime
from services import product_service
from models.product import Product
import base64

from services.auth import login_required

product_bp = Blueprint('product_bp', __name__)


@product_bp.route('/create_product', methods=['POST'])
@login_required
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
    product = product_service.create_product(
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
    

@product_bp.route('/products', methods=['GET'])
def get_products():
    """Route used for viewing all the products in the db

    Returns:
        JSON: list of products with their image base64 encoded
    """
    
    # get all the products in the db
    products = product_service.get_all_products()

    # making the data into a list and decoding the image
    products_list = []
    for product in products:
        product_dict = product.to_dict()
        product_dict['image'] = base64.b64encode(product_dict['image']).decode('utf-8')
        products_list.append(product_dict)

    # returning JSON message with the list of products under products:
    return jsonify({'products': products_list}), 200

        
@product_bp.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Route to view a specific product by its ID

    Args:
        product_id (int): the id of the product to view

    Returns:
        JSON: The product details along with base64-encoded image data
    """
    
    # get the product with the given id
    product = product_service.get_product_by_id(product_id)

    if not product:
        return jsonify({'error': 'Product not found'}), 404

    # convert the product to a dictionary and encode the image for JSON
    product_dict = product.to_dict()
    product_dict['image'] = base64.b64encode(product_dict['image']).decode('utf-8')

    return jsonify({'product': product_dict}), 200