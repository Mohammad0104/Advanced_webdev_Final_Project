<<<<<<< Updated upstream
from flask import Flask
from models import db
from config import Config
from controllers.oauth_controller import oauth_bp

def create_app():
  app = Flask(__name__)
  
  # Initialize extensions
  # db.init_app(app)
  
  app.secret_key = Config.SECRET_KEY
  
  # Register blueprints
  app.register_blueprint(oauth_bp)
    
  return app

if __name__ == '__main__':
  app = create_app()
  app.run(debug=True)
=======
from flask import Flask, render_template, session, redirect
from your_oauth_service_module import OAuthService  # Adjust the import according to your project

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a secret key for securely signing the session

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/google')
def google_login():
    oauth_service = OAuthService()
    authorization_url, state = oauth_service.get_authorization_url()
    session['oauth_state'] = state  # Store the state in session for later validation
    return redirect(authorization_url)

if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> Stashed changes
