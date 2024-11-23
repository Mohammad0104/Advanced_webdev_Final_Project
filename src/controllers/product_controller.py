from flask import Blueprint, request, jsonify
from datetime import datetime
from services import product_service
from models.product import Product
import base64

product_bp = Blueprint('product_bp', __name__)

# Create a new product
@product_bp.route('/create_product', methods=['POST'])
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
        year_product_made = data.get('year_product_made')
        avg_rating = data.get('avg_rating')

        # Validate required fields
        if not all([seller_id, name, price, quantity, condition]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Create the product using the service
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
            image=image_binary,
            date_listed=datetime.now(),
            year_product_made=year_product_made,
            avg_rating=avg_rating
        )

        # Serialize product to dict and re-encode image for JSON response
        product_dict = product.to_dict()
        product_dict['image'] = base64.b64encode(product_dict['image']).decode('utf-8')

        return jsonify({
            'message': 'Product created successfully',
            'product': product_dict
        }), 201

    except Exception as e:
        print(f"Error creating product: {e}")
        return jsonify({'error': 'Internal server error'}), 500


# Get all products
@product_bp.route('/products', methods=['GET'])
def get_products():
    """Fetch all products from the database"""
    try:
        products = product_service.get_all_products()

        # Convert products to JSON-friendly format
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
def get_product(product_id):
    """Fetch a product by its ID"""
    try:
        product = product_service.get_product_by_id(product_id)

        if not product:
            return jsonify({'error': 'Product not found'}), 404

        # Serialize product and re-encode image for JSON response
        product_dict = product.to_dict()
        if product_dict.get('image'):
            product_dict['image'] = base64.b64encode(product_dict['image']).decode('utf-8')

        return jsonify({'product': product_dict}), 200

    except Exception as e:
        print(f"Error fetching product: {e}")
        return jsonify({'error': 'Internal server error'}), 500


# Update a product
@product_bp.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update a specific product by its ID"""
    try:
        data = request.get_json()
        product = product_service.get_product_by_id(product_id)

        if not product:
            return jsonify({'error': 'Product not found'}), 404

        # Update product fields if they exist in the request
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
            image=base64.b64decode(data['image'].split(',')[1]) if data.get('image') else None,
            year_product_made=data.get('year_product_made'),
            avg_rating=data.get('avg_rating'),
        )

        updated_product = product_service.get_product_by_id(product_id)
        product_dict = updated_product.to_dict()
        if product_dict.get('image'):
            product_dict['image'] = base64.b64encode(product_dict['image']).decode('utf-8')

        return jsonify({'message': 'Product updated successfully', 'product': product_dict}), 200

    except Exception as e:
        print(f"Error updating product: {e}")
        return jsonify({'error': 'Internal server error'}), 500
