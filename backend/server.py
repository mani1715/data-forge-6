from flask import Flask
from flask_cors import CORS
from config import Config
import os
from asgiref.wsgi import WsgiToAsgi

# Import the Blueprints
from routes.data_routes import data_bp
from routes.clean_routes import clean_bp

flask_app = Flask(__name__)
flask_app.config.from_object(Config)

# Configure for large file uploads - 500MB
flask_app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB
flask_app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
flask_app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Ensure upload folder exists
os.makedirs(flask_app.config['UPLOAD_FOLDER'], exist_ok=True)

# Enable CORS
CORS(flask_app, resources={r"/api/*": {"origins": "*"}})

# Register the Routes
flask_app.register_blueprint(data_bp, url_prefix='/api')
flask_app.register_blueprint(clean_bp, url_prefix='/api')

@flask_app.route('/')
def index():
    return "DataForge API is Live."

@flask_app.route('/api/health')
def health():
    return {"status": "healthy"}

@flask_app.errorhandler(413)
def too_large(e):
    return {"error": "File too large. Max 500MB allowed."}, 413

# Wrap Flask in ASGI for uvicorn compatibility
app = WsgiToAsgi(flask_app)
