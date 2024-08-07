import firebase_admin
from firebase_admin import credentials, auth, db
from flask import Flask, request, jsonify
from flask_cors import CORS


cred = credentials.Certificate("./credentials.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://pure-focus-2e5bf-default-rtdb.firebaseio.com/"
})
firebase_app = firebase_admin.get_app()

app = Flask(__name__)
CORS(app)

def success_response(data: any, code: int):
    """
    Returns a success response with the given data and status code.

    :param data: The data to include in the response.
    :param code: The HTTP status code.
    :return: A Flask JSON response with the given data and status code.
    """
    return jsonify(data), code


def error_response(error: str, code: int):
    """
    Returns an error response with the given error message and status code.

    :param error: The error message to include in the response.
    :param code: The HTTP status code.
    :return: A Flask JSON response with the error message and status code.
    """
    return jsonify({'error': error}), code


@app.route("/", methods=["GET"])
def index():
    return success_response("Hello, world!", 200)

@app.route("/users/create", methods=["POST"])
def create_user():
    """
    Creates a new user with the provided email and password.

    Expects a JSON payload in the request body with the following fields:
    - email: The email address of the user.
    - password: The password for the user's account.

    :return: A JSON response indicating the result of the user creation process.
             On success, returns a JSON response with the user data and a 200 status code.
             On failure, returns a JSON response with an error message and a 400 status code.
    """
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    if not email:
        return error_response("Email is required", 400)
    if not password:
        return error_response("Password is required", 400)
    try:
        user = auth.create_user(email=email, password=password)  # FireBase Error OR ValueError
        user_data = {
            'message': "User created successfully",
            'user_id': user.uid,
            'email': user.email
        }
        return success_response(user_data, 200)
    except Exception as e:
        return error_response(f"Error creating user: {str(e)}", 400)
    

@app.route("/users/profile/working_hours", methods=["POST"])
def set_working_hours():
    print("setting working hours")

    # get the idtoken of the user and authenticate it

    data = request.get_json()

    id_token = request.headers.get("Authorization")

    if not id_token:
        return error_response("id_token is required", 400)

    uid = ""
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    print("Point 2")
    

    # get the json from the request

    data = request.get_json()

    
    ref = db.reference(f'users/{uid}/profile/working_hours')

    ref.set(data)

    return jsonify({"message": "Working hours updated successfully"}), 200
    

if __name__ == '__main__':
    app.run(debug=True)