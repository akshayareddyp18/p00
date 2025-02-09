from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_talisman import Talisman
import os
from flask_jwt_extended import JWTManager
from routes.auth_routes import auth_bp



app = Flask(__name__)
app.config.from_object("config.Config")


'''
app.config["JWT_HEADER_NAME"] = "Authorization"  # Default is 'Authorization'
app.config["JWT_HEADER_TYPE"] = "Bearer"  # Default is 'Bearer'
app.config["JWT_SECRET_KEY"] = "your_jwt_secret_here"
app.config["JWT_ALGORITHM"] = "HS256"
'''



CORS(app, supports_credentials=True)
Talisman(app, content_security_policy=None)


jwt = JWTManager(app)  # ✅ Initialize JWTManager




# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/")




# Define frontend path
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))




@app.route("/")
def serve_frontend():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory(FRONTEND_DIR, path)

if __name__ == "__main__":
    app.run(port=8000, debug=True)
