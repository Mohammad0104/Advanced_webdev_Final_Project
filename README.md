# Advanced Web Dev Final Project - *Sports Equipment Marketplace*


## Group Information
- **Anthony Liscio (100787902)**
- **Mohammad (100755461)**


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
    - in package.json:
      - change `"proxy": "http://backend:8080"` to `"proxy": "http://localhost:8080"` (this change is only for running locally, `http://backend:8080` is needed for running this on docker)
    - `cd frontend`
    - `npm install` (if you haven't run the frontend yet)
    - `npm start`
    - once ready, go to http://localhost:3000

### To run on docker container:
- ensure that in `frontend/package.json` there is this line exactly: `"proxy": "http://backend:8080"` (this is important)
- run docker desktop/engine
- open terminal:
  - run `docker-compose up --build`
- once the backend and frontend are ready, go to http://localhost:3000

## Database Diagram
![database diagram](assets/db_diagram.png)
## Pytests
![image](https://github.com/user-attachments/assets/cb9b8fc2-c2cd-40bf-a797-bdc85a470f5c)
![image](https://github.com/user-attachments/assets/397b561c-915f-473d-8e98-92695f79c685)
![image](https://github.com/user-attachments/assets/b91dde46-c64c-4e02-82ab-102e9afd9f7d)




