# Advanced Web Dev Final Project - *Sports Equipment Marketplace*


## Group Information
- **Anthony Liscio (100787902)**
- **.Mohammad (100755461)**


## Run Instructions:
### To run locally:
- Open 2 terminals (windows command line)
  - In 1 terminal:
    - Create virtual environment (should work on other versions but we used 3.12.2):
      - `python -m venv .venv` or `python3.12.2 -m venv .venv` (to use specific version if needed)
    - Run virtual environment:
      - `.venv\Scripts\activate`
    - Install dependencies:
      - `cd backend`
      - (if you'd like to use the most up to date pip) `python -m pip install --upgrade pip`
      - `pip install -r requirements.txt`
    - Add the necessary .env and client_secret.json files
    - Run backend:
      - `python src/app.py`
  - In the other terminal, run the frontend:
    - in `frontend/package.json`:
      - change `"proxy": "http://backend:8080"` to `"proxy": "http://localhost:8080"` (this change is only for running locally, `http://backend:8080` is needed for running this on docker)
    - `cd frontend`
    - `npm install`
    - `npm start`
    - once ready, go to http://localhost:3000

### To run on docker container:
- ensure that in `frontend/package.json` there is this line exactly: `"proxy": "http://backend:8080"` (this is important)
- run docker desktop/engine
- open terminal:
  - run `docker-compose up --build` 
  - This should take at least a few minutes.  Once it's done building and the backend and frontend run, go to http://localhost:3000

## Database
- Used ORM with Flask-SQLAlchemy on sqlite database
- The tables:
  - **user**
    - stores information about the user that we get from the Google OAuth 2.0, such as name and email
    - no passwords are stored since the logging in process is purely through Google OAuth 2.0 only
  - **product**
    - stores lots of information about a product
    - has a foreign key of the user.id which represents the seller (`seller_id`) who created the product for sale
  - **review**
    - stores information for product rating
    - has a foreign key of the user.id (`reviewer_id`) which represents the reviewer who created the review
    - has a foreign key of the product.id (`product_id`) which represents the product of which the review is for
  - **cart**
    - stores subtotal
    - has a foreign key of the user.id (`user_id`) which represents the user who created the cart
    - when a purchase is completed, the cart that was used is deleted
  - **cart_item**
    - stores item quantity
    - has a foreign key of the cart.id (`cart_id`) which represents the cart that the cart_item is in
    - has a foreign key of the product.id (`product.id`) which represents the product which the cart_item is linked to (essentially cart_item is a product that is currently assigned to and used by a cart)
    - when a purchase is completed, the cart_items that were used in the cart are also deleted
  - **order**
    - stores the order history information and total
    - good way to see purchase history, while cart and cart_item are deleted after they are used in a purchase
    - has a foreign key of the user.id (`user_id`) which represents the user for which the order history is for
  - **order_item**
    - stores the product name, quantity, and price (since its possible products can be altered after a purchase, storing them here will show accurate price for when it was purchased)
    - has a foreign key of the order.id (`order_id`) which represents the order that the order_item is in
![database diagram](assets/db_diagram.png)

## Pytests
- to run:
  - `cd backend`
  - if not already done: `pip install -r requirements.txt`
  - `pytest tests/`
![image](https://github.com/user-attachments/assets/cb9b8fc2-c2cd-40bf-a797-bdc85a470f5c)
![image](https://github.com/user-attachments/assets/397b561c-915f-473d-8e98-92695f79c685)
![image](https://github.com/user-attachments/assets/b91dde46-c64c-4e02-82ab-102e9afd9f7d)

CLI TEST
- **lint.yaml**
![image](https://github.com/user-attachments/assets/7abde393-7166-45f9-a3ef-ee49dc71f941)
- **test.yaml**
![image](https://github.com/user-attachments/assets/50bf2025-266d-4a38-acf8-d16bb1d33a86)
- **CodeQL Analysis**
![image](https://github.com/user-attachments/assets/00faa6bd-9908-4bab-9248-d130447c079e)
- **Dependabot Updates**
![image](https://github.com/user-attachments/assets/bf0a36e9-4c2e-4238-b15b-fe050883d548)
## UML
![Uml](https://github.com/user-attachments/assets/91c44a10-0e18-482b-9c72-261a438395b6)











