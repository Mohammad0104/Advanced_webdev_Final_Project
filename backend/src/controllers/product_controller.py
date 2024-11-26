from flask import Blueprint, request, jsonify
from datetime import datetime
from services import product_service
from flask_cors import cross_origin
import base64

from services.auth import login_required

product_bp = Blueprint('product_bp', __name__)


# Create a new product
@product_bp.route('/create_product', methods=['POST'])
@cross_origin()
def create_new_product():
    try:
        data = request.get_json()
        seller_id = data.get('seller_id')

        # Decode the base64 image data
        image_data = data.get('image')
        if image_data:
            image_binary = base64.b64decode(image_data.split(',')[1])  # Strip "data:image/png;base64," part
        else:
            return jsonify({'error': 'Image data is missing'}), 400

        # Extract other product details
        product_details = {
            'name': data.get('name'),
            'description': data.get('description'),
            'price': data.get('price'),
            'gender': data.get('gender'),
            'size': data.get('size'),
            'youth_size': data.get('youth_size'),
            'featured': data.get('featured'),
            'brand': data.get('brand'),
            'sport': data.get('sport'),
            'quantity': data.get('quantity'),
            'condition': data.get('condition'),
            'year_product_made': data.get('year_product_made'),
            'avg_rating': data.get('avg_rating'),
        }

        # Validate required fields
        if not all([seller_id, product_details['name'], product_details['price'], product_details['quantity'], product_details['condition']]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Create the product using the service
        product = product_service.create_product(
            seller_id=seller_id,
            image=image_binary,
            date_listed=datetime.now(),
            **product_details
        )

        # Serialize product to dict and re-encode image for JSON response
        product_dict = product.to_dict()
        product_dict['image'] = base64.b64encode(product_dict['image']).decode('utf-8')

        return jsonify({'message': 'Product created successfully', 'product': product_dict}), 201

    except Exception as e:
        print(f"Error creating product: {e}")
        return jsonify({'error': 'Internal server error'}), 500


# Get all products
@product_bp.route('/products', methods=['GET'])
@cross_origin()
def get_products():
    try:
        products = product_service.get_all_products()

        products_list = []
        for product in products:
            product_dict = product.to_dict()
            if product_dict.get('image'):
                product_dict['image'] = base64.b64encode(product_dict['image']).decode('utf-8')
            products_list.append(product_dict)

        return jsonify({'products': products_list}), 200

    except Exception as e:
        print(f"Error fetching products: {e}")
        return jsonify({'error': 'Internal server error'}), 500


# Get a specific product by ID
@product_bp.route('/product/<int:product_id>', methods=['GET'])
@cross_origin()
def get_product(product_id):
    try:
        product = product_service.get_product_by_id(product_id)

        if not product:
            return jsonify({'error': 'Product not found'}), 404

        product_dict = product.to_dict()
        if product_dict.get('image'):
            product_dict['image'] = base64.b64encode(product_dict['image']).decode('utf-8')

        return jsonify({'product': product_dict}), 200

    except Exception as e:
        print(f"Error fetching product: {e}")
        return jsonify({'error': 'Internal server error'}), 500


# Update a product
@product_bp.route('/product/<int:product_id>', methods=['PUT'])
@cross_origin()
def update_product(product_id):
    try:
        data = request.get_json()
        product = product_service.get_product_by_id(product_id)

        if not product:
            return jsonify({'error': 'Product not found'}), 404

        # Decode the image if provided
        image_binary = None
        if data.get('image'):
            try:
                image_binary = base64.b64decode(data['image'].split(',')[1])  # Decode the base64 string
            except Exception as e:
                return jsonify({'error': 'Invalid image format'}), 400

        # Update product fields using the service
        product_service.update_product(
            product_id=product_id,
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            gender=data.get('gender'),
            size=data.get('size'),
            youth_size=data.get('youth_size'),
            featured=data.get('featured'),
            brand=data.get('brand'),
            sport=data.get('sport'),
            quantity=data.get('quantity'),
            condition=data.get('condition'),
            image=image_binary,
            year_product_made=data.get('year_product_made'),
            avg_rating=data.get('avg_rating'),
        )

        # Fetch and return the updated product
        updated_product = product_service.get_product_by_id(product_id)
        product_dict = updated_product.to_dict()
        if product_dict.get('image'):
            product_dict['image'] = base64.b64encode(product_dict['image']).decode('utf-8')

        return jsonify({'message': 'Product updated successfully', 'product': product_dict}), 200

    except Exception as e:
        print(f"Error updating product: {e}")
        return jsonify({'error': 'Internal server error'}), 500
