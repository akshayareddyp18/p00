from flask import Blueprint, request, jsonify
import sqlite3


from database import get_db, get_user
from auth import pwd_context


from flask_jwt_extended import(
    jwt_required,
    get_jwt_identity,
    create_access_token,
    get_jwt
)

from datetime import timedelta





auth_bp = Blueprint("auth", __name__)

BLACKLIST = set()


@auth_bp.route("/signup", methods=["POST"])

def signup():
    """Registers a new user securely."""
    data = request.json
    conn = get_db()

    required_fields = ["username", "password", "email"]

    for field in required_fields:
        if field not in data:
            conn.close()
            return jsonify({"error": f"Missing field: {field}"}), 400


    if get_user(data["username"], conn):
        conn.close()
        return jsonify({"error": "User already exists"}), 400

    # Check if the email already exists
    cursor = conn.execute("SELECT id FROM users WHERE email = ?", (data["email"],))
    existing_email = cursor.fetchone()


    if existing_email:
        conn.close()
        return jsonify({"error": "Email already in use"}), 400



    hashed_password = pwd_context.hash(data["password"])

    try:
        conn.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                 (data["username"], hashed_password, data["email"]))


        conn.commit()
        return jsonify({"message": "User created successfully"}), 201
    except sqlite.IntegrityError:
        return jsonify({"error": "Database error"}), 500
    finally:
        conn.close()


#    return jsonify({"message": "User created successfully"}), 201




@auth_bp.route("/login", methods=["POST"])


def login():
    data = request.json
    conn = get_db()
    user_data = get_user(data["username"], conn)
    conn.close()

    if not user_data or not pwd_context.verify(data["password"], user_data["password"]):
        return jsonify({"error": "Invalid credentials"}), 400


    access_token = create_access_token(identity = data["username"], expires_delta=timedelta(minutes=15))
    refresh_token = create_access_token(identity = data["username"], expires_delta=timedelta(days=1))



    response = jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token
    })


    return response



@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    BLACKLIST.add(jti)
    return jsonify({"message": "Logout successful"}), 200




@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
#    return jsonify({"message": "This is a protected route"})


    current_user = get_jwt_identity()
    return jsonify({"message": f"Hello, {current_user}! This is a protected route."})


@auth_bp.route("/user-profile", methods=["GET"])
@jwt_required()
def user_profile():

    current_user = get_jwt_identity()
    conn = get_db()
    user_data = get_user(current_user, conn)

    conn.close()

    if user_data:
        return jsonify({"username": user_data["username"]})  # Return user-specific data
    return jsonify({"error": "User not found"}), 404

